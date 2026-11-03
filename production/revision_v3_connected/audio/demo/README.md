# Approved-voice demo narration

Nine stems preserve the nine paragraphs in `insightGen_demo_voiceover_v2.txt` unchanged. Every synthesis request uses the same approved settings: **English_ConfidentWoman / speech-2.8-hd / speed 1.04 / pitch -1 / volume 1**, 44.1 kHz, 128 kbps, mono. `voice_lock.json` in the parent folder records the approved sample hash and fixed settings. The saved CLI credential was locally compared with `MINIMAX_KEY_2`; requests use that key, with no fallback. Explicit `--region global` avoids the CLI attempting a protected config write.

## Deliverables

- `demo_01.mp3` through `demo_09.mp3`: original-speed narration stems; no words trimmed and no tempo/pitch processing.
- `insightgen_demo_v2_approved_voice.wav`: edit-ready mono PCM master, approximately 101.283 seconds.
- `insightgen_demo_v2_approved_voice.mp3`: matching playback master; MP3 container padding makes the encoded file slightly longer.
- `demo_cues_actual.csv`: nominal windows and actual safe placements.
- `demo_manifest.json`: source hashes, settings fingerprints, natural durations and master hashes.
- `audio_verification.json`: executed settings/format/full-decode checks and level measurements. No listening assessment is claimed.

## Recording synchronization requires review

At the fixed approved speed, paragraph 7 naturally lasts **14.237 seconds** against its nominal 13-second window, and paragraph 9 lasts **9.183 seconds** against its nominal 7-second window. No additional TTS takes were requested to force a faster delivery.

The master retains nominal starts wherever possible, then shifts later speech enough to avoid overlap: paragraph 8 starts at approximately **81.357s** instead of 80s, and paragraph 9 starts at approximately **92.100s** instead of 92s. Its last spoken segment ends around **101.283s**. All speech is preserved at the approved speed. The owner's unavailable recording cannot be asserted to match these placements.

Use the individual stems to align the real recording; extend or re-edit visual holds if needed. Do not speed up these two stems or cut their words to force the original 99-second target.

`python generate_demo.py` resumes verified stems from the manifest and rebuilds the masters locally. It only sends a new synthesis request for a missing stem whose voice/source fingerprint matches. No music, sound effects or previous narration are mixed in.
