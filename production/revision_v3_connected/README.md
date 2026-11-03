# InsightGen v3 — connected business process

This edit uses the distinct visual operations that worked in v2 and connects their outputs to the next component's inputs. It does not use the rejected repeated glass-report world. The edit is built around three acceptance criteria: the enterprise differentiator, an integrated process involving business teams, and meaningful connections between components.

## Production status

Narration is approved and generated. Both real knowledge-to-method and skill-to-run-to-trace handoffs are present, and the complete source edit is conformed. See `edit/video_timeline.csv` for the nine source stages and `edit/semantic_actions.json` for the local business actions and artifact handoffs.

The 14-second opening and 70-second explainer are rendered. Both narrated and silent delivery pairs passed exact frame counts (336/1680), picture durations, 1280×720/24 fps metadata, expected audio-stream counts and full decode. Details and approved source-audio hashes are in `edit/delivery_verification.json` and `docs/VERIFICATION.md`.

Final export names are:

- `insightgen_v3_connected_opening_narrated.mp4` — 14-second portfolio-question opening and agenda.
- `insightgen_v3_connected_underthehood_narrated.mp4` — 70-second connected explanation.
- `insightgen_v3_connected_opening_silent.mp4` and `insightgen_v3_connected_underthehood_silent.mp4` — the same complete visual edits with no audio stream.
- `insightgen_v3_connected_underthehood_clean_silent.mp4` — the conformed picture edit without local captions, moving lineage overlays or narration.

Final delivery is 1280×720, 16:9, 24 fps. The two narrated files map only the newly approved narration masters, with no old narrator, native generated soundtrack, music or speech retiming.

## What makes the story connected

- Business teams select the bookmarked business definition, review its policy context and publish governed knowledge. The same business-team illustration and cursor later initiate an InsightGen question.
- A selected C-60 definition retains its source identity while it leaves Enterprise Knowledge Foundation and grounds the Skill Foundry primitives.
- The comparison, segmentation and test primitives compose into a recognizable skill. The new handoff takes that skill into a run, then derives its AOF execution trace.
- AOF's amber database/query stage becomes the **query-method review** evidence. That same evidence enters Harness diagnosis and is tied to a candidate method change inside the same skill. This is an illustrative quality review, not a claim that the real recording has a verified error.
- Only after validation does the updated skill move into a receiving Skill Foundry library. A copy then reaches a receiving agent workspace, whose input reacts. The sequence shows a completed return path and next use.

Action-led local captions explain responsibilities. V2's documents, knowledge graph, primitives, report workspaces, execution trace and improvement imagery remain distinct. The shared platform is established near the start and revisited at the end.

## Approved voice and recording timing

The approved sample is `production/voice_demo/insightgen_polished_american_demo.mp3`. All new stems use MiniMax `English_ConfidentWoman`, model `speech-2.8-hd`, speed **1.04**, pitch **−1**, volume 1, 44.1 kHz, 128 kbps mono. The source sample, settings hash and voice lock are recorded in `audio/`. All generation uses **MINIMAX_KEY_2**, with no fallback.

The opening and under-the-hood WAV masters are exactly 14 and 70 seconds. Native speech is not sped up or trimmed. The closing begins at 65.15 seconds so its full approved-speed delivery fits before 70 seconds; other actual audio cue times are in `edit/story.json` and `audio/narrative/narrative_cues_actual.csv`.

The owner retains the re-edited recording. Its reference timeline is approximately 99 seconds. At the approved fixed speed, unchanged demo paragraphs 7 and 9 exceed their reference windows, and the complete demo master is **101.283 seconds**. See `audio/demo/` for the unchanged nine stems, WAV/MP3 master and actual cue CSV. The owner must check synchronization and accommodate the two overruns. Do not accelerate individual stems or cut words to force a 99-second recording.

## Local rendering

Requirements: Python, Pillow, Windows Segoe UI/Segoe UI Semibold, and FFmpeg/FFprobe from the sibling `production/tools` installation or system PATH. `render_connected.py` uses local source files and never calls a generation API.

```powershell
python render_connected.py --prepare --stills
python render_connected.py --render
python verify_delivery.py
```

The first command conforms the source excerpts and creates review frames. The second requires both actual generated handoffs and both approved audio masters, then produces the narrated and silent exports. Entire source plates are fit/padded; selected visual source excerpts are used once. Audio is passed unchanged into delivery encoding. The opening has a 0.65-second gentle picture entrance and a 0.35-second picture exit; narration is unaffected.

`assets/` includes v2-derived source frames and extracted definition, skill, query-evidence, library and workspace sprites. `edit/semantic_actions.json` records all added curation, question, evidence and skill-return actions. `edit/typography_audit.json` records checked text bounds. `frames/` contains representative rendered review images. The same three-pictogram skill is copied into the selected report during 39.5–41.3 seconds; its original collection stays in the source scene.

`docs/storyboard_contact.jpg` and `docs/STORYBOARD.md` show the complete actual cut. `docs/TIMED_NARRATION.md` records actual approved-speed speech windows, and `edit/assembly_timeline.csv` marks the recording slot. Rebuild these documents with `python build_handoff_docs.py`.

See `docs/ASSEMBLY.md` for preserving the complete owner-held recording. A complete film cannot be verified here because that recording is unavailable.
