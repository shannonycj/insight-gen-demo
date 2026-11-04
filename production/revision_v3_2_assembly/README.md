# InsightGen v3.2 assembly

This handoff uses the original **12-second architectural reveal** at 6–18 seconds
of the **70-second explainer**. Fixed labels explain the handoffs over the original scene footage. The cut uses the approved narration at speed 1.04.

| Order | Material | Duration |
| --- | --- | --- |
| 1 | [Narrated opening](media/01_opening.mp4) | 14 seconds |
| 2 | Your complete re-edited recording with [demo narration](audio/02_demo_narration.wav) | 101.283 seconds when aligned to the narration master |
| 3 | [Narrated v3.2 explainer](media/03_under_the_hood_v3_2.mp4) | 70 seconds |

Use the [demo cue sheet](edit/demo_cues_actual.csv) and the nine stems under
`audio/demo_segments/` to align your recording. Paragraphs 7 and 9 exceed
their original cue windows. Adjust picture holds to preserve the narration.
The opening and explainer already include their narration tracks.

Install FFmpeg and FFprobe on PATH and run from this folder:

```powershell
python assemble_v3_2.py --recording 'D:/path/to/aligned_recording.mp4' --dry-run
python assemble_v3_2.py --recording 'D:/path/to/aligned_recording.mp4'
```

The helper produces a 1280×720, 24 fps MP4, fits and pads the complete recording
frame, and uses the supplied narration for its audio. A shorter recording
requires picture alignment before export. The explicit `--pad-tail` option
extends the final frame after you have checked internal cue alignment.

Estimated runtime with a 101.283-second recording is **3:05.28**. The actual
recording is required to render and review the complete film.
