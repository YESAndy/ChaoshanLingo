# Audio tooling

Two independent recording tracks. All output stays small enough for the
GitHub repo (course audio ~2 MB, full syllable bank ~20-25 MB).

## 1. Course audio (priority)

Per-word/phrase recordings replacing the Mandarin TTS placeholders.

- `manifest.csv` — every course item: Peng'im `text`, `hanzi` for the
  speaker to read, `record_as` filename, and the app's `target_hash`.
- `ingest.sh <dir>` — converts recordings (m4a/wav/mp3), compresses to
  32 kbps mono, installs into `apps/web/static/voice/` under hash names.

Recording tips: quiet room, one item per file, natural speed, one
consistent accent (府城 Chaozhou / 汕头 Swatow / 揭阳 Jieyang differ).

## 2. Syllable bank (future "speak anything" TTS)

Goal: client-side concatenative TTS — speak *any* Peng'im text by joining
per-syllable clips, like chaofayin.com. No server needed.

- `syllable-bank.csv` — all **2,215 attested syllable+tone combinations**
  (837 base syllables), derived from the ~19k-entry pronunciation
  dictionary in [teochew-g2p](https://github.com/p1an-lin-jung/teochew-g2p)
  (MIT-licensed data for Teochew speech synthesis). Sorted by corpus
  frequency with cumulative coverage:
  - top 200 syllables ≈ 39% of running text
  - top 500 ≈ 64%
  - top 800 ≈ 79%
  - top 1,200 ≈ 91%
  Record from the top; partial banks are already useful (fall back to
  per-item course audio when a syllable is missing).
- `ingest-syllables.sh <dir>` — installs clips as
  `apps/web/static/voice-bank/<syllable>.mp3` (e.g. `gai5.mp3`).

Player (to build once a partial bank exists): split Peng'im into syllable
tokens, fetch `voice-bank/<syl>.mp3` per token, play sequentially with
~40 ms crossfade. Tone sandhi: course notation like `san1(3)` marks the
sandhi tone in parentheses — the player should prefer the parenthesized
(spoken) tone when present.

## Status

- [ ] Course audio: 0/115 recorded (Mandarin espeak placeholders in use)
- [ ] Syllable bank: 0/2215 recorded
