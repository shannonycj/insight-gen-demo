# InsightGen demo v2 — final editing handoff

This folder contains the latest opening, refined under-the-hood explainer, and narration for the owner's screen recording. The complete recording must be added by the owner.

## Assemble in this order

| Part | File | Duration |
| --- | --- | --- |
| Opening, with titles and narration | [media/01_opening.mp4](media/01_opening.mp4) | 10 seconds |
| Owner's complete recording | Add `media/02_recording.mp4` | Align to the demo narration |
| Demo narration | [audio/02_demo_narration.mp3](audio/02_demo_narration.mp3) | 96 seconds |
| Under the hood, with titles and narration | [media/03_under_the_hood.mp4](media/03_under_the_hood.mp4) | Approximately 68 seconds |

The nominal full edit is 2 minutes 54 seconds. The opening and explainer already contain narration; do not add their MP3 tracks on top of the embedded audio. Mute recording audio where it competes with the demo narration.

## Editable assets

- `audio/`: standalone opening, demo and explainer narration.
- `audio/demo_segments/`: nine timed demo narration segments for aligning the recording.
- `audio/explainer_segments/`: current narration stems for shots 2–7.
- `edit/narrated_shots/`: seven individual clips with titles and narration.
- `edit/clean_shots/`: silent footage without the locally added titles, for re-editing.
- `edit/overlays/` and `edit/title_cues.json`: title graphics and their timing within each shot.
- `edit/timeline.csv`: shot and narration timing, relative to each part.
- `docs/asset_manifest.json`: current delivery settings and revised narration.
- `docs/original_brief/`: historical scripts and brief. The latest media and revised narration take precedence where the original brief differs.
- `SHA256SUMS.txt`: integrity hashes for this handoff.

## Current revision

Skill Foundry shows reusable analytical primitives grounded by Enterprise Knowledge Foundation and composed into governed, explainable skills. AOF supplies execution evidence to Harness Intelligence, which diagnoses, optimizes and validates improvements across the platform and feeds successful patterns into reusable skills.

Shots 5–7 contain the latest component refinement. This handoff excludes obsolete takes, reference recordings, API credentials, and local generation tools. Final editing requires no MiniMax account or API key.

See [the final editing notes](docs/FINAL_EDIT_HANDOFF.md) before assembling the recording. Media files are included directly in the repository; this copy does not commit or push them.
