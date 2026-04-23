# Voice Extraction — TDI Biomedical · Session 2 (Continuation)
**Status:** Skeleton v0.3 → target v1.0
**Use:** Paste the CONTEXT BLOCK + SESSION PROMPT into Claude mobile (voice mode). Answer one question at a time.
**What was already captured (Block 1):** May–Aug 2023 · full-time 48 h/sem · $3,500 MXN/week · biomedical metal devices (bone fixation plates, prosthetic components) · first "serious professional" CNC role

---

## PASTE THIS TO START THE SESSION

> Paste everything below the line into Claude mobile as your first message.

---

**[CONTEXT — DO NOT ANSWER YET, JUST READ]**

I'm going to do a voice extraction for my CV. The role is:

- **Company:** TDI — Tecnología & Diseño Industrial, Guadalajara
- **Dates:** May–August 2023, full-time 48 hrs/week
- **What they make:** biomedical metal devices — bone fracture fixation plates, prosthetic metal components
- **Self-note:** This was my first serious professional CNC role — step up from prior work

What we already know is above. What we need to fill in is everything else — machines, materials, daily workflow, what I actually did, and any achievements.

**How I want this to work:**
- Ask me ONE question at a time
- Wait for my answer before moving to the next
- After every 4-5 questions, give me a short recap of what you've heard so far
- At the end, generate the completed role file

Start with Block 2 — Company Context. First question: **How big was the team at TDI? Were you one of a few people on the floor, or part of a large operation?**

---

## QUESTIONS REMAINING (for Claude to work through, one at a time)

### Block 2 — Company Context
- Team size?
- Was TDI a certified medical device manufacturer? (ISO 13485, FDA registered, or just producing for local market?)
- Formal employment contract, or informal by-project?
- Who did you report to directly — supervisor, owner, engineer?
- How did you hear about / get this job?

### Block 3 — Role
- Exact title on your contract (if different from "Operador CNC")?
- What did you spend most of your day doing — operating machines, setup, programming, inspection?
- Did your responsibilities grow over the 3 months?

### Block 4 — Machines
- What CNC machines did you run? (brand/model if you remember — Haas, Mazak, DMG, other?)
- Mill, lathe, or both? Any Swiss-type lathe for screws/pins?
- Did you write or modify G-code, or load existing programs?
- Tool changes, offsets, zeroing — was that your responsibility?

### Block 5 — Daily Workflow
- Walk me through a normal day start to finish.
- How did work orders come to you — traveler sheets, paper drawings, verbal from supervisor?
- Quality inspection — how frequent, who signed off, did you participate?
- If a machine had a problem, what was the process?

### Block 6 — Technical Specifics
- What materials did you machine? (titanium, stainless 316L, other — confirm or correct the inferred list)
- Tolerance ranges you worked to? (general ballpark — ±0.1mm, ±0.01mm, tighter?)
- CAM software used (SolidWorks CAM, Mastercam, other — or just G-code by hand)?
- Drawing standard — GD&T, ISO, or just dimensional drawings?
- Any special handling for biomedical parts after machining? (cleaning, passivation, marking?)

### Block 7 — Achievements
- Was there a difficult part you pulled off that you're proud of?
- Did you catch or prevent a quality problem?
- Informal improvements you made to how things were done?
- Any metrics you remember — scrap rate, parts per shift, cycle time?

### Block 8 — Collaboration
- Did you work alone or on a team?
- Any coordination with engineers or designers?
- Any interaction with clients (hospitals, distributors)?
- Formal documentation — device history records, inspection logs, SOPs?

### Block 9 — Artifacts
- Any photos, drawings, or part samples?
- G-code or SolidWorks files from work done there?
- LinkedIn connections from TDI?
- Any recommendation or reference you could get?

### Block 10 — Closing
- Anything you did that you're not sure how to describe technically?
- Brief exposure to something mentionable that didn't fit above?
- What's the one thing from TDI you're most proud of?

---

## END — RECAP PROMPT

After all blocks, say to Claude:
> *"Recap everything and generate the completed role file for TDI Biomedical"*

Target output:
- ATS-ready title
- Dates, location, employment type confirmed
- Machines + materials confirmed (no more "EXPANSION_SLOT" guesses)
- 3–5 achievement bullets (STAR format where possible)
- Updated CV-ready bullets in Spanish
- Interview defensibility note (2-minute verbal test)
- Updated STRATEGIC NOTE if new info changes the framing

---

*Template: v1.0 — Apr 23, 2026*
*Scope: TDI only — Session 2 continuation from skeleton v0.3*
