# InsightGen v3.2 recreation bundle

Give this folder to a video producer or another AI agent as the source of truth for a fresh cut. Match the story, approved voice and editorial constraints. Recreate the imagery as needed for the available tools and footage.

1. Start with [RECREATE_V3_2.md](RECREATE_V3_2.md). It is written as a handoff prompt you can paste directly into a new session.
2. Supply [NARRATION.md](NARRATION.md) and [narration_cues.json](narration_cues.json). The JSON separates spoken text, picture timing, actual speech placement and visual intent. Send only `spoken_text` to speech synthesis. The three files in `narration/` also contain clean spoken copy.
3. Include [VOICE.md](VOICE.md), the [approved voice sample](references/approved_voice.mp3) and the [visual reference sheet](references/v3_2_visual_reference.jpg). Use the visuals as references for composition, motion and clarity.
4. Supply the owner’s re-edited screen recording and apply the [feedback and acceptance checks](FEEDBACK_AND_ACCEPTANCE.md). Check the nine demo cues against the actual screen actions before assembling the final film.

The intended order is a 14-second opening, the re-edited recording, and a 70-second explainer. The approved demo narration runs 101.283 seconds, which gives an assembled reference runtime of about 3:05.28. The owner provides the recording separately.

The approved exports, demo narration and assembly helper are available in the [v3.2 GitHub handoff](https://github.com/shannonycj/insight-gen-demo/tree/bca5943315c37f4d259fe782d04f0caef6ec9c7b/production/revision_v3_2_assembly). Prefer those audio masters when you have access. The instructions here also support a fresh render.
