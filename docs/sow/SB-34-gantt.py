"""SB-34 single source of dates.

Generates docs/sow/SB-34.md (Schedule of Deliverables text and tables) and
docs/sow/SB-34-gantt.svg (Figure 1) from the same data, so that the chart and
the document always show the same dates.

Usage: python3 SB-34-gantt.py <output-dir>
"""
from datetime import date, timedelta
import html
import os
import sys

STATUS_DATE = date(2026, 11, 11)

# ------------------------------------------------------------------ calendar
SPRINTS = [  # name, start, end, source
    ("Sprint 1", date(2026, 10, 5), date(2026, 10, 18), "Jira (closed)"),
    ("Sprint 2", date(2026, 10, 19), date(2026, 11, 1), "Jira (closed)"),
    ("Sprint 3", date(2026, 11, 2), date(2026, 11, 15), "Jira (active)"),
    ("Sprint 4", date(2026, 11, 16), date(2026, 11, 29), "Official course timeline; not yet created in Jira"),
    ("Sprint 5", date(2026, 11, 30), date(2026, 12, 13), "Official course timeline; not yet created in Jira"),
    ("Sprint 6", date(2026, 12, 14), date(2026, 12, 27), "Official course timeline; not yet created in Jira"),
]
WEEK0 = date(2026, 9, 21)          # first column of the chart (course initiation week)
NWEEKS = 14                        # 21 Sep - 27 Dec 2026
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]  # SE 4920, 2027

S = {n: (s, e) for n, s, e, _ in SPRINTS}
def W(s, e): return ("w", s, e)                 # dated SE 4910 period
def M(i, j): return ("m", i, j)                 # SE 4920 months, 0 = Jan 2027
def SP(a, b=None): return W(S[a][0], S[b or a][1])

DONE, PROG, PLAN = "done", "progress", "planned"

# --------------------------------------------------------------- deliverables
# id, group, name, segments [(period, status)], sprint label, evidence, related SB-24 §4.6 criteria
D = [
 ("D1", "Project management and SoW", "Team initiation; Jira, Confluence and GitHub set-up",
  [(SP("Sprint 1"), DONE)], "Sprint 1",
  "SB-10, SB-11: Jira Done 17 Oct 2026", "—"),
 ("D2", "Project management and SoW", "Project proposal v1.0 and literature review",
  [(SP("Sprint 1"), DONE)], "Sprint 1",
  "SB-8, SB-13: Jira Done 17 Oct 2026; SB-8 merged in PR #10 (17 Oct 2026). Submission evidence: Table 3", "—"),
 ("D3", "Project management and SoW", "Revised proposal v1.1 (R6) and list of changes",
  [(SP("Sprint 2"), DONE)], "Sprint 2",
  "SB-18: Jira Done 24 Oct 2026; R6 merged in PR #16 (24 Oct 2026) and is the current version on main. Submission evidence: Table 3", "—"),
 ("D4", "Project management and SoW", "SoW: happy paths, scope of work, use cases, acceptance criteria",
  [(SP("Sprint 2"), DONE)], "Sprint 2",
  "SB-23 (PR #22), SB-24 (PR #29): Jira Done", "1–17 (defined)"),
 ("D5", "Project management and SoW", "SoW: introduction, verification mapping, special requirements",
  [(W(date(2026, 11, 2), date(2026, 11, 11)), DONE)], "Sprint 3",
  "SB-33 (PR #30), SB-38 (PR #35), SB-41 (PR #38): Jira Done 10–11 Nov 2026", "1–17 (verification methods)"),
 ("D6", "Project management and SoW", "SoW: schedule, economic, ethics, literature, references",
  [(W(date(2026, 11, 2), date(2026, 11, 12)), PROG)], "Sprint 3",
  "SB-34, SB-35, SB-37, SB-42, SB-43: Jira In Progress on 11 Nov 2026", "—"),
 ("D7", "Project management and SoW", "SoW assembly and final check (SB-39)",
  [(W(date(2026, 11, 11), date(2026, 11, 13)), PROG)], "Sprint 3",
  "SB-39: Jira In Progress on 11 Nov 2026 (preparation status). The submission itself is milestone M4 and has not happened yet", "—"),
 ("D8", "Research and feasibility", "Dataset exploration, AUTSL access, lexicon schema, MediaPipe check",
  [(W(date(2026, 10, 5), date(2026, 11, 1)), DONE)], "Sprints 1–2",
  "SB-12, SB-14, SB-15, SB-16: Jira Done", "1, 7 (inputs)"),
 ("D9", "Research and feasibility", "Avatar approach research and playback pilot",
  [(W(date(2026, 10, 19), date(2026, 11, 10)), DONE)], "Sprints 2–3",
  "SB-25: Jira Done; SB-40: PR #32, Jira Done 10 Nov 2026", "4, 13 (inputs)"),
 ("D10", "Research and feasibility", "Post-SoW feasibility work: coverage audit, landmarks, device benchmark",
  [(SP("Sprint 4"), PLAN)], "Sprint 4",
  "Proposal R6 Table 6 (Oct–Nov) and Methods 1 (a)–(f); the remaining checks continue after the SoW. Separate from the pre-SoW review M6", "1, 7"),
 ("D11", "Research and feasibility", "Ethics: drafts, BTTO consultation, committee application",
  [(W(date(2026, 10, 5), date(2026, 10, 25)), DONE), (W(date(2026, 11, 2), date(2026, 11, 15)), PROG), (SP("Sprint 4"), PLAN)],
  "Sprints 1–4",
  "SB-9, SB-19: Jira Done; SB-36: Jira In Progress; application per proposal R6 Table 6", "10"),
 ("D12", "Research and feasibility", "Ethics committee review (expected 2–3 months)",
  [(SP("Sprint 5", "Sprint 6"), PLAN), (M(0, 0), PLAN)], "Sprints 5–6, Jan 2027",
  "Proposal R6 Table 6 (Nov–Jan) and Methods 6; the end shown is an estimate, not an approval date", "10"),
 ("D13", "Product build (planned)", "User research and interface prototypes",
  [(SP("Sprint 4", "Sprint 6"), PLAN)], "Sprints 4–6",
  "Proposal R6 Table 6 (Nov–Dec)", "8, 11, 12"),
 ("D14", "Product build (planned)", "Dataset audit, MVP recognition vocabulary and lexicon",
  [(SP("Sprint 4", "Sprint 6"), PLAN), (M(0, 0), PLAN)], "Sprints 4–6, Jan 2027",
  "Proposal R6 Table 6 (Nov–Jan); deliverable 5. Also supplies lexicon entries as an input to the avatar library (D16); the 300-sign target belongs to D16", "1, 10"),
 ("D15", "Product build (planned)", "Recognition model v1 → v2",
  [(SP("Sprint 5", "Sprint 6"), PLAN), (M(0, 1), PLAN)], "Sprints 5–6, Jan–Feb 2027",
  "Proposal R6 Table 6 (Dec–Feb); deliverable 2", "1, 5, 7"),
 ("D16", "Product build (planned)", "Avatar rig and animation library (≥300 signs + fingerspelling)",
  [(SP("Sprint 5", "Sprint 6"), PLAN), (M(0, 2), PLAN)], "Sprints 5–6, Jan–Mar 2027",
  "Proposal R6 Table 6 (Dec–Mar); deliverable 3. The ≥300-sign + Turkish fingerspelling target is verified under SB-24 §4.6 criterion 4. Input: lexicon entries from D14", "4, 6, 13"),
 ("D17", "Product build (planned)", "Speech, LLM and TTS pipeline; back-end",
  [(SP("Sprint 5", "Sprint 6"), PLAN), (M(0, 1), PLAN)], "Sprints 5–6, Jan–Feb 2027",
  "Proposal R6 Table 6 (Dec–Feb); deliverable 4", "2, 3, 5, 6, 10"),
 ("D18", "Product build (planned)", "Front-end and accessibility layer",
  [(M(0, 2), PLAN)], "Jan–Mar 2027",
  "Proposal R6 Table 6 (Jan–Mar); deliverable 1", "8, 9, 11, 12, 13"),
 ("D19", "Evaluation and closure (planned)", "MVP integration and internal testing",
  [(M(2, 3), PLAN)], "Mar–Apr 2027",
  "Proposal R6 Table 6 (Mar–Apr); deliverables 1, 7", "1–13"),
 ("D20", "Evaluation and closure (planned)", "WCAG audit, pre-tests, target-user evaluation",
  [(M(3, 4), PLAN)], "Apr–May 2027",
  "Proposal R6 Table 6 (Apr–May); deliverables 7, 8", "11, 14, 15, 16 (17 if D-23 approved)"),
 ("D21", "Evaluation and closure (planned)", "Post-implementation report, demo video, poster, presentation",
  [(M(4, 5), PLAN)], "May–Jun 2027",
  "Proposal R6 Table 6 (May–Jun); deliverable 9. Official SE 4920 dates to be confirmed", "Reports evidence for 1–17"),
]

# ----------------------------------------------------------------- milestones
# id, label, date text, kind, source, chart: ("date", d) | ("before", d) | ("monthend", i) | None
MS = [
 ("M1", "Team initiation and project-management configuration due", "2 Oct 2026", "official", "Official course timeline", ("date", date(2026, 10, 2))),
 ("M2", "Project proposal due", "9 Oct 2026", "official", "Official course timeline", ("date", date(2026, 10, 9))),
 ("M3", "Revised project proposal due", "23 Oct 2026", "official", "Official course timeline", ("date", date(2026, 10, 23))),
 ("M4", "Statement of Work due (planned submission; not yet submitted)", "13 Nov 2026", "official", "Official course timeline", ("date", date(2026, 11, 13))),
 ("M5", "Sprint 3 ends", "15 Nov 2026", "sprint", "Jira sprint SB Sprint 3", ("date", date(2026, 11, 16))),
 ("M6", "Advisor review point 1 before the SoW. Potential inputs, subject to availability at the time: D8, D9. Date and scope unverified",
  "Before SoW submission — exact date and completion unverified", "review", "Proposal R6 Methods 7", ("before", date(2026, 11, 13))),
 ("M7", "Advisor review point 2 (baseline and model accuracy)", "End of Jan 2027 (planned)", "review", "Proposal R6 Methods 7", ("monthend", 0)),
 ("M8", "SE 4920 final submission and demo day", "To be confirmed", "tbc", "No official SE 4920 calendar available", None),
]

# Intermediate outputs that start the next phase (used for dependency arrows).
# id, label, source deliverable, position ("w", date) or ("m", month boundary index), target deliverables, conditional
I = [
 ("I1", "MVP vocabulary and scenarios fixed after the coverage audit", "D10", ("w", date(2026, 11, 30)), ["D15", "D16"], False),
 ("I2", "Recognition model v2 and speech/LLM/TTS back-end ready for integration", "D15, D17", ("m", 2), ["D19"], False),
 ("I3", "Integrated MVP build frozen for the WCAG audit and, once G1 is in place, the pre-tests", "D19", ("m", 3), ["D20"], False),
 ("I4", "WCAG audit report and other available evidence (test and benchmark reports); starts report drafting", "D20", ("m", 4), ["D21"], False),
 ("I5", "Participant test results (pre-tests and, if held, target-user stage): a later input, only if obtained after G1 and written consent; otherwise reported as not measured", "D20", ("m", 5), ["D21"], True),
]
EXTRA_ARROWS = [("D7", "D10"), ("D11", "D12"), ("D17", "D19")]   # finish-to-start
GATE = ("G1", "Ethics approval obtained — date to be confirmed", "D20")   # required before any participant test

# ======================================================================= text
def fmt(d): return f"{d.day} {d.strftime('%b')} {d.year}"

def period_text(segs):
    mixed = len({st for _, st in segs}) > 1
    tag = {DONE: " (completed)", PROG: " (in progress)", PLAN: " (planned)"}
    out = []
    for p, st in segs:
        if p[0] == "w":
            t = f"{fmt(p[1])} – {fmt(p[2])}"
        else:
            a, b = MONTHS[p[1]], MONTHS[p[2]]
            t = f"{a} 2027" if a == b else f"{a}–{b} 2027"
        out.append(t + (tag[st] if mixed else ""))
    return "; ".join(out)

def status_text(segs):
    sts = {s for _, s in segs}
    if sts == {DONE}: return "Completed"
    if sts == {PLAN}: return "Planned"
    if sts == {PROG}: return "In progress"
    return "Partly completed; in progress"

KIND = {"official": "Official course deadline", "sprint": "Jira sprint boundary",
        "review": "Advisor review point", "tbc": "To be confirmed"}

def tables():
    cal = ["| Sprint | Dates | Date source |", "|---|---|---|"]
    for n, s, e, src in SPRINTS:
        cal.append(f"| {n} | {fmt(s)} – {fmt(e)} | {src} |")
    cal.append("| SE 4920 (spring) | Jan – Jun 2027, by month | Sprint calendar to be confirmed |")
    ms = ["| ID | Milestone | Date | Type | Source |", "|---|---|---|---|---|"]
    for i, l, dt, k, src, _ in MS:
        ms.append(f"| {i} | {l} | {dt} | {KIND[k]} | {src} |")
    sub = ["| Item | Official deadline | Jira record | Submission to the course system | Delivery to the advisor |",
           "|---|---|---|---|---|",
           "| Project proposal v1.0 | 9 Oct 2026 (M2) | SB-8 Done 17 Oct 2026; PR #10 merged 17 Oct 2026 | Not verified: no access to the course-system record | Not verified |",
           "| Revised proposal v1.1 and list of changes | 23 Oct 2026 (M3) | SB-18 Done 24 Oct 2026; R6 merged in PR #16 on 24 Oct 2026. R6 is the current version in the repository (`docs/SignBridge-TR_Project_Proposal.pdf`) | Not verified: no access to the course-system record | Not verified |",
           "| Statement of Work | 13 Nov 2026 (M4) | SB-39 (assembly and final check) In Progress on 11 Nov 2026 | Not yet submitted; planned for 13 Nov 2026 | Not yet delivered |"]
    sch = ["| ID | Deliverable | Planned period | Sprint | Status (11 Nov 2026) | Evidence / source | Related acceptance criteria (SB-24 §4.6) |",
           "|---|---|---|---|---|---|---|"]
    for i, g, n, segs, sp, ev, ac in D:
        sch.append(f"| {i} | {n} | {period_text(segs)} | {sp} | {status_text(segs)} | {ev} | {ac} |")
    io = ["| ID | Intermediate output | Produced by | Expected | Starts |", "|---|---|---|---|---|"]
    for i, l, src, pos, tgts, cond in I:
        when = fmt(pos[1] - timedelta(days=1)) if pos[0] == "w" else f"End of {MONTHS[pos[1]-1]} 2027"
        if cond:
            when += " at the earliest; conditional on G1 and consent"
        io.append(f"| {i} | {l} | {src} | {when} | {', '.join(tgts)} |")
    io.append(f"| {GATE[0]} | {GATE[1]} | D11–D12 (ethics committee) | To be confirmed; the end of D12 is only an estimate of the review period | Participant tests in {GATE[2]} |")
    return "\n".join(cal), "\n".join(ms), "\n".join(sub), "\n".join(sch), "\n".join(io)

def markdown():
    cal, ms, sub, sch, io = tables()
    return f"""# SB-34: Schedule of Deliverables and Sprint-Aligned Gantt Chart

- **Project:** SignBridge-TR
- **Owner:** Yasmin Malgir
- **Jira:** [SB-34](https://el-dili.atlassian.net/browse/SB-34)
- **Status:** Draft for peer review. Item status recorded on {fmt(STATUS_DATE)}.
- **Date sources:** Jira sprints (board 3); official course *Timeline of Events* (SE 4910, Fall 2026); Project Proposal v1.1 R6, the current version in this repository (Table 6 and Methods 1, 6 and 7); SB-24 §4.6, the acceptance verification mapping merged through SB-38 (PR #35).

The section below supplies the original SoW template heading **Schedule of Deliverables**. The integration notes at the end are editorial material and are not part of the SoW text.

## Schedule of Deliverables

This schedule lists what SignBridge-TR will deliver and when. It follows the course template: deliverables are aligned with the two-week Scrum sprints of SE 4910 and with the project work plan for SE 4920. The deliverables come from the Scope of Work and from Expected Outcomes/Deliverables 1–9 of proposal R6. Each deliverable is linked to the acceptance criteria that will verify it. These criteria are defined in Acceptance Criteria §4.6. The tables and Figure 1 are generated from the same date list, so every date in this section appears unchanged in the chart.

**Sprint calendar.** SE 4910 runs six two-week sprints. Sprints 1–3 use the dates recorded in Jira. Sprints 4–6 follow the official course timeline and will be created in Jira at the corresponding sprint planning meetings. The SE 4920 sprint calendar has not been published yet, so spring work is planned by month.

*Table 1 – Sprint calendar*

{cal}

**Milestones.** Official course deadlines, Jira sprint boundaries and advisor review points are listed separately. The Statement of Work is due on 13 November 2026, two days before Sprint 3 ends in Jira on 15 November 2026. Proposal R6 places advisor review point 1 (M6) before the Statement of Work. Its exact date has not been recorded, and whether it took place has not been verified. For this reason it is not shown as a dated milestone.

**Pre-SoW review (M6) and post-SoW feasibility work (D10).** These are two separate items. M6 is the advisor review planned before the SoW. Potential inputs, subject to availability at the time, are the dataset exploration and AUTSL access, the MediaPipe feasibility check and the lexicon schema (D8), and the avatar approach research and playback pilot (D9). The date of the review and its scope remain unverified. Proposal R6 Methods 7 also lists the scenario coverage, the avatar method and its effort for the 300-sign library, the recording decision and the O4 fallback for this review. The sources inspected do not confirm which of these findings, if any, were actually presented to the advisor. In particular, the repository still marks the scenario coverage audit as pending (`docs/sow/happy-paths.md`), and no advisor record of the recording decision or of the O4 fallback was found. D10 is the feasibility work planned for Sprint 4, after the SoW submission. It completes the remaining checks of Methods 1 (a)–(f), including the full scenario coverage audit and the device benchmark. Its output, I1, fixes the MVP vocabulary and scenarios. No official SE 4920 submission or demonstration date is available yet. The chart therefore shows the planned final-report work up to June 2027, without a fixed deadline marker.

*Table 2 – Milestones*

{ms}

**Submission evidence.** Official deadlines, Jira closure dates and the actual submissions are kept apart. A Jira resolution date records when the team closed the issue. It does not prove that the document was submitted to the course system or delivered to the advisor, and neither of those has been verified.

*Table 3 – Proposal and SoW submission evidence*

{sub}

**Deliverables.** Completed items are supported by verified Jira records (status *Done* and resolution date) and, where applicable, by pull requests merged into `main`. Items in progress reflect their Jira status on {fmt(STATUS_DATE)}. Planned items take their periods from Table 6 of proposal R6 and are mapped to the sprints that cover those months. They are plans, not completed work. The last column uses the criterion numbers of Acceptance Criteria §4.6. Every planned result remains *not measured / not verified* until the corresponding check has been run.

*Table 4 – Schedule of deliverables*

{sch}

**Dependencies, intermediate outputs and reviews.** Several phases in Table 6 of the proposal overlap by month. Where they do, the next phase starts when a named intermediate output is ready, not when the whole previous phase has ended (Table 5).

*Table 5 – Intermediate outputs that start the next phase, and conditional later inputs*

{io}

- The SoW sections (D5, D6) feed the assembly and final check of the document (D7, SB-39). The team reviews the SoW jointly before submission, and every section is merged only after an independent teammate's pull-request approval. The planned submission is milestone M4.
- The post-SoW feasibility work (D10) runs in Sprint 4, after the SoW submission and separately from the pre-SoW review M6. Its output, I1, fixes the MVP vocabulary and scenarios and starts training the recognition model (D15) and producing the avatar library (D16). D14 continues in parallel: it refines the MVP recognition vocabulary and the lexicon for D15, and supplies lexicon entries to D16 as an input. The ≥300-sign avatar-library target belongs to D16 and is verified under criterion 4.
- The ethics committee application (D11) is followed by the committee review (D12). The end of D12 is only the proposal's estimate of the review period. Participant testing in D20 is gated by G1, the actual ethics approval, together with written, explicit consent (criterion 10). No participant test, including simulated pre-tests, begins before G1.
- I2 starts MVP integration (D19). The avatar library (D16) and the front-end (D18) continue to deliver into integration until the end of March. I3 starts the WCAG audit in D20; the participant pre-tests in D20 also need G1. I4, the WCAG audit report and other available evidence, starts the drafting of the post-implementation report (D21). Participant test results (I5) are a conditional later input. They exist only if the pre-tests or the target-user stage run after G1 and written consent. Otherwise the report states those measures as not measured.
- Advisor review point 2, planned for the end of January 2027, assesses the baseline and the model accuracy. If it is not met, the scope is narrowed with the advisor; no target is changed by this schedule.
- Each sprint ends with a sprint review with the advisor, who acts as Product Owner, followed by a retrospective and sprint planning. These reviews are where the schedule is checked and adjusted.

**Figure 1 – Sprint-aligned Gantt chart of deliverables (status on {fmt(STATUS_DATE)}).**

![Figure 1 – SignBridge-TR sprint-aligned Gantt chart](SB-34-gantt.png)

*Solid green bars: completed work verified in Jira/GitHub. Hatched bars: work in progress. Dashed bars: planned work from proposal R6 Table 6. Diamonds: official course deadlines (red), the Jira end of Sprint 3 (dark blue) and a planned advisor review point (purple). Circles: intermediate outputs (I1–I4); the dashed circle and arrow mark I5, a conditional later input. Grey gate: ethics approval, date to be confirmed. Advisor review point 1 is shown only as "before SoW submission", and the SE 4920 final deadline is not shown because its date has not been confirmed. An editable vector version is provided as `SB-34-gantt.svg`.*

**Items to be confirmed.** The following have no accessible source yet:

- the SE 4920 sprint calendar and official SE 4920 deadlines (post-implementation report, demo day, poster and presentation; M8);
- the date of advisor review point 1, whether it took place, and which preliminary findings were reviewed (M6);
- the actual submission of the proposal, the revised proposal and the SoW to the course system, and their delivery to the advisor (Table 3);
- the ethics committee submission date and the actual approval date (G1), which depend on the BTTO / Project Support Office guidance (SB-36);
- the creation of Sprints 4–6 in Jira with the course-timeline dates shown above.

---

### Integration and Review Notes — not part of the SoW section

- Copy the section under the existing **Schedule of Deliverables** heading of the Confluence page *Statement of Work* (https://el-dili.atlassian.net/wiki/spaces/SIGNBRIDGE/pages/5046283/Statement+of+Work). Do not add or reorder template headings. Upload `SB-34-gantt.png` as Figure 1.
- `SB-34-gantt.py` is the single source for every date and table in this file and in the chart. If a date changes, edit the script and regenerate both outputs.
- AC-5 in the Jira description names `task/SB-34`. The branch rule that currently applies, `docs/BRANCHING.md` (updated by SB-45, PR #34), requires the exact issue key. This work is therefore committed on branch `SB-34`.
- Statuses are a snapshot of {fmt(STATUS_DATE)}. Before the SoW is submitted, recheck D6, D7 and Table 3 against Jira and update them if their status has changed.
- Peer approval, applicable checks, merge and the final SoW/Confluence evidence updates are still pending. Do not mark SB-34 Done on the basis of this draft.
"""

# ====================================================================== chart
LBL_W, ID_W = 430, 46
WK, MO, GAP = 44, 92, 18
X0 = ID_W + LBL_W
XW_END = X0 + NWEEKS * WK
XM0 = XW_END + GAP
XM_END = XM0 + 6 * MO
TOP, ROW, GROUP_H = 172, 26, 24

def xw(d): return X0 + (d - WEEK0).days / 7 * WK
def xm(i): return XM0 + i * MO
def seg_x(p): return (xw(p[1]), xw(p[2] + timedelta(days=1))) if p[0] == "w" else (xm(p[1]), xm(p[2] + 1))
def pos_x(p): return xw(p[1]) if p[0] == "w" else xm(p[1])

def svg():
    e = html.escape
    rows, groups, y, last = [], [], TOP, None
    for d in D:
        if d[1] != last:
            groups.append((d[1], y)); y += GROUP_H; last = d[1]
        rows.append((d, y)); y += ROW
    bottom = y
    H, Wd = y + 190, XM_END + 20
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {H}" width="{Wd}" height="{H}" font-family="Arial, Helvetica, sans-serif" font-size="12">',
         '<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#f3c88a"/><line x1="0" y1="0" x2="0" y2="6" stroke="#c77700" stroke-width="2.5"/></pattern>'
         '<marker id="arr" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#444"/></marker>'
         '<marker id="arrp" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#6a1b9a"/></marker></defs>',
         f'<rect width="{Wd}" height="{H}" fill="#ffffff"/>',
         '<text x="10" y="24" font-size="17" font-weight="bold" fill="#111">SignBridge-TR — Schedule of Deliverables (sprint-aligned Gantt chart)</text>',
         f'<text x="10" y="43" font-size="11.5" fill="#444">Status as of {fmt(STATUS_DATE)}. SE 4910 by week and sprint; SE 4920 by month (sprint calendar to be confirmed). Generated from the same date list as Tables 1–5.</text>']
    hy = 62
    o.append(f'<text x="{X0 + NWEEKS*WK/2}" y="{hy-4}" text-anchor="middle" font-weight="bold" fill="#222">SE 4910 — Fall 2026</text>')
    o.append(f'<text x="{(XM0+XM_END)/2}" y="{hy-4}" text-anchor="middle" font-weight="bold" fill="#222">SE 4920 — Spring 2027 (dates TBC)</text>')
    o.append(f'<rect x="{xw(WEEK0)}" y="{hy}" width="{xw(date(2026,10,5))-xw(WEEK0)}" height="22" fill="#eceff3" stroke="#fff"/>')
    o.append(f'<text x="{(xw(WEEK0)+xw(date(2026,10,5)))/2}" y="{hy+15}" text-anchor="middle" font-size="11" fill="#333">Initiation</text>')
    for n, s, ex, src in SPRINTS:
        x1, x2 = xw(s), xw(ex + timedelta(days=1))
        jira = src.startswith("Jira")
        o.append(f'<rect x="{x1}" y="{hy}" width="{x2-x1}" height="22" fill="{"#d7e3f4" if jira else "#e9eef6"}" stroke="#fff"/>')
        o.append(f'<text x="{(x1+x2)/2}" y="{hy+15}" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#1d3557">{n}{"" if jira else "*"}</text>')
    for i in range(NWEEKS):
        d = WEEK0 + timedelta(weeks=i)
        o.append(f'<text x="{X0+i*WK+WK/2}" y="{hy+37}" text-anchor="middle" font-size="10" fill="#555">{d.day}.{d.month:02d}</text>')
    o.append(f'<text x="{ID_W}" y="{hy+37}" font-size="10.5" fill="#555">Week starting</text>')
    for i, m in enumerate(MONTHS):
        o.append(f'<rect x="{xm(i)}" y="{hy}" width="{MO}" height="22" fill="#eef0f2" stroke="#fff"/>')
        o.append(f'<text x="{xm(i)+MO/2}" y="{hy+15}" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#333">{m} 2027</text>')
    # grid
    for i in range(NWEEKS + 1):
        o.append(f'<line x1="{X0+i*WK}" y1="{TOP-6}" x2="{X0+i*WK}" y2="{bottom}" stroke="#e3e6ea"/>')
    for n, s, ex, src in SPRINTS + [("end", date(2026, 12, 28), None, "")]:
        o.append(f'<line x1="{xw(s)}" y1="{hy}" x2="{xw(s)}" y2="{bottom}" stroke="#9fb3cc" stroke-width="1.2"/>')
    for i in range(7):
        o.append(f'<line x1="{xm(i)}" y1="{TOP-6}" x2="{xm(i)}" y2="{bottom}" stroke="#e3e6ea"/>')
    o.append(f'<rect x="{XW_END+2}" y="{hy}" width="{GAP-4}" height="{bottom-hy}" fill="#f6f6f6"/>')
    # milestones
    MY = TOP - 30
    col = {"official": "#c62828", "sprint": "#1d3557", "review": "#6a1b9a", "tbc": "#888"}
    lab_off = {"M4": ("end", -8), "M5": ("start", 8)}
    for i, l, dt, k, src, ch in MS:
        if ch is None:
            continue
        if ch[0] == "before":
            x = xw(ch[1])
            x0 = xw(date(2026, 10, 26))
            o.append(f'<line x1="{x-2}" y1="{MY-30}" x2="{x0}" y2="{MY-30}" stroke="#6a1b9a" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#arrp)"/>')
            o.append(f'<text x="{x0-4}" y="{MY-26}" text-anchor="end" font-size="10" font-weight="bold" fill="#6a1b9a">M6: advisor review before SoW submission — potential inputs, subject to availability; date and scope unverified</text>')
            continue
        x = xw(ch[1]) if ch[0] == "date" else xm(ch[1] + 1) - 4
        dash = '' if k == "official" else ' stroke-dasharray="5 3"'
        o.append(f'<line x1="{x}" y1="{MY}" x2="{x}" y2="{bottom}" stroke="{col[k]}" stroke-width="1.6"{dash}/>')
        o.append(f'<path d="M{x},{MY-10} l6,6 l-6,6 l-6,-6 z" fill="{col[k]}"/>')
        anc, dx = lab_off.get(i, ("middle", 0))
        o.append(f'<text x="{x+dx}" y="{MY-13 if anc == "middle" else MY-1}" text-anchor="{anc}" font-size="10" font-weight="bold" fill="{col[k]}">{i}</text>')
    # groups and rows
    for g, gy in groups:
        o.append(f'<rect x="4" y="{gy}" width="{XM_END-4}" height="{GROUP_H-2}" fill="#f4f6f8" opacity="0.92"/>')
        o.append(f'<text x="10" y="{gy+16}" font-weight="bold" fill="#1d3557">{e(g)}</text>')
    box = {}
    for (d, ry) in rows:
        i, g, n, segs, sp, ev, ac = d
        o.append(f'<text x="10" y="{ry+17}" font-size="11" fill="#666">{i}</text>')
        o.append(f'<text x="{ID_W}" y="{ry+17}" fill="#111">{e(n)}</text>')
        xs = []
        for p, st in segs:
            x1, x2 = seg_x(p)
            if st == DONE:
                o.append(f'<rect x="{x1+1}" y="{ry+5}" width="{x2-x1-2}" height="16" rx="3" fill="#2e7d32"/>')
            elif st == PROG:
                o.append(f'<rect x="{x1+1}" y="{ry+5}" width="{x2-x1-2}" height="16" rx="3" fill="url(#hatch)" stroke="#c77700"/>')
            else:
                o.append(f'<rect x="{x1+1}" y="{ry+5}" width="{x2-x1-2}" height="16" rx="3" fill="#dbe7f6" stroke="#4a6fa5" stroke-dasharray="4 2"/>')
            xs += [x1, x2]
        box[i] = (min(xs), max(xs), ry)
        if all(st == DONE for _, st in segs):
            o.append(f'<text x="{max(xs)+4}" y="{ry+17}" font-size="12" fill="#2e7d32" font-weight="bold">✓</text>')
    # arrows
    def arrow(x1, y1, x2, ry2, colr="#444", mk="arr", dash=""):
        top = ry2 + 5
        if abs(x2 - x1) < 3:
            p = f"M{x1},{y1} V{top-1}"
        else:
            p = f"M{x1},{y1} H{x1+6} V{ry2+13} H{x2-1}"
        o.append(f'<path d="{p}" fill="none" stroke="{colr}" stroke-width="1.2" marker-end="url(#{mk})"{dash}/>')
    for a, b in EXTRA_ARROWS:
        arrow(box[a][1], box[a][2] + 13, box[b][0], box[b][2])
    for iid, lab, src, p, tgts, cond in I:
        x = xw(p[1]) if p[0] == "w" else xm(p[1])
        if cond:
            x -= 10   # drawn just inside the end of the source bar
        sy = box[src.split(",")[0]][2] + 13
        dash = ' stroke-dasharray="4 3"' if cond else ""
        for t in tgts:
            arrow(x, sy + 6, x, box[t][2], colr="#777" if cond else "#444", dash=dash)
        o.append(f'<circle cx="{x}" cy="{sy}" r="5" fill="#fff" stroke="{"#777" if cond else "#444"}" stroke-width="1.6"{dash}/>')
        o.append(f'<text x="{x-7}" y="{sy-6}" text-anchor="end" font-size="9.5" font-weight="bold" fill="#333">{iid}</text>')
    # ethics gate
    gx, gy = box["D20"][0] - 14, box["D20"][2] + 13
    d12x, d12y = box["D12"][1], box["D12"][2] + 13
    o.append(f'<path d="M{d12x},{d12y} H{d12x+8} V{gy} H{gx-9}" fill="none" stroke="#777" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#arr)"/>')
    o.append(f'<rect x="{gx-8}" y="{gy-8}" width="16" height="16" fill="#9e9e9e" transform="rotate(45 {gx} {gy})"/>')
    o.append(f'<text x="{gx}" y="{gy+4}" text-anchor="middle" font-size="9" font-weight="bold" fill="#fff">G</text>')
    o.append(f'<text x="{d12x+12}" y="{d12y-9}" font-size="9.5" fill="#555">est. end of review — not an approval date</text>')
    o.append(f'<text x="{gx-12}" y="{gy-11}" text-anchor="end" font-size="9.5" font-weight="bold" fill="#555">G1 ethics approval (date TBC)</text>')
    # status date
    tx = xw(STATUS_DATE)
    o.append(f'<line x1="{tx}" y1="{hy+22}" x2="{tx}" y2="{bottom}" stroke="#ff8f00" stroke-width="2"/>')
    o.append(f'<text x="{tx+3}" y="{bottom+14}" font-size="10.5" fill="#e65100" font-weight="bold">Status date {STATUS_DATE.day} Nov</text>')
    # final-report end note (no fixed deadline)
    o.append(f'<text x="{XM_END-2}" y="{bottom+14}" text-anchor="end" font-size="10" fill="#666">SE 4920 final submission / demo day: date to be confirmed (no marker)</text>')
    # legend
    ly, lx = bottom + 38, 10
    def leg(shape, text, w):
        nonlocal lx
        o.append(shape.format(x=lx, y=ly)); o.append(f'<text x="{lx+34}" y="{ly+12}" font-size="11.5" fill="#222">{e(text)}</text>'); lx += w
    leg('<rect x="{x}" y="{y}" width="28" height="14" rx="3" fill="#2e7d32"/>', "Completed (Jira Done / merged PR)", 240)
    leg('<rect x="{x}" y="{y}" width="28" height="14" rx="3" fill="url(#hatch)" stroke="#c77700"/>', "In progress (Jira)", 145)
    leg('<rect x="{x}" y="{y}" width="28" height="14" rx="3" fill="#dbe7f6" stroke="#4a6fa5" stroke-dasharray="4 2"/>', "Planned (proposal R6 Table 6)", 230)
    leg('<path d="M{x},{y} m14,0 l7,7 l-7,7 l-7,-7 z" fill="#c62828"/>', "Official course deadline", 180)
    leg('<path d="M{x},{y} m14,0 l7,7 l-7,7 l-7,-7 z" fill="#1d3557"/>', "Jira sprint end", 135)
    leg('<path d="M{x},{y} m14,0 l7,7 l-7,7 l-7,-7 z" fill="#6a1b9a"/>', "Advisor review point (planned)", 225)
    leg('<circle cx="{x}" cy="{y}" r="5" transform="translate(14 7)" fill="#fff" stroke="#444" stroke-width="1.6"/>', "Intermediate output", 160)
    leg('<circle cx="{x}" cy="{y}" r="5" transform="translate(14 7)" fill="#fff" stroke="#777" stroke-width="1.6" stroke-dasharray="4 3"/>', "Conditional input", 150)
    leg('<rect x="{x}" y="{y}" width="12" height="12" transform="translate(8 1)" fill="#9e9e9e"/>', "Gate (date TBC)", 130)
    notes = [
        "* Sprints 4–6 follow the official course timeline and are not yet created in Jira.  Arrows run from an intermediate output (circle) or from the end of a phase to the start of the next phase.",
        "M1 Team initiation due 2 Oct 2026   M2 Proposal due 9 Oct 2026   M3 Revised proposal due 23 Oct 2026   M4 SoW due 13 Nov 2026 (planned submission)   M5 Sprint 3 ends 15 Nov 2026   M7 Advisor review point 2, end of Jan 2027 (planned)",
        "I1 MVP vocabulary and scenarios fixed   I2 Model v2 and speech back-end ready for integration   I3 Integrated MVP build frozen for audit (pre-tests also need G1)   I4 WCAG report and available evidence start report drafting   I5 Participant results: conditional later input (G1 + consent)",
    ]
    for k, t in enumerate(notes):
        o.append(f'<text x="10" y="{ly+40+k*18}" font-size="10.5" fill="#333">{e(t)}</text>')
    o.append('</svg>')
    return "\n".join(o)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    with open(os.path.join(out, "SB-34.md"), "w", encoding="utf-8") as f:
        f.write(markdown())
    with open(os.path.join(out, "SB-34-gantt.svg"), "w", encoding="utf-8") as f:
        f.write(svg())
    print("written SB-34.md and SB-34-gantt.svg")
