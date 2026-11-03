# Assembly and voice continuity

The owner-held recording sits between the 14-second opening and 70-second under-the-hood export. Both supplied exports use the approved voice, at the same synthesis speed and pitch. Use the supplied demo stems/master for the recording, not an earlier voice or narrator.

## Preserve the complete recording

Fit the entire source proportionally inside 1280×720 and center-pad in navy. Do not crop, stretch, mask UI edges, or place titles over controls. Keep its actual runtime. Convert cadence to 24 fps without changing its playback speed.

```text
scale=1280:720:force_original_aspect_ratio=decrease:force_divisible_by=2:reset_sar=1,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x061323,setsar=1,fps=24
```

## Fixed-speed audio takes priority

The unchanged demo narration at the approved voice/speed lasts 101.283 seconds. Paragraphs 7 and 9 overrun the reference windows; actual cue placement is recorded in `audio/demo/demo_cues_actual.csv`. Check those transitions against the real recording before final assembly. The source narration v2 remains unchanged.

The assembly helper refuses to silently cut words or accelerate narration. If the supplied recording is shorter than the demo master, first align/extend the appropriate recording holds in the editor. The optional `--pad-tail` switch deliberately extends only the last video frame; it does not solve internal cue alignment and should be used only after checking the earlier cue transitions.

```powershell
python assemble_connected.py --recording 'D:/path/to/record2.mp4' --dry-run
python assemble_connected.py --recording 'D:/path/to/aligned_recording.mp4'
```

When the recording is longer than the demo master, the helper pads narration silence to preserve the full video. Original recording audio is omitted. Approved opening and explainer audio is retained. No voice tempo/pitch processing is performed.

## Review before sharing

Check all nine demo action/narration cues, complete UI framing, joins into/out of the recording, last spoken words, and opening/closing holds. Rebase global cue times to the actual recording duration. The source recording, its readability after scaling, full-film synchronization and final listening review remain unverified here.
