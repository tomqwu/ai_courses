/*
 * Renders window.CATALOG (from products.js) into the page: a card per product, a filter per
 * category, a search box and a sort. No libraries, no build step, no network requests, so the
 * page behaves the same when you double-click index.html as it does on GitHub Pages.
 *
 * You should not need to edit this file to run your catalog. Change products.js instead.
 */
(function () {
  "use strict";

  var catalog = window.CATALOG;
  var grid = document.getElementById("grid");
  var status = document.getElementById("status");
  var filters = document.getElementById("filters");
  var search = document.getElementById("search");
  var sort = document.getElementById("sort");

  if (!catalog || !Array.isArray(catalog.products)) {
    status.textContent = "products.js did not load, or it has a mistake in it. Open it and check " +
      "for a missing comma or quote — the browser's developer console names the line.";
    return;
  }

  var store = catalog.store || {};
  var currency = store.currency || "USD";
  var money = new Intl.NumberFormat(undefined, { style: "currency", currency: currency });
  var state = { category: "All", query: "", sort: "featured" };

  document.title = store.name ? store.name + " — Catalog" : document.title;
  setText("store-name", store.name || "Your catalog");
  setText("store-tagline", store.tagline || "");
  setText("store-note", store.note || "");
  var contact = document.getElementById("store-contact");
  if (store.contact) { contact.href = store.contact; } else { contact.hidden = true; }
  setText("year", String(new Date().getFullYear()));

  function setText(id, value) {
    var el = document.getElementById(id);
    if (el) { el.textContent = value; }
  }

  function initials(name) {
    return name.split(/\s+/).slice(0, 2).map(function (w) { return w.charAt(0); }).join("").toUpperCase();
  }

  // Readable text on a coloured placeholder: dark ink on light colours, light ink on dark ones.
  function inkFor(hex) {
    var m = /^#?([0-9a-f]{6})$/i.exec(hex || "");
    if (!m) { return "#1d232a"; }
    var n = parseInt(m[1], 16);
    var r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
    var lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
    return lum > 0.55 ? "#1d232a" : "#ffffff";
  }

  var categories = ["All"];
  catalog.products.forEach(function (p) {
    if (p.category && categories.indexOf(p.category) === -1) { categories.push(p.category); }
  });

  categories.forEach(function (name) {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "chip";
    button.textContent = name;
    button.setAttribute("aria-pressed", name === state.category ? "true" : "false");
    button.addEventListener("click", function () {
      state.category = name;
      Array.prototype.forEach.call(filters.children, function (b) {
        b.setAttribute("aria-pressed", b.textContent === name ? "true" : "false");
      });
      render();
    });
    filters.appendChild(button);
  });

  search.addEventListener("input", function () { state.query = search.value.trim().toLowerCase(); render(); });
  sort.addEventListener("change", function () { state.sort = sort.value; render(); });

  function matches(p) {
    if (state.category !== "All" && p.category !== state.category) { return false; }
    if (!state.query) { return true; }
    var haystack = [p.name, p.category, p.summary].concat(p.tags || []).join(" ").toLowerCase();
    return haystack.indexOf(state.query) !== -1;
  }

  function sorted(list) {
    var copy = list.slice();
    if (state.sort === "price-asc") { copy.sort(function (a, b) { return a.price - b.price; }); }
    if (state.sort === "price-desc") { copy.sort(function (a, b) { return b.price - a.price; }); }
    if (state.sort === "name") { copy.sort(function (a, b) { return a.name.localeCompare(b.name); }); }
    return copy;
  }

  function card(p) {
    var article = document.createElement("article");
    article.className = "card";
    article.id = p.id;

    var media = document.createElement("div");
    media.className = "card-media";
    if (p.image) {
      var img = document.createElement("img");
      img.src = p.image;
      img.alt = p.imageAlt || p.name;
      img.loading = "lazy";
      media.appendChild(img);
    } else {
      media.style.background = p.color || "#cfd8dc";
      media.style.color = inkFor(p.color);
      media.setAttribute("aria-hidden", "true");
      media.textContent = initials(p.name);
    }
    article.appendChild(media);

    var body = document.createElement("div");
    body.className = "card-body";

    var cat = document.createElement("p");
    cat.className = "card-category";
    cat.textContent = p.category || "";
    body.appendChild(cat);

    var h = document.createElement("h2");
    h.className = "card-title";
    h.textContent = p.name;
    body.appendChild(h);

    var summary = document.createElement("p");
    summary.className = "card-summary";
    summary.textContent = p.summary || "";
    body.appendChild(summary);

    if (p.tags && p.tags.length) {
      var tags = document.createElement("ul");
      tags.className = "card-tags";
      tags.setAttribute("aria-label", "Details");
      p.tags.forEach(function (t) {
        var li = document.createElement("li");
        li.textContent = t;
        tags.appendChild(li);
      });
      body.appendChild(tags);
    }

    var foot = document.createElement("div");
    foot.className = "card-foot";
    var price = document.createElement("p");
    price.className = "card-price";
    price.textContent = typeof p.price === "number" ? money.format(p.price) : "";
    foot.appendChild(price);

    var action = document.createElement("a");
    action.className = "card-action";
    if (p.buyUrl) {
      action.href = p.buyUrl;
      action.textContent = "Buy";
      action.rel = "noopener";
      action.setAttribute("aria-label", "Buy " + p.name);
    } else if (store.contact) {
      action.href = store.contact + (store.contact.indexOf("mailto:") === 0 ? "?subject=" + encodeURIComponent(p.name) : "");
      action.textContent = "Ask about this";
      action.setAttribute("aria-label", "Ask about " + p.name);
    } else {
      action = null;
    }
    if (action) { foot.appendChild(action); }
    body.appendChild(foot);

    article.appendChild(body);
    return article;
  }

  function render() {
    var list = sorted(catalog.products.filter(matches));
    grid.textContent = "";
    list.forEach(function (p) { grid.appendChild(card(p)); });
    var total = catalog.products.length;
    status.textContent = list.length === total
      ? total + " products"
      : list.length === 0
        ? "Nothing matches that. Try another word, or choose All."
        : list.length + " of " + total + " products";
  }

  render();
}());
