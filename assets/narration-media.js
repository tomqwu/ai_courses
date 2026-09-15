/* Narration media: strict WebVTT parsing and one audio owner for the whole page.
 *
 * Two lessons from ai_qe are load-bearing here (ai_qe/assets/js/narration-media.js):
 *   1. Exactly one player may own audio at a time, and focus is claimed synchronously BEFORE the
 *      media starts buffering — otherwise a slow-loading clip and a fast one both start talking.
 *   2. A play request we already cancelled must not steal focus back when its promise resolves.
 * Cross-tab coordination uses BroadcastChannel with a localStorage fallback, so two open tabs (or
 * two embedded frames) cannot talk over each other.
 */
(() => {
  'use strict';
  if (window.APSNarrationMedia) return;

  function parseTime(value) {
    if (!/^(?:\d{2,}:)?\d{2}:\d{2}\.\d{3}$/.test(value)) return NaN;
    return value.split(':').reduce((sum, part) => sum * 60 + Number(part), 0);
  }

  const ENTITIES = { '&amp;': '&', '&lt;': '<', '&gt;': '>', '&nbsp;': ' ', '&quot;': '"' };

  function parseCaptions(text) {
    if (!/^\uFEFF?WEBVTT(?:\s|$)/.test(text)) throw new Error('Invalid caption file');
    const cues = [];
    const blocks = text.replace(/^\uFEFF/, '').replace(/\r/g, '').split(/\n\s*\n/);
    for (const block of blocks) {
      const lines = block.split('\n');
      if (/^(?:WEBVTT|NOTE|STYLE|REGION)(?:\s|$)/.test(lines[0])) continue;
      const timing = lines.findIndex(line => line.includes('-->'));
      if (timing < 0) continue;
      const match = lines[timing].match(/(\S+)\s+-->\s+(\S+)/);
      if (!match) continue;
      const start = parseTime(match[1]);
      const end = parseTime(match[2]);
      // Render cue text as text, never as markup.
      const caption = lines.slice(timing + 1).join(' ')
        .replace(/<[^>]*>/g, '')
        .replace(/&(?:amp|lt|gt|nbsp|quot);/g, entity => ENTITIES[entity])
        .replace(/[ \t]+/g, ' ')
        .trim();
      if (Number.isFinite(start) && end > start && caption) cues.push({ start, end, text: caption });
    }
    if (!cues.length) throw new Error('Empty caption file');
    return cues.sort((a, b) => a.start - b.start);
  }

  // Find the topmost same-origin frame so coordination spans embedded decks too.
  let root = window;
  try {
    while (root.parent !== root && root.parent.location.origin === location.origin) root = root.parent;
  } catch (_) { /* cross-origin host: it has its own controls */ }

  function pauseTree(view, except) {
    try {
      if (view.location.origin !== location.origin) return;
      view.document.querySelectorAll('audio, video').forEach(media => { if (media !== except) media.pause(); });
      view.document.dispatchEvent(new view.CustomEvent('aps:narration-interrupt', { detail: { except } }));
      view.document.querySelectorAll('iframe').forEach(frame => {
        if (frame.contentWindow) pauseTree(frame.contentWindow, except);
      });
    } catch (_) { /* other origins keep their own playback */ }
  }

  const KEY = '__apsNarrationFocus';
  if (!root[KEY]) {
    const channelName = 'aps:narration-focus';
    const id = root.crypto?.randomUUID?.() || Math.random().toString(36).slice(2);
    let owner = null;
    let latest = { time: 0, id: '' };
    let channel = null;
    const newer = value => value.time > latest.time || (value.time === latest.time && value.id > latest.id);
    const receive = value => {
      if (!value || value.type !== channelName || typeof value.id !== 'string') return;
      if (!Number.isFinite(value.time) || value.id === id || !newer(value)) return;
      latest = value;
      owner?.pause();
      owner = null;
      pauseTree(root, null);
    };
    try {
      channel = new root.BroadcastChannel(channelName);
      channel.onmessage = event => receive(event.data);
    } catch (_) { /* storage events still coordinate tabs */ }
    root.addEventListener('storage', event => {
      if (event.key !== channelName || !event.newValue) return;
      try { receive(JSON.parse(event.newValue)); } catch (_) { /* ignore unrelated values */ }
    });
    root[KEY] = {
      claim(media) {
        if (owner === media) return;
        owner?.pause();
        owner = media;
        pauseTree(root, media);
        latest = { type: channelName, id, time: Math.max(Date.now(), latest.time + 1) };
        channel?.postMessage(latest);
        try { root.localStorage.setItem(channelName, JSON.stringify(latest)); } catch (_) { /* fine */ }
      },
      owns: media => owner === media,
      stop() {
        owner?.pause();
        owner = null;
        pauseTree(root, null);
      },
    };
  }

  const coordinator = root[KEY];
  const claim = media => coordinator.claim(media);
  const play = media => { claim(media); return media.play(); };

  document.addEventListener('play', event => {
    const media = event.target;
    if (media?.matches?.('audio, video') && !media.paused) claim(media);
  }, true);
  document.addEventListener('visibilitychange', () => { if (document.hidden) coordinator.stop(); });
  window.addEventListener('pagehide', () => coordinator.stop());

  window.APSNarrationMedia = Object.freeze({ parseCaptions, claim, play, owns: coordinator.owns });
})();
