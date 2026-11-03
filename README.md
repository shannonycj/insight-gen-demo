# InsightGen demo v3 — final assembly handoff

The approved connected v3 opening, explainer, narration and editable sources are in
[`production/revision_v3_connected/`](production/revision_v3_connected/).
The owner's re-edited screen recording must be supplied locally.

## Assemble in this order

| Part | Current approved file | Duration |
| --- | --- | --- |
| Opening with narration | [Opening MP4](production/revision_v3_connected/insightgen_v3_connected_opening_narrated.mp4) | 14 seconds |
| Owner's full recording | Supply your re-edited recording | Align to demo narration |
| Audio for the recording | [Demo WAV](production/revision_v3_connected/audio/demo/insightgen_demo_v2_approved_voice.wav) / [MP3](production/revision_v3_connected/audio/demo/insightgen_demo_v2_approved_voice.mp3) | 101.283 seconds |
| Under the hood with narration | [Explainer MP4](production/revision_v3_connected/insightgen_v3_connected_underthehood_narrated.mp4) | 70 seconds |

The opening and explainer already contain narration. Do not layer their standalone
audio on top of the embedded audio. All 18 new narration stems use the approved
polished American voice at speed **1.04**, pitch **−1**. No speech is accelerated
or trimmed. Final assembly requires no API credentials or generation account.

The unchanged demo script was timed against a roughly 99-second recording.
Paragraphs 7 and 9 exceed their reference windows at the approved speed; align the
real recording to the supplied [actual demo cues](production/revision_v3_connected/audio/demo/demo_cues_actual.csv).
With a 101.283-second recording slot, the total film is about **3:05.28**.
The recording's actual internal synchronization and final listening review remain
unverified. Preserve the complete UI through proportional scaling and navy padding;
do not crop or cover controls.

## Assembly helper

Install FFmpeg/FFprobe on PATH, then run from the repository root:

```powershell
python production/revision_v3_connected/assemble_connected.py --recording 'D:/path/to/aligned_recording.mp4' --dry-run
python production/revision_v3_connected/assemble_connected.py --recording 'D:/path/to/aligned_recording.mp4'
```

The helper preserves the full recording frame and approved speech speed. It refuses
to cut narration when the recording is too short. See [assembly instructions](production/revision_v3_connected/docs/ASSEMBLY.md)
before using its explicit tail-padding option; tail padding does not fix internal cue alignment.

## Editing and verification materials

- [Full production README](production/revision_v3_connected/README.md), including silent exports and rebuild commands.
- [Storyboard](production/revision_v3_connected/docs/STORYBOARD.md), [contact sheet](production/revision_v3_connected/docs/storyboard_contact.jpg), and [timed narration](production/revision_v3_connected/docs/TIMED_NARRATION.md).
- [Assembly timeline](production/revision_v3_connected/edit/assembly_timeline.csv), [visual timeline](production/revision_v3_connected/edit/video_timeline.csv), and all audio stems under `production/revision_v3_connected/audio/`.
- Editable overlays, extracted visual assets, two new animated handoffs, renderer and exact v2 source dependencies.
- [Technical QC](production/revision_v3_connected/qc/verification.json) and [sampled visual review](production/revision_v3_connected/qc/semantic_review.json).

Opening and explainer are 1280×720, 24 fps. Duration, full decode, approved-master
audio identity and voice continuity checks passed; automated transcription matched
all 392 normalized script words. `SHA256SUMS.txt` covers the v3 payload and current entry documents. Legacy v2
checksums are preserved in `docs/V2_SHA256SUMS.txt`.

## Previous version

The older root `media/`, `audio/`, and `edit/` folders are the **v2 handoff** and
remain for reference. Use the v3 paths above for the new final film. The original
v2 handoff README is preserved at [docs/V2_HANDOFF_README.md](docs/V2_HANDOFF_README.md).

The original verified v3 ZIP is stored locally in `.handoff/`; it is omitted from
Git to avoid duplicating all the unpacked media. No credentials, local tool binaries
or rejected v3 revisions are included.
