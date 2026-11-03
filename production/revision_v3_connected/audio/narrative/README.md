# Approved-voice opening and under-the-hood narration

Every native stem uses the same approved MiniMax system voice and settings as the user's selected polished American sample: **English_ConfidentWoman, speech-2.8-hd, speed 1.04, pitch -1, volume 1, 44.1 kHz, 128 kbps, mono**. Requests use verified `MINIMAX_KEY_2` and explicit global region. No other voice, per-segment speed setting, speech tempo/pitch processing, old narration, music or sound effects were used.

## Masters

- `insightgen_opening_approved_voice.wav` — exact 14-second mono PCM master.
- `insightgen_underthehood_approved_voice.wav` — exact 70-second mono PCM master.
- Corresponding `.mp3` files are supplied for playback. MP3 encoding adds small container padding; use WAV for exact edit timing.
- `*_raw.mp3` files preserve the nine original TTS outputs for separate editing.

The differentiator naturally lasts 13.322 seconds against its original 12-second window, so business curation starts at 19.442449s and the grounded-skill cue starts at 31.288526s. Later cues recover their planned starts where natural gaps permit them. The complete closing line lasts 4.667211 seconds. The main agent approved starting it at 65.15s, inside the final wide visual from 65–70s; it ends at 69.817211s. No speech was cut or sped up.

`actual_cues.csv` and the separate `audio_actuals` field in `edit/story.json` record actual spoken cue positions while preserving planned visual windows and narration wording. `narrative_manifest.json` records source hashes, natural durations, locked voice fingerprints and master metadata.

## Verification

Both PCM masters fully decode and match exact target durations at 44.1 kHz mono. Each raw stem and playback master also fully decodes.

One MiniMax `asr-1.0` transcription checked all 18 generated native stems (opening, nine demo-v2 paragraphs, eight under-the-hood cues). All **392 normalized words match**. Normalization covers punctuation/hyphen spacing, Insight Gen/InsightGen, C-sixty/C60 and S Q L/SQL. The payload index records exact raw-stem hashes, so changes to silence placement in masters do not alter this speech-content check. Results are in `qc/transcript_comparison.json`; `qc/master_verification.json` contains PCM checks. No listening assessment or owner approval of final delivery is implied by these technical checks.

`generate_narrative.py` resumes only voice/source-attributed stems and rebuilds masters locally. The main-approved closing-start override is explicit. It does not issue repeat synthesis requests for existing verified stems. No full-film synchronization claim is made because the owner-held recording is unavailable.
