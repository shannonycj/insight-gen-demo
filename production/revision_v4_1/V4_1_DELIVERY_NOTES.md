# InsightGen v4.1 delivery

The narrated opening runs 34.000 seconds. The explainer runs 121.417 seconds. The projected assembly is 239.454 seconds using the 83.167-second reference demo and a 0.870-second hold for `demo_07d`. Cue positions for the demo are provisional until the local picture edit.

## Local assembly

1. Place the opening, the owner-edited recording and the explainer in that order. The ten demo WAVs are in `audio/demo/`.
2. Replace explainer frames **2016–2433 inclusive** with the Galileo recording. The zero-based slot starts at **84.000 s** and runs **418 frames**. Use the existing narration over the insert. The silent explainer and separate narration WAV contain the same edit.
3. Overlay `galileo_lower_third.png` for the first three seconds of Galileo. Check the span selection against `aof_02`, then confirm the final runtime and cue alignment against the actual footage.

## Edit and review

- The cut retains the full data, knowledge-search and Skill Foundry sequences at their original playback speed. This moves the Galileo slot to 84.000 seconds.
- H3 returned slightly longer clips than requested. The extra frames were removed at low-motion points while retaining the conditioned endpoints. The opening joins the actual clean chart close-up at v3.2 opening 4.0 seconds. Readable generated axis labels in that transition were masked in post.
- The reused AOF plates carry an updated caption, “Every run is traced.” The second plate points to the query-method review and Harness Intelligence.
- The data chart includes small stylized tick marks and a blue trace outline before the separate silver web trace arrives. The Skill Foundry shot shows the guard ring and contracts. The edge-case deflection is subtle.
- All nine H3 tasks succeeded on their first submission using `MINIMAX_KEY_2`. The delivery JSON records the task IDs, exact edit timings and stem hashes. The four reused MP3s are byte-identical to their v3.2 sources.
- FFmpeg verifies the Galileo slot as 418 identical frames. Limited-range BT.709 H.264 decoding yields `#061423`, one green-channel step from the requested `#061323`.
- Speech recognition checked the 21 new stems as one speaker and rendered Lumi phonetically as “Loomi.” Listening for delivery and pronunciation and checking cue alignment against the owner-held screen recordings remain open.

## Pronunciation retakes

`opening_01` introduces a “portfolio risk analyst” who monitors “key portfolio metrics,” including the “dollar current to sixty rate.” The revised cue transcribed as scripted and fits the original 34-second opening. The title and caption match the analyst and metrics wording. `aof_01` uses the American-English pronunciation of Galileo, with stress on “lay.” Both exports passed full decode. Listening confirmation remains open.
