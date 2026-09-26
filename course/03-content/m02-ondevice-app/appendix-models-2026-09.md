# M2 Appendix — On-Device Model Matrix, read 2026-09-26

> **Dated snapshot, read 2026-09-26.** Every row was checked against the source it names on that date.
> Small models turn over in months, so treat this file as a record of what was true then, not as a
> recommendation, and re-read a row's source before you quote it.

This is the model survey that M2.2 points to (`course/03-content/m02-ondevice-app/lesson.md`, M2.2).
The lesson teaches the routing rules; this file lists what those rules can choose from today. **The lab
default does not move with it.** `qwen3:0.6b` stays the model `lab.md` and TinyCopilot name, because
it runs on any laptop, not because it is the best model listed here.

## How to read the evidence column

| Tag | What it means | What it does not mean |
|---|---|---|
| **Vendor, primary** | Read directly in the vendor's own repository or documentation source: model card, README, docs Markdown, SDK code | That the claim is true. It is the vendor describing its own product |
| **Runtime code** | A runtime's own source names the tag, file size or memory floor: Ollama's integration tests, Google's AI Edge Gallery allowlist | Anything about quality. It shows the tag is published and exercised |
| **Case study** | Measured or decided in a case-study repo, with a pointer | Independent. One maintainer's benchmark on one product |
| **Secondary** | Carried over from `course/00-research/08-domain-currency-2026.md` (search summaries, third-party articles) and not re-confirmed on the read date | Confirmed |
| **Unverified** | No primary source was readable from here: the network proxy blocked it | False. It is still open |

No row is an independent measurement. "Good for" is the vendor's own positioning unless the cell says
*Course*, which marks the only judgement added here: where M2.2's routing rules would place the model.

## A. Open-weight models you run yourself

You download these as files and run them in a runtime: Ollama in this course's labs; llama.cpp, MLX,
Foundry Local or LiteRT-LM elsewhere.

| Family | Sizes (vendor-stated) | Good for | Where it runs | Source, read 2026-09-26 | Evidence |
|---|---|---|---|---|---|
| **Qwen3**: the lab default | 0.6B, 1.7B, 4B, 8B, 14B, 32B dense; 30B-A3B and 235B-A22B mixture-of-experts; a 2507 refresh of 4B, 30B-A3B and 235B-A22B. Apache 2.0 | Vendor: switchable thinking and non-thinking modes, 100+ languages, tool use. *Course:* `qwen3:0.6b` is the lab's runs-anywhere model for Listener and Quick in TinyCopilot, never a quality pick | Ollama: `qwen3:0.6b` is in Ollama's own small-model test set and `qwen3:8b` in its medium set (commented "~6.6G"). The README also documents llama.cpp, vLLM and SGLang | [QwenLM/Qwen3 README](https://github.com/QwenLM/Qwen3/blob/main/README.md); [ollama `integration/concurrency_test.go`](https://github.com/ollama/ollama/blob/main/integration/concurrency_test.go) | Vendor, primary; Runtime code |
| **Qwen3.5 small** | 0.8B, 2B, 4B, 9B, published 2026-03-02; larger siblings 27B, 35B-A3B, 122B-A10B, 397B-A17B | Vendor: one vision-language family, 201 languages, hybrid attention with sparse mixture-of-experts | llama.cpp and MLX (`mlx-lm` for text, `mlx-vlm` for vision), per the README. Ollama's launcher recommends `qwen3.5` locally with a 14 GB VRAM estimate, and its release tests run `qwen3.5:2b` with a 4 GB minimum. Ollama tags for 0.8B, 4B and 9B: **unverified** | [QwenLM/Qwen3.8 README](https://github.com/QwenLM/Qwen3.8/blob/main/README.md) (the repo now carries 3.5, 3.6 and 3.8); [ollama `integration/reg_release_test.go`](https://github.com/ollama/ollama/blob/main/integration/reg_release_test.go); `cmd/launch/models.go` | Vendor, primary; Runtime code. License: the README defers to the model card, **unverified** |
| **Qwen3.6 / Qwen3.8**, mid-size | Qwen3.6: 35B-A3B (2026-04-16), 27B (2026-04-22). Qwen3.8: 27B (2026-08-14) | Vendor: agentic coding (3.6), long-horizon agent tasks (3.8). *Course:* a Deep candidate on a workstation, not a laptop Quick model | Ollama tests `qwen3.6:27b` with a 20 GB VRAM minimum and lists `qwen3.8:27b` among its tool-calling test models | Same README; same test file | Vendor, primary; Runtime code |
| **Gemma 4** | E2B, E4B, 26B-A4B, 31B in Google DeepMind's checkpoint list. Ollama also tests a `gemma4:12b`, and a post linked from the LiteRT-LM README is titled "Bringing Gemma 4 12B to your Laptop"; the 12B is absent from the checkpoint list: **unverified** against Google's model card | Vendor: the E2B and E4B builds take image **and audio** input (Gallery allowlist), and Ollama runs its audio-transcription tests on `gemma4:e2b` and `gemma4:e4b`. For this archetype that means one model that can listen | Ollama: `gemma4` is one of the two local models Ollama's launcher recommends, with a 12 GB VRAM estimate. Android through LiteRT-LM: Google's Gallery app ships E2B as a 2.59 GB file needing 8 GB of device memory (32K context) and E4B as 3.66 GB needing 12 GB | [google-deepmind/gemma `gemma/gm/ckpts/_paths.py`](https://github.com/google-deepmind/gemma/blob/main/gemma/gm/ckpts/_paths.py); [google-ai-edge/gallery `model_allowlists/1_0_18.json`](https://github.com/google-ai-edge/gallery/blob/main/model_allowlists/1_0_18.json); [ollama `cmd/launch/models.go`](https://github.com/ollama/ollama/blob/main/cmd/launch/models.go); `reg_release_test.go` | Vendor, primary; Runtime code. License: **Secondary** (Apache 2.0 per 08; the model card on ai.google.dev was blocked) |
| **Phi-4-mini** | 3.8B; Phi-4-multimodal (5.6B) adds vision and audio | Vendor: text, chat and coding. *Secondary:* 08 calls it the "8 GB machine" pick, citing a third-party blog | Ollama's library inventory lists `phi4-mini`. Microsoft's Windows docs use the Foundry Local alias `phi-4-mini` as the fallback when Phi Silica is unavailable. The Phi Cookbook ships ONNX samples | [microsoft/PhiCookBook, Phi family table](https://github.com/microsoft/PhiCookBook/blob/main/md/01.Introduction/01/01.PhiFamily.md); [windows-ai-docs `docs/windows-ai-comparison.md`](https://github.com/MicrosoftDocs/windows-ai-docs/blob/docs/docs/windows-ai-comparison.md) (ms.date 2026-04-06); [ollama `integration/reg_library_test.go`](https://github.com/ollama/ollama/blob/main/integration/reg_library_test.go) | Vendor, primary; Runtime code. License: **unverified** |
| **Llama 3.2** | 1B (1.23B) and 3B (3.21B); 128k context, 8k for the quantized builds; released 2024-10-24 | Vendor: multilingual dialogue, retrieval, summarization, "mobile AI powered writing assistants". *Course:* the oldest row here, a stable baseline rather than a current pick | Ollama tests `llama3.2:1b` in its small set and `llama3.2:3b` in its medium set (commented "~3.4G") | [meta-llama/llama-models `models/llama3_2/MODEL_CARD.md`](https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/MODEL_CARD.md); `concurrency_test.go` | Vendor, primary; Runtime code. License: Llama 3.2 Community License, a custom commercial license |
| **gpt-oss-20b** | 21B total, 3.6B active (mixture-of-experts, MXFP4). Apache 2.0 | Vendor: "lower latency, and local or specialized use cases"; runs "within 16GB of memory". *Course:* Deep on a 16 GB+ machine, not Quick | Ollama `gpt-oss:20b` (the README's own command; Ollama's release tests set a 16 GB VRAM minimum). Foundry Local's catalog names "GPT OSS" | [openai/gpt-oss README](https://github.com/openai/gpt-oss/blob/main/README.md); [microsoft/Foundry-Local README](https://github.com/microsoft/Foundry-Local/blob/main/README.md) | Vendor, primary; Runtime code |

**In Ollama's library inventory, not assessed here:** `lfm2.5`, `granite4.1`, `ministral-3`,
`gemma3n`, `smollm2`, among others. The inventory in `integration/reg_library_test.go` describes itself
as "roughly newest to oldest from https://ollama.com/library?sort=newest", with cloud-only models
omitted. A name there means a local tag exists. Nothing more.

## B. Platform models you call but do not ship

The operating system downloads, updates and runs these. You do not choose the size, and none of the
vendor pages read here states one.

| Model | Where it runs | What it constrains | Source, read 2026-09-26 | Evidence |
|---|---|---|---|---|
| **Apple Foundation Models, on-device** (`SystemLanguageModel`) | iOS, iPadOS, macOS and visionOS 26+ (the framework reaches watchOS 27, but the `SystemLanguageModel` page lists no watchOS), where the device and region support Apple Intelligence and the user has it switched on | Availability is a runtime check: `.deviceNotEligible`, `.appleIntelligenceNotEnabled`, `.modelNotReady`. Apple updates the model with the OS. The context size is an API value (`contextSize`), not a documented constant. ListenToMe caps every Apple prompt at 8,000 characters, and its code calls the window "~4k-token … shared by input and output" | [Apple: Foundation Models](https://developer.apple.com/documentation/foundationmodels), [`SystemLanguageModel`](https://developer.apple.com/documentation/foundationmodels/systemlanguagemodel); `ListenToMe/SharedPlatform/AppleIntelligenceProvider.swift:10-12`; `ListenToMe/Sources/ListenToMeCore/PromptBudget.swift:16-18` | Vendor, primary; Case study (the 4k figure is ListenToMe's reading, not Apple's) |
| **Apple Foundation Model on Private Cloud Compute** | Apple's servers, not the device: a third tier between local and third-party cloud | Apple: apps in the App Store Small Business Program with fewer than 2 million first-time downloads use it "at no cloud API cost". The 32K context and per-user daily quota that 08 reports were not re-read | [Apple WWDC26 Apple Intelligence guide](https://developer.apple.com/wwdc26/guides/apple-intelligence/) | Vendor, primary; context and quota **Secondary** |
| **Phi Silica** (Windows AI APIs) | Copilot+ PCs only: an NPU of 40+ TOPS and 16 GB+ of RAM | A Limited Access Feature, so you request an unlock token. "Not available in China." No size stated | [windows-ai-docs `docs/apis/phi-silica.md`](https://github.com/MicrosoftDocs/windows-ai-docs/blob/docs/docs/apis/phi-silica.md) (ms.date 2026-01-21); `docs/windows-ai-comparison.md` | Vendor, primary |
| **Gemini Nano** through ML Kit GenAI on AICore | Android devices whose AICore supports it; API level 26+ | Prompt input under 4,000 tokens; AICore enforces a per-app inference quota; the model can be `DOWNLOADABLE` or `DOWNLOADING` before it is `AVAILABLE`. The Prompt API artifact is `1.0.0-beta4`, a beta. The supported-device list: **unverified** (developers.google.com was blocked) | [Android Developers: Gemini Nano](https://developer.android.com/ai/gemini-nano) (last updated 2026-09-08); [android/skills `ml-kit-genai-prompt-api`](https://github.com/android/skills/blob/main/device-ai/ml-kit-genai-prompt-api/SKILL.md) (last-updated 2026-09-03) and its `references/get-started.md` | Vendor, primary |

## C. Speech models

| Model | Sizes | Where it runs | Source, read 2026-09-26 | Evidence |
|---|---|---|---|---|
| **Apple SpeechAnalyzer** | System model | macOS 26; ListenToMe's default engine (M2.1) | `ListenToMe/App/SpeechAnalyzerTranscriber.swift:6-39` | Case study |
| **Whisper** (OpenAI) | tiny 39M to large 1550M; turbo 809M, about 6 GB of VRAM per the README, and not trained for translation | Apple platforms through WhisperKit, a Swift package; Android only through Argmax's commercial Pro SDK. Windows through Foundry Local (`whisper-tiny` in its README), which Microsoft's docs say varies in performance and is "not available on all devices" | [openai/whisper README](https://github.com/openai/whisper/blob/main/README.md); [argmaxinc/WhisperKit README](https://github.com/argmaxinc/WhisperKit/blob/main/README.md); Foundry-Local README; [windows-ai-docs `docs/apis/speech-recognition.md`](https://github.com/MicrosoftDocs/windows-ai-docs/blob/docs/docs/apis/speech-recognition.md) | Vendor, primary |
| **ML Kit GenAI speech recognition** | Not stated | Android, on AICore | Android Developers: Gemini Nano | Vendor, primary; release status **unverified** |
| **Gemma 4 E2B / E4B**, audio input | See Table A | Ollama; LiteRT-LM | See Table A | Runtime code |

## D. Runtimes and platform frameworks on the read date

- **Apple.** The Foundation Models framework "provides access to any large language model, like the
  on-device and Private Cloud Compute models"; its `LanguageModel` protocol, introduced in OS 27, is
  how another provider plugs in ([Apple: `LanguageModel`](https://developer.apple.com/documentation/foundationmodels/languagemodel)).
  For your own models, the WWDC26 guide names Core AI, "a new framework built directly into the OS",
  and MLX, which "gains support for Metal 4 and GPU Neural Accelerators"
  ([WWDC26 machine-learning guide](https://developer.apple.com/wwdc26/guides/machine-learning/)).
  Vendor, primary. The one measurement: ListenToMe ran the Apple model as its automatic Quick
  evaluator, and "the native Auto experiment failed the quality gate (3/7 cases …)"
  (`ListenToMe/docs/SHARED-LIVE-SUMMARY.md:64-68`). Case study.
- **Ollama.** GitHub's release feed shows v0.34.4 (2026-09-24) and a v0.40.0 entry (2026-09-25)
  whose notes say that on Apple silicon "model architectures supported by the MLX runtime will
  automatically run on MLX". Whether v0.40.0 is a stable release, and the 32 GB memory floor 08
  reports for the MLX preview: **unverified**.
  Ollama installs on macOS, Windows and Linux ([README](https://github.com/ollama/ollama/blob/main/README.md)).
  [ollama releases](https://github.com/ollama/ollama/releases). Vendor, primary.
- **Windows, three layers.** Microsoft's own chooser: the Windows AI APIs (Phi Silica and imaging,
  OCR and search models) need a Copilot+ PC; Foundry Local offers "20+ open-source LLMs and speech
  models via an OpenAI-compatible API" on any Windows hardware; Windows ML runs any ONNX model
  ([`windows-ai-comparison.md`](https://github.com/MicrosoftDocs/windows-ai-docs/blob/docs/docs/windows-ai-comparison.md)).
  For speech the docs offer Whisper through Foundry Local or the older Windows SDK recognizer,
  "available on all devices". Vendor, primary.
- **Foundry Local.** The SDK's v1.0.0 release notes announce General Availability (April 2026); the
  SDK is at v2.0.1 (2026-09-01) and the CLI is still a "public preview" (0.10.x). Runs on Windows,
  macOS (Apple silicon) and Linux, per its README, which also says it "may collect usage data and
  send it to Microsoft". [Foundry-Local releases](https://github.com/microsoft/Foundry-Local/releases).
  Vendor, primary.
- **Windows ML.** ONNX Runtime with NPU, GPU and CPU execution providers "that Windows installs and
  keeps up to date via Windows Update" ([overview](https://github.com/MicrosoftDocs/windows-ai-docs/blob/docs/docs/new-windows-ml/overview.md),
  ms.date 2026-04-27). Shipped in the stable Windows App SDK 1.8.1, released 2025-09-23; the notes
  run to 1.8.8. Foundry Local's WinML build notes that virtual machines without GPU passthrough
  "return a successful response with empty content"
  ([`foundry-local/get-started.md`](https://github.com/MicrosoftDocs/windows-ai-docs/blob/docs/docs/foundry-local/get-started.md)). Running LLMs directly through ONNX Runtime GenAI on Windows ML is labelled *Preview*
  ([release notes](https://github.com/MicrosoftDocs/windows-dev-docs/blob/docs/hub/apps/windows-app-sdk/release-notes/windows-app-sdk-1-8.md);
  [`run-genai-onnx-models.md`](https://github.com/MicrosoftDocs/windows-ai-docs/blob/docs/docs/new-windows-ml/run-genai-onnx-models.md),
  ms.date 2026-03-17). Vendor, primary.
- **LiteRT-LM** (Google). Describes itself as "production-ready", at v0.16.0; its Kotlin and C++ APIs
  are marked Stable, Swift and JavaScript Early Preview
  ([README](https://github.com/google-ai-edge/LiteRT-LM/blob/main/README.md)). Vendor, primary.
- **Android, ML Kit GenAI.** Prompt, Summarization, Proofreading, Rewriting, Image Description and
  Speech Recognition APIs over Gemini Nano, "built on top of AICore, an Android system service"
  (Android Developers: Gemini Nano). Google's own `android/snippets` pins `genai-prompt` at
  `1.0.0-beta4` ([`gradle/libs.versions.toml`](https://github.com/android/snippets/blob/main/gradle/libs.versions.toml)).
  Vendor, primary.

## What could not be confirmed, and how it is handled

- **Ollama tags beyond Ollama's own code.** ollama.com was blocked, so a tag is named only where
  Ollama's repository names it. Other sizes are marked unverified rather than guessed.
- **Gemma 4's license and its 12B size; the Qwen3.5 and Phi-4-mini licenses.** Hugging Face and
  ai.google.dev were blocked. The license cells say so.
- **Apple's on-device parameter count.** No Apple page read here states one. Do not teach a number;
  08 gives the same warning.
- **ML Kit GenAI device support, and whether any GenAI API has left beta.** developers.google.com and
  Google's Maven repository were blocked. The beta version comes from Google's own sample repositories.
- **Quality.** Nothing here is an independent benchmark. The one measurement in this file,
  ListenToMe's quality gate on the Apple model (section D and M2.1), is the case study's own.

## Refreshing this appendix

1. Write a new `appendix-models-YYYY-MM.md` with the new date in its title and first line. Do not
   edit a dated file's rows in place.
2. Re-read every source and update each read date. A row whose source you cannot re-read becomes
   **Unverified**; it does not keep its old value.
3. Point M2.2 in `lesson.md` and the handout's file list at the new file, then delete the old one.
4. Leave `qwen3:0.6b` alone unless `lab.md`, TinyCopilot's `demo.py` and its privacy tests change
   with it.
5. Run `python3 course/06-production/verify.py`. It checks every case-study pointer in this file.
