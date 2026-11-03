# Delivery verification

The narrated and silent opening/explainer exports passed exact picture duration, frame count, dimensions, cadence, expected audio-stream count and complete FFmpeg decode.

| Export | Duration | Frames | Audio streams | Decode |
|---|---:|---:|---:|---|
| insightgen_v3_connected_opening_narrated.mp4 | 14.000s | 336 | 1 | Passed |
| insightgen_v3_connected_opening_silent.mp4 | 14.000s | 336 | 0 | Passed |
| insightgen_v3_connected_underthehood_narrated.mp4 | 70.000s | 1680 | 1 | Passed |
| insightgen_v3_connected_underthehood_silent.mp4 | 70.000s | 1680 | 0 | Passed |

All exports are 1280×720, 24 fps. Narrated exports contain one 44.1 kHz mono AAC stream sourced only from the approved new voice masters. Silent exports contain no audio stream. Source-master hashes are in `edit/delivery_verification.json`.

Text bounds passed across the complete rendered film. Nineteen representative explainer stills and three opening stills are available for visual review. Both real generated handoffs are present; no missing-source placeholder is used.

The owner-held recording is unavailable. Its complete UI framing, internal action/narration alignment and final joins remain unverified. The unchanged demo master lasts 101.283 seconds at the approved fixed speed, exceeding the 99-second reference slot. A final subjective listening review of delivery, pronunciation and sentence endings is still required before sharing.
