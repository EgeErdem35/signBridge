# SignBridge-TR — Turkish Sign Language Accessibility and Communication

> **Senior Project (SE 4910 / SE 4920), October 2026 – June 2027 · Research and development in progress.**
> This README reflects the **SB-18 revised proposal v1.1 r5 (23 October 2026)** as the team's latest *draft*, not yet independently merged or advisor-approved. Features, performance targets, and studies below are **planned**, not claims of completion.

## Project overview

**SignBridge-TR (İşaret Köprüsü)** is a proposed accessible, browser-based progressive web application (PWA) designed to support short, practical conversations between people who use **Turkish Sign Language (TİD)** and those who do not, including accessibility support for people who are blind or have low vision.

The project investigates two complementary directions:

- **Direction A — TİD → Turkish text and speech:** capture camera frames locally; extract hand/body/face landmarks; classify **isolated** signs from a dataset-dependent vocabulary; form limited Turkish text from the gloss sequence; display it and speak it aloud.
- **Direction B — Turkish text or speech → TİD avatar:** transcribe or accept Turkish text; map it to supported sign **glosses** with a language model and documented rules; look up **pre-authored** sign animation clips; show them with a 3D avatar, captions and playback-speed controls. An alphabet-based fingerspelling fallback is proposed for vocabulary gaps.

The app is **not** proposed as unrestricted continuous-sign recognition or a fully generative, linguistically validated sentence-level TİD translator. TİD is a distinct language with its own structure: a gloss-to-clip sequence alone is not proof of natural signing.

## Intended users and scenarios

The proposal addresses Deaf/hard-of-hearing TİD users, TİD-using people with speech impairments, hearing non-signers, and blind/low-vision users communicating with TİD users. Example scenarios include a hospital information desk, a pharmacy, a university conversation, and short everyday exchanges. These are **planned scenarios**, not demonstrations of deployed functionality.

## Planned MVP features

| Area | Planned behavior | Important limitation / status |
|---|---|---|
| Sign → voice | Webcam → on-device MediaPipe landmarks → isolated-sign recognition → gloss → Turkish text/TTS | Dataset-dependent vocabulary; accuracy targets not yet achieved |
| Voice/text → sign | Turkish STT or typed input → gloss selection/rule layer → pre-authored 3D sign clips | Not free-form generation of new movements |
| Two-way mode | Switch between the above in a short conversation | End-to-end behavior remains to be implemented/tested |
| Quick phrases | Reuse predefined and confirmed expressions | Vocabulary and scenarios pending coverage audit |
| Accessibility | Captions, adjustable text, keyboard/screen-reader flow, voice alternatives, spoken camera-framing help | WCAG 2.2 AA is a **target** to test, not achieved compliance |
| Privacy | Raw camera video intended to stay on device; data-flow decisions for audio, text and landmarks documented | External service providers/retention remain undecided |

The four planned interface modes are **Sign → Voice**, **Voice → Sign**, **Two-way Conversation** and **Quick Phrases**.

## Proposed system architecture

```text
Direction A:
Camera → MediaPipe landmarks (in browser)
       → Isolated-sign model → glosses → Turkish language layer
       → Large-print text / text-to-speech

Direction B:
Turkish speech / typed text → speech-to-text (if needed)
       → Turkish-to-TİD gloss mapping (LLM + rules)
       → Approved sign-clip lexicon → 3D avatar playback
       → Captions and playback control

Shared: accessible React/PWA interface; conversation service;
        privacy controls and confirmation/replay interactions.
```

The proposal considers **React/Next.js**, **Python/FastAPI + WebSocket**, **MediaPipe**, **PyTorch**, **ONNX Runtime Web or TensorFlow.js**, **Three.js**, **Blender** and **glTF/GLB**. These are **proposed technologies**, not a declaration that all packages have been installed or production-validated. The [SB-25 avatar research](docs/SB-25-3D-Avatar-Approach-Research.md) (currently under PR review) compares Three.js, Babylon.js and Godot; no final engine or animation-production method is unilaterally locked.

### Dataset and animation are different problems

The intended primary training resource is **AUTSL** (226 sign classes in the original dataset description), with **BosphorusSign22k** as an alternative subject to access and licensing. Per the SB-18 r5 package, access instructions were received and a teammate reported downloading AUTSL; only **sample files were verified**, not the complete dataset integrity. The supplied challenge sample/labels can have a different sample count than the original publication. **Neither recognition class labels nor body-skeleton points are ready-to-play 3D sign animations.**

The **recognition class inventory** and **avatar animation lexicon** are separate. A video-assisted 3D retargeting workflow or manual keyframing must be evaluated for accuracy, licensing and workload. The proposal keeps a target of **at least 300 avatar signs plus the full Turkish fingerspelling alphabet**. This is an **unverified delivery target**, not an already completed library; any modification requires advisor review.

### Potential supplementary recordings — proposed, not approved

SB-18 r5 proposes prioritizing existing permitted datasets. **Only if coverage gaps require it**, supplementary sign recordings may be considered **after advisor agreement, ethics approval, participant consent and data-use arrangements**. This is a **team revision proposal, not an authorization to collect data**. User-study recording arrangements likewise require separate approval.

## Planned verification and evaluation

Key proposal targets are research goals, **not current performance results**. These include dataset-based top-1/top-5 recognition measurements, laptop landmark-processing throughput, speech word error rate, latency, avatar comprehensibility, WCAG 2.2 AA evaluation, and short-scenario usability. The 300-sign library and comprehension targets remain as described in the proposal.

The **SB-18 r5 team draft** changes the earlier fixed participant quotas into a **proposed two-stage evaluation** (simulated-condition preparatory tests, then appropriately recruited target users where possible). **Participant numbers and sampling are not agreed with the advisor yet**; research testing involving people requires ethics approval. No participant study is represented here as already conducted.

## Project structure

The repository is evolving; the paths below refer to existing areas or documented conventions rather than a promised final architecture:

```text
signBridge/
├── README.md                    # This project overview
├── .gitignore                   # Excludes .venv/, Python caches, local artifacts
├── docs/
│   ├── BRANCHING.md             # GitHub Flow and PR/review conventions
│   ├── ETHICS.md                # Ethics planning and consent references
│   ├── MEDIAPIPE_EVAL.md        # MediaPipe feasibility notes
│   ├── literature-review/      # Research bibliography and reports
│   └── SB-25-3D-Avatar-Approach-Research.md
│       # Available on story/SB-25 until its PR is approved and merged
└── ml/
    └── eval/
        └── mediapipe_eval.py   # MediaPipe evaluation experiment
```

The **SB-18 r5 package** separately prepares revised proposal, list-of-changes, feedback matrix, supporting notes and scope companion files for submission under its own Jira issue. They are **not described as merged into `main`** before SB-18 completes its review.

## Project team and advisor

**Advisor:** Kazım Erdoğdu.

**Team:** Kutay Çalışkan · Emir Ersan · Ege Sarp Erdem · Ceren Bilgenoğlu · Barış Hansu · Yasmin Malgir.

## Documentation and project management

- **Jira project:** [SignBridge issues](https://el-dili.atlassian.net/jira/software/projects/SB) — sprint planning, requirements, ownership and review.
- **Confluence space:** [SIGNBRIDGE](https://el-dili.atlassian.net/wiki/spaces/SIGNBRIDGE) — project documentation, meeting notes, sprint records, proposal and SoW.
- **Proposal revision (SB-18):** [Jira SB-18](https://el-dili.atlassian.net/browse/SB-18). The uploaded r5 package is the current working draft pending its own GitHub/Confluence workflow.
- **3D avatar research (SB-25):** [Research report](https://github.com/EgeErdem35/signBridge/blob/story/SB-25/docs/SB-25-3D-Avatar-Approach-Research.md) · [PR #14](https://github.com/EgeErdem35/signBridge/pull/14) · [Confluence page](https://el-dili.atlassian.net/wiki/spaces/SIGNBRIDGE/pages/13172737).
- **Repository strategy:** [Branching and Pull Request Strategy](docs/BRANCHING.md).
- **Ethics:** [Research ethics and consent planning](docs/ETHICS.md).
- **Technical exploration:** [MediaPipe evaluation](docs/MEDIAPIPE_EVAL.md).
- **Literature review:** [Research folder](docs/literature-review/).
- **SB-26 (this README expansion):** [Jira SB-26](https://el-dili.atlassian.net/browse/SB-26).

Documents marked draft, research or review must not be cited as advisor-approved final decisions.

## Contributing and development workflow

Per the **Senior Project Handbook rev2** and [repository policy](docs/BRANCHING.md):

1. Work in a Jira-linked branch matching issue type: `story/SB-123`, `task/SB-123`, or `bug/SB-123`.
2. Commit focused, traceable work to that branch. Do not push directly to `main`.
3. Open a PR referencing the issue and describing scope and verification.
4. Request **at least one independent teammate review** and address feedback.
5. Merge only after approval and required checks; use the project's preferred squash workflow.
6. Keep Confluence and Jira documentation links updated.

## Getting started

This repository is under active development. A stable end-to-end installation or deployment procedure is **not yet documented**, and no setup commands are invented here. Consult the relevant component files and technical documentation before running an experimental script. Dataset access instructions, credentials, copyrighted videos and personal research information must not be committed to Git.

---

**Scope caution:** This README is an accessible overview of the **SB-18 r5 team proposal draft**. Detailed acceptance criteria, measured evidence, ethical approvals, and any advisor-approved scope changes belong to the proposal, Statement of Work and linked research documentation.
