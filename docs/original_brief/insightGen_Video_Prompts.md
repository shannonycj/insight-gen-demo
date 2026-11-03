# InsightGen on Blue Orbit: "Real Case First, Then Under the Hood" MiniMax Video & Voice Production Guide (v3)

**Audience:** American Express senior leadership
**Purpose:** Lead with a real business case, then explain the enterprise context behind InsightGen and the broader intended Blue Orbit platform scope, beyond a standalone coding agent.
**Structure (fixed; do not reorder, add or remove acts):**
1. ~10s hook
2. Real InsightGen demo on Blue Orbit
3. ~65–70s "under the hood" explainer

**Style:** Energetic premium technology product film; confident, sophisticated, precise
**Status:** Codex master handoff; production prompts and illustrative API examples, not generated media.

---

## 0. Master instructions for Codex

### Available materials

Read this master guide and the two companion text files. Follow this guide for the film structure and cinematic generation.

| Input | Purpose |
|---|---|
| This master guide | Fixed film structure, cinematic scripts, seven visual prompts and editing guidance |
| [insightGen_demo_voiceover.txt](./insightGen_demo_voiceover.txt) | Exact spoken text for the recording's audio track only; its nine paragraphs map to the nine timed segments below |
| [insightGen_demo_narration.md](./insightGen_demo_narration.md) | Timing, pronunciation and context for generating the recording's narration |

**The MP4 is not included because the owner cannot pass it to Codex.** Work from the supplied Markdown and TXT files; the owner will combine the generated cinematic assets and narration with the recording.

The companion scripts are for **audio generation**, not a storyboard for additional AI video. Generating their narration with the same voice as the cinematic sections provides a consistent narrator throughout the final film.

### Production approach

1. Keep the fixed structure: Shot 1 → real recording → shots 2–7, in the stated order.
2. **Generate narration first**: Part A, the demo narration and Part B. Use the same narrator and consistent voice settings across all three (Section 5).
3. Measure the audio and fit picture to it using Section 2's timing plan. Allow natural pauses and adjust cut points within the target lengths; flag any timing issue that cannot be resolved naturally.
4. Generate the seven cinematic shots from Section 4, appending the Section 3 shared style string to each prompt. Narration is supplied separately through TTS; keep any video-model speech out of the final clips. Add readable titles in post-production rather than generating product UI or text.
5. If supported, use generated frames to chain shots 2→7 for continuity. Shot 1 is separate because the recording sits between it and Shot 2.
6. Read `MINIMAX_API_KEY` from the environment; never hard-code or log it. Use the visual prompts for video generation and spoken scripts for TTS, rather than uploading entire source documents. Retain the original confidentiality safeguard: no internal data extracts, screenshots, table names, metric values, SQL, decks or code in external generation requests.
7. **Naming rules:**
   - Our components: Blue Orbit, Enterprise Knowledge Foundation, Skill Foundry, InsightGen (or Insight Generation), Agent Observability Framework (AOF), Harness Intelligence.
   - Third-party tools (Claude Code, Codex) may appear in narration or post-production labels, not video prompts or logos. The current script uses generic wording.
   - Never mention Gleam or any individual's name in generated content.

### Deliverables

- `shot1.mp4` … `shot7.mp4`: 16:9 cinematic clips for the seven shots.
- `vo_partA_hook.mp3`: hook narration.
- `vo_demo_recording.mp3`: demo narration using the companion timing guide. Separate segments named `vo_demo_01.mp3` … `vo_demo_09.mp3` are useful for synchronization.
- `vo_partB_underthehood.mp3`: explainer narration, including the tagline.
- A short summary of the voice settings, actual asset durations and any editing notes. Separate per-shot audio stems are optional if useful for editing.

---

## 1. The story in one line

**Here's a real portfolio investigation in one session. Blue Orbit brings governed knowledge and expert skills to the agent; the broader platform vision adds observability and a validated improvement loop.**

| Act | Content | Target length |
|---|---|---|
| **Act 1: Hook** | Shot 1: the real business question and today's pain | ~10s |
| **Act 2: Demo** | Existing real InsightGen screen recording in Blue Orbit; audio generated separately | ~96s, as documented in the companion narration |
| **Act 3: Under the hood** | Shot 2: why not a drop-in agent → Shot 3: Blue Orbit → Shot 4: EKF → Shot 5: Skill Foundry → Shot 6: AOF → Shot 7: Harness Intelligence + tagline | ~65–70s |

**Why this order:** Leadership sees a concrete result first. The explanation then answers the obvious next question, *"Couldn't an off-the-shelf AI agent do that?"*, and turns InsightGen into the case for the wider platform.

### Differentiation: how we frame drop-in agents

| | Drop-in coding agents (e.g., Claude Code, Codex) | InsightGen on Blue Orbit |
|---|---|---|
| Business definitions | Enterprise definitions and context must be supplied | Governed definitions with provenance (Enterprise Knowledge Foundation) |
| Analytical method | Expert methods must be supplied and maintained | Reusable, auditable expert methods (Skill Foundry design) |
| Evidence | Evidence collection depends on the configured workflow | Linked definitions, SQL and data artifacts described in the demo |
| Governance | Enterprise access controls and review processes require integration | Intended scope: read-only, entitlement-checked access, human checkpoints and auditability |
| Improvement | Observability and improvement workflows require integration | Intended scope: AOF + Harness Intelligence observe, diagnose, validate and improve |

**Scope:** Act 2 is the existing demonstration; Act 3 explains the design and intended wider platform scope. Keep that distinction clear. The companion narration contains the specific editorial notes about the demo, including the current Lumi MCP / temporary BigQuery setup.

**Tone guardrail:** Present coding agents fairly as powerful general-purpose tools that need enterprise context and integration, rather than claiming they fail or score worse. Keep comparisons qualitative unless supporting measurements are available. Analysts remain responsible for decisions.

---

## 2. Voiceover scripts and timing plan

Use the following cinematic scripts and the companion TXT wording for Act 2. Headings, labels, stage directions and Markdown formatting are not spoken text.

### Part A: Hook (before the demo, ~10s)

> Why did a portfolio metric move? Watch InsightGen investigate with governed knowledge and evidence, in one session, on Blue Orbit.

Target: ~10 seconds including a natural ending. "One session" is the workflow framing, not a claim that the full investigation executes in the recording's 96 seconds.

### Act 2: Demo narration (audio only, approximately 96 seconds)

Use the nine paragraphs in the companion TXT verbatim, one per window. The companion Markdown supplies context and guardrails, not additional spoken words. These times are relative to the **start of the recording**, not the start of the final film.

| Suggested segment file | Start | End | Available time |
|---|---|---|---|
| `vo_demo_01.mp3` | 00:00 | 00:12 | 12s |
| `vo_demo_02.mp3` | 00:12 | 00:22 | 10s |
| `vo_demo_03.mp3` | 00:22 | 00:32 | 10s |
| `vo_demo_04.mp3` | 00:32 | 00:46 | 14s |
| `vo_demo_05.mp3` | 00:46 | 00:56 | 10s |
| `vo_demo_06.mp3` | 00:56 | 01:05 | 9s |
| `vo_demo_07.mp3` | 01:05 | 01:18 | 13s |
| `vo_demo_08.mp3` | 01:18 | 01:29 | 11s |
| `vo_demo_09.mp3` | 01:29 | 01:36 | 7s |

Use these timings to assemble the demo audio, leaving pauses where needed. The owner can fine-tune synchronization against the recording during editing.

### Part B: Under the hood (after the demo, ~65–70s)

> General-purpose coding agents are powerful. Enterprise analysis also needs governed definitions, expert methods, and controlled data access. Blue Orbit brings those together for InsightGen, within a broader platform.
>
> **Blue Orbit** is our operating system for enterprise agents: build the foundation once, then specialize it for many kinds of knowledge work.
>
> **Enterprise Knowledge Foundation** gives every agent governed business knowledge: definitions, context and policies, with clear provenance.
>
> **Skill Foundry** turns expert analytical methods into reusable, auditable skills, giving agents a consistent approach while keeping analysts in control of decisions.
>
> The broader platform vision includes the **Agent Observability Framework**: tracing each step, evaluating quality, and helping diagnose issues.
>
> **Harness Intelligence** is designed to close the loop: optimize, validate, and learn, so improvements can support InsightGen and every agent that follows.
>
> **Built once. Specialized many times. Improving continuously.**

The first five paragraphs map to shots 2–6 respectively. The final two paragraphs, including the tagline, belong to shot 7. Use the same narrator as Part A and the demo, whether generating Part B continuously or as per-shot segments.

### Picture and audio budget

| Shot | Act-relative picture window | Target picture duration | Voice |
|---|---|---|---|
| 1 | Act 1, 00:00–00:10 | 10s | Part A |
| 2 | Act 3, 00:00–00:14 | 14s | General-purpose agents / enterprise context |
| 3 | Act 3, 00:14–00:24 | 10s | Blue Orbit |
| 4 | Act 3, 00:24–00:33 | 9s | Enterprise Knowledge Foundation |
| 5 | Act 3, 00:33–00:44 | 11s | Skill Foundry |
| 6 | Act 3, 00:44–00:53 | 9s | Agent Observability Framework |
| 7 | Act 3, 00:53–01:08 | 15s | Harness Intelligence + tagline |

**Act 3 totals 68 seconds**, within the 65–70-second target. These are planning durations; fit the cut points to the generated narration while preserving the shot order and overall length. Shorter speech leaves breathing room. Place the tagline near the end of Shot 7 with a brief closing hold.

**Voice direction:** Use the same narrator across **Part A, the demo and Part B**: energetic, assured and polished US English, with a clear conversational pace. Ask the hook question with curiosity. Keep the comparison respectful; distinguish the wider platform vision from what was just demonstrated. Give a short lift on component names and build to the three-beat close.

---

## 3. Visual system (keep identical across all shots)

**Shared style string (append to every prompt):**
*Deep midnight-navy environment, American Express-inspired electric-blue and cyan illumination, understated warm-gold accents, premium financial-services product-launch film, volumetric lighting, shallow depth of field, precise physically believable motion, 16:9. No readable text, no numbers, no logos, no robots, no people, no watermarks.*

**Recurring motif:** a central **orbit core**, a calm sphere of light with thin concentric orbital rings.
- In Act 3 each component docks into a ring.
- Shot 7 adds the outer improvement ring.
- The final hero shot reads as the complete platform.

**Drop-in agent visual language (Shot 2 only):** a neutral cool-grey pulse representing a general-purpose tool before enterprise context is connected. Show an integration distinction, not a failed answer or a benchmark. Never show a third-party logo or UI.

---

## 4. Shots and generation prompts

### ▶ ACT 1: Hook

#### Shot 1: The question (00:00–00:10, 10s)

**Voice:** Part A.

**Post labels:** THE PORTFOLIO QUESTION → INSIGHTGEN · ONE SESSION

**Prompt:**
Premium cinematic 3D opening. An elegant abstract line chart floats in deep navy space. Its trend line suddenly bends, and a single bright glowing question pulse lifts from the inflection point. For a moment the pulse stalls between several distant, disconnected glass workstations holding scattered documents and data blocks, and the light dims as if time is passing. Then the pulse accelerates decisively toward the camera along a single clean beam of electric-blue light. [Slow push-in, then rapid acceleration] The shot ends by flying into a bright, softly glowing rectangular screen surface that fills the frame with near-white blue light, ready for a dissolve into a real application screen. + shared style string.

### ▶ ACT 2: Real InsightGen demo on Blue Orbit (edit only)

For this act, generate the demo narration from the companion files using the same voice as the cinematic sections. The owner will add it to the existing recording.

**Editing notes:**
- Insert the approximately 96-second recording between shots 1 and 2.
- Dissolve from Shot 1's glow into the recording, and from its ending into Shot 2's abstract report panel. A match cut is an option if the composition works.
- Fine-tune narration placement against the footage. The recording contains execution/result jumps, so its duration is not the full investigation runtime.
- Optional component callouts can highlight what is visible in the demo.
- Review data approval and redact names, workspace paths, internal URLs and unapproved branding before sharing the final video.

### ▶ ACT 3: Under the hood

#### Shot 2: Why not a drop-in agent? (14s)

**Voice:** "General-purpose coding agents are powerful. Enterprise analysis also needs governed definitions, expert methods, and controlled data access. Blue Orbit brings those together for InsightGen, within a broader platform."

**Post labels:**
- Left side: GENERAL-PURPOSE CODING AGENTS: *enterprise context and controls require integration*
- Right side: INSIGHTGEN ON BLUE ORBIT: *governed knowledge · expert skills · cited & governed*

**Prompt:**
Opens on a softly glowing translucent report panel with an abstract chart, centered. The camera pulls back and the frame splits into two parallel lanes.
- **Left lane:** a neutral cool-grey pulse moves smoothly through a clean general-purpose workspace. Separate abstract knowledge nodes, method modules and a protective access shell sit nearby but are not yet connected to its path. Keep the composition calm and capable, with no error symbols, random choices or unstable results.
- **Right lane:** an electric-blue pulse travels a structured path. Fine cyan threads connect it to a knowledge-graph constellation and to glowing skill modules, it draws from a secure data column inside a protective glass shell, and it builds a stable report whose every chart element is linked by warm-gold threads back to its sources.

The left lane gently dims as the right lane brightens and expands to fill the frame. [Slow pullback, then lateral drift to the right lane] Respectful contrast, not dramatic failure. + shared style string.

#### Shot 3: Blue Orbit (10s)

**Voice:** "Blue Orbit is our operating system for enterprise agents: build the foundation once, then specialize it for many kinds of knowledge work."

**Post title:** BLUE ORBIT · *Agent Operating System*

**Prompt:**
The bright right lane resolves into a luminous orbit core with smooth concentric orbital rings rotating slowly and precisely. Beneath it, a layered foundation platform of glowing translucent tiers assembles. From the core, several identical modular pods extend along the rings, then each subtly takes on a different shape and accent color: one shared foundation, specialized into many modules. One pod glows slightly brighter, marking the use case just seen. [Smooth pullback revealing the whole structure] An elegant operating system for intelligent work, not a machine. End on the core with empty docking slots. + shared style string.

#### Shot 4: Enterprise Knowledge Foundation (9s)

**Voice:** "Enterprise Knowledge Foundation gives every agent governed business knowledge: definitions, context and policies, with clear provenance."

**Post label:** ENTERPRISE KNOWLEDGE FOUNDATION

**Prompt:**
Scattered definition fragments fly in and organize into an elegant three-dimensional knowledge-graph constellation of cyan nodes and fine relationship links. Each node carries a tiny warm-gold provenance thread trailing back to a source point. The completed constellation glides along an orbital ring and docks into the first slot of the orbit core, which brightens. [Slow orbit around the constellation, then follow it to the core] Calm, trustworthy, structured. + shared style string.

#### Shot 5: Skill Foundry (11s)

**Voice:** "Skill Foundry turns expert analytical methods into reusable, auditable skills, giving agents a consistent approach while keeping analysts in control of decisions."

**Post label:** SKILL FOUNDRY

**Prompt:**
In a precise luminous workshop space, simple violet-blue geometric blocks represent basic analytical operations. Cyan threads from the knowledge constellation touch each block, which gains detail and becomes a richer component. The components snap together left to right into a complete glowing skill module, which receives a warm-gold approval seal. The module then duplicates into copies that travel along the orbital rings to several different pods. Each copy follows the same visible sequence of method stages while working on differently shaped abstract inputs, representing reusable methodology rather than identical outcomes. [Gentle push-in, then pullback] Craftsmanship, consistency, reuse. + shared style string.

#### Shot 6: Agent Observability Framework (9s)

**Voice:** "The broader platform vision includes the Agent Observability Framework: tracing each step, evaluating quality, and helping diagnose issues."

**Post label:** AGENT OBSERVABILITY FRAMEWORK · INTENDED PLATFORM SCOPE

**Prompt:**
Close on one pod, where a luminous path of four connected stages shows every step of a run leaving a fine glowing trace line. A calm layer of observation light sweeps across the traces, and small elegant signal markers appear along them:
- soft blue markers for activity
- green-cyan markers for quality outcomes
- one amber marker that opens into a branching root-cause view highlighting the step that contributed

[Slow lateral reveal] Analytical, precise, transparent. + shared style string.

#### Shot 7: Harness Intelligence and finale (15s)

**Voice:** "Harness Intelligence is designed to close the loop: optimize, validate, and learn, so improvements can support InsightGen and every agent that follows. Built once. Specialized many times. Improving continuously."

**Post labels:** HARNESS INTELLIGENCE · INTENDED PLATFORM SCOPE; OBSERVE · EVALUATE · DIAGNOSE · OPTIMIZE · VALIDATE · LEARN, then the tagline

**Prompt:**
Pull back to reveal the full orbit core: foundation, knowledge constellation, skill modules and several specialized pods. A wide luminous ring with six evenly spaced nodes forms around the entire structure. Light flows clockwise around the ring, brightening each node in turn:
- A component inside a pod is refined and glows cleaner.
- The refinement passes a warm-gold quality gate.
- A newly learned skill module emerges and travels to every pod.

The loop completes, and the whole platform glows brighter and more organized. [Slow rising crane shot ending in a majestic, stable, centered hero composition with room for a tagline] Continuous improvement, momentum, scale. + shared style string.

---

## 5. Voice generation settings

**One narrator for the entire film:** use the same model, voice ID and consistent delivery settings across Part A, the demo and Part B. If an existing narrator configuration is supplied, reuse it; otherwise select one voice for all three. Adjust pacing naturally to fit the timing windows.

The supplied materials are text, so voice continuity comes from generating all three sections with the same synthesized narrator.

| Setting | Starting value | Reason |
|---|---|---|
| Model | speech-2.8-hd | High-quality narration |
| Voice | English_expressive_narrator (verify availability) | Expressive English starting point |
| Speed | 1.05–1.10 as a starting point | Clear delivery that fits the timing windows |
| Emotion | fluent or happy, only if supported; select once | Energetic without hype |
| Pitch | 0 | Natural authority |
| Output | mp3, 44.1 kHz | Editing-friendly |

**Pronunciation (all acts):** "InsightGen" is spoken as "Insight Jen"; "C-sixty" as "see sixty"; "Lend" as the ordinary word; "SQL" as "S-Q-L". Use the API's pronunciation facility or TTS-only phonetic substitutions while keeping display labels unchanged.

Strip formatting from cinematic scripts and send spoken text only. Check available voices and supported settings, and include the selected configuration and measured audio durations in the handoff summary. Sentence timestamps are useful if available.

**Illustrative request:** verify endpoint, fields, voice and response format against the current account. Substitute the script text and chosen voice settings.

```bash
curl -X POST 'https://api.minimax.io/v1/t2a_v2' \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "speech-2.8-hd",
    "text": "<Part A, demo paragraph, or Part B text>",
    "stream": false,
    "voice_setting": { "voice_id": "English_expressive_narrator", "speed": 1.08, "vol": 1.0 },
    "audio_setting": { "audio_sample_rate": 44100, "format": "mp3" },
    "language_boost": "English"
  }'
```

Decode or download audio according to the API response; it may return encoded audio rather than an MP3 URL. Check playback, pronunciation and duration, and assemble segments with natural pauses where needed.

## 6. MiniMax H3 API (illustrative)

Verify the current model, API schema, duration options and output settings. Use 16:9 output; the example below is a starting point.

```bash
curl -X POST 'https://api.minimax.io/v2/video_generation' \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "MiniMax-H3",
    "content": [ { "type": "text", "text": "<Shot N prompt + shared style string>" } ],
    "duration": 10,
    "resolution": "2K"
  }'
```

**Editorial durations:** S1 = 10s, S2 = 14s, S3 = 10s, S4 = 9s, S5 = 11s, S6 = 9s, S7 = 15s. Shots 2–7 total 68s. Set each request's duration accordingly.

The EKF guide assumed a maximum 15-second generated clip; check the current available durations. Where a target length is unsupported, use a suitable supported length and trim or hold a clean end frame during editing. Report any limitation that prevents the planned timing.

Poll the generation task and download the result when successful; report any generation errors. Check playback, aspect ratio and duration. Expand `+ shared style string` into the actual Section 3 text before submission.

---

## 7. Editing and sound direction

- **Generate all three narration sections first:** hook, demo and under the hood. The owner will combine these with the cinematic clips and recording.
- **Act 1:** the trend line bends on "metric move", and the glow fills the frame on "on Blue Orbit". Dissolve into the app.
- **Out of the demo:** dissolve into Shot 2's abstract report panel, or use a match cut if it works with the footage.
- **Shot 2 sync points:**
  - The lanes split on "General-purpose coding agents".
  - The unconnected context elements are visible on "Enterprise analysis also needs".
  - Knowledge, methods and controlled access become visible in the right lane as they are named.
  - The right lane fills the frame on "Blue Orbit brings those together".
- **Act 3 sync points:**
  - Reveal or highlight each component on its name, using docking only where the shot depicts it.
  - The amber root-cause marker opens on "helping diagnose issues".
  - The improvement ring develops through "optimize, validate, and learn".
  - Validated improvements reach the pods on "every agent that follows".
  - Hold the final hero composition for the three-beat tagline within Shot 7.
- **Third-party names:** the current script uses generic wording. Names, if used, belong in narration or plain post-production text, not generated logos or UI.
- **Sound:**
  - Curious, unresolved pad in the hook, then a rising whoosh into the demo.
  - Music ducked or silent during the demo.
  - A neutral tone for the left lane; a warm, resolved chord for the right lane, without failure/error sounds.
  - A soft "dock" tone per component.
  - A cyclical motif building to the finale.
- **Optional final hierarchy overlay (inside Shot 7's existing hold, not an extra card or extra time):**
  - InsightGen on top.
  - Enterprise Knowledge Foundation · Skill Foundry in the middle.
  - Blue Orbit as the base.
  - AOF · Harness Intelligence as the encircling ring.

---

## 8. Quality-control checklist

- [ ] The order is hook → **real demo** → drop-in comparison → Blue Orbit → Enterprise Knowledge Foundation → Skill Foundry → AOF → Harness Intelligence.
- [ ] Visuals cover the seven cinematic shots; the companion scripts provide the demo's audio.
- [ ] The same narrator and consistent pronunciation are used across the hook, demo and explainer.
- [ ] Demo narration follows the nine source paragraphs and their approximate timing.
- [ ] Part A fits ~10s; Part B, including the tagline, fits 65–70s (planned 68s). Actual durations are reported for editing.
- [ ] The comparison is fair, and the broader platform scope is distinguished from the recorded demonstration.
- [ ] Labels are added in post-production; no generated product UI or third-party logos appear.
- [ ] The original confidentiality and naming safeguards are retained.
- [ ] Audio and video play correctly, cinematic output is 16:9, and there is no competing video-model narration.
- [ ] Any generation or timing issues are reported. Final synchronization with the recording is done during editing.

---

## 9. Source notes

- **Internal positioning references (background only; not included in the Codex handoff and not independently verified here):**
  - InsightGen leadership decks: problem, solution, Knowledge Foundation / Skill Foundry / agentic harness, governance (read-only entitlement-checked queries, human checkpoints, full audit trail)
  - Blue Orbit Knowledge Work Architecture executive deck (AOF, Harness Intelligence)
  - Enterprise Knowledge Foundation MiniMax guide
  - Skill Foundry architecture note
- **MiniMax references:**
  - https://www.minimax.io/blog/minimax-h3
  - https://platform.minimax.io/docs/guides/video-generation
  - https://platform.minimax.io/docs/api-reference/speech-t2a-intro

*MiniMax details are carried over from EKF research dated 27 Oct 2026 and have not been reverified for this handoff. Check current availability, pricing and API schemas against the account before generation.*