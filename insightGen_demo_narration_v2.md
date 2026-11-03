# InsightGen demo narration

## What this demo shows

InsightGen turns a business question into a governed, evidence-backed analytical investigation inside Blue Orbit. The story is not just automatic chart generation: the user controls access and scope, the agent consults business definitions, and follow-up questions progress from describing a trend to proposing explanations, testing them, and synthesizing the findings.

Source: [record2.mp4](./record2.mp4). Duration: approximately 99 seconds.

## Voice and timing

- Confident, conversational product-demo delivery for a business audience.
- Read "InsightGen" as "Insight Jen"; "C-sixty" as "see sixty"; "Lend" as the ordinary word.
- Generate each timed segment separately for easier synchronization. Leave a short pause at sentence boundaries and adjust clip spacing to the visual transitions.
- The nine paragraphs in the companion [plain-text script](./insightGen_demo_voiceover_v2.txt) match these timed segments in order; it contains only spoken narration for text-to-speech.
- The recording jumps between execution and completed results. Do not imply that the full investigation actually runs in 99 seconds.

## Timed script

### 00:00-00:12 | Set up the analysis

**On screen:** Existing skill descriptions, workspace creation, and session configuration. Lumi MCP and analytical skills are enabled; web tools remain disabled.

**Narration:**

This is InsightGen, the insight generation agent in Blue Orbit. We start by creating a workspace and enabling Lumi MCP and analytical skills.

### 00:12-00:23 | Ask and clarify

**On screen:** The user asks for US SBS dollar C-60 trends comparing 2025 and 2026, separately for Charge and Lend. The clarification form covers methodology, metric scope, and analytical depth.

**Narration:**

We ask for a year-over-year comparison of dollar C-sixty trends for Charge and Lend. Before proceeding, the agent clarifies the methodology, metric, and analytical depth.

### 00:23-00:33 | Ground the analysis

**On screen:** Knowledge-agent activity, governed calculation details, source-table rules, and query execution.

**Narration:**

It consults the governed knowledge bundle for metric definitions, calculation rules, and source tables, before querying the data and running the analysis.

### 00:33-00:47 | Read the initial findings

**On screen:** The trend report, executive summary, a clickable source citation opening the metric definition, and KPI comparison tables.

**Narration:**

The report opens with key findings and a like-for-like comparison. Both products show modest improvement. Linked references open business definitions directly in the governed knowledge bundle.

### 00:47-00:58 | Explore the charts

**On screen:** Monthly trend lines and separate Charge and Lend year-over-year charts, each opened in an enlarged view.

**Narration:**

Interactive previews make the monthly patterns easy to inspect, with separate views for Charge and Lend and clear year-over-year comparisons.

### 00:58-01:07 | Inspect the evidence

**On screen:** Audit artifacts and deliverables, an executed SQL file, and a CSV data preview.

**Narration:**

The supporting SQL, data extracts, and charts are linked alongside the report, so we can inspect the underlying evidence.

### 01:07-01:20 | Move from what to why

**On screen:** The user asks what could explain the improvement, primarily in the second quarter. The agent produces a ranked hypothesis register with mechanisms, expected signals, and proposed tests.

**Narration:**

Next, we ask what might explain the second-quarter improvement. InsightGen ranks candidate hypotheses, spelling out their mechanisms, expected signals, and tests, rather than jumping straight to a conclusion.

### 01:20-01:32 | Test the explanations

**On screen:** "Test the top 2 hypothesis," followed by empirical verdicts, decomposition findings, behavioral evidence, and linked artifacts.

**Narration:**

We ask it to test the top two. The results reject favorable portfolio mix as the explanation and find repayment behavior supportive for Charge, but not Lend.

### 01:32-01:39 | Synthesize for action

**On screen:** Executive summary, key learnings, charts, evidence table, and recommended next steps.

**Narration:**

Finally, InsightGen brings the investigation together: an executive summary, decisive charts, supporting evidence, and recommended next steps.

## Editorial guardrails

- Describe the results as findings reported in this demo, not independently validated business conclusions.
- The narration names Lumi MCP as the configured data source and intended integration. This recording still uses temporary BigQuery tools for execution; Lumi MCP is designed to replace them.
- The diagnostic report attributes improvement mainly to within-segment rate changes, with portfolio mix acting as an unfavorable counter-driver. Repayment evidence is supportive for Charge, not a proven causal explanation for both products.
- Avoid reading detailed figures aloud: the video moves quickly, and the analytical workflow is the central message.