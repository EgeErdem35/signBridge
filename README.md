# SignBridge-TR | İşaret Köprüsü

**Turkish Sign Language (TİD) ↔ Turkish communication and accessibility research**

[Project Proposal](docs/SignBridge-TR_Project_Proposal.pdf) · [Statement of Work](docs/sow/README.md) · [Jira Board](https://el-dili.atlassian.net/jira/software/projects/SB) · [Confluence](https://el-dili.atlassian.net/wiki/spaces/SIGNBRIDGE) · [Contribution & PR Rules](docs/BRANCHING.md)

> **Project status — October 2026:** Senior capstone project (SE 4910 / SE 4920) at Yaşar University, under active research and development. This is a project overview, **not** a claim that an end-to-end translator, trained recognition model, avatar library, production deployment or ethics-approved user study already exists. The latest tracked revised proposal is v1.1 R6; any open scope decisions still require the appropriate team/advisor confirmation.

## Overview

SignBridge-TR explores a browser-based, accessible **progressive web application (PWA)** for short, practical communication between Turkish Sign Language (TİD) users and Turkish speakers. The planned product supports two complementary directions:

| Direction | Planned flow | Main limitation |
|---|---|---|
| **A · TİD → Turkish text / speech** | Camera → on-device MediaPipe landmark extraction → isolated-sign recognition → gloss sequence → constrained Turkish sentence → confirmation/edit → text-to-speech | A selected, dataset-dependent **isolated-sign** vocabulary; not unrestricted continuous TİD translation |
| **B · Turkish text / speech → TİD avatar** | Turkish text or speech-to-text → gloss selection (language model + explicit rules) → prepared animation clips → 3D avatar with captions and replay | A finite, separately authored sign-clip library; not automatically generated fluent TİD |

**Recognition classes and avatar animations are different assets.** Training videos or extracted landmarks do not directly create accurate 3D signing animations. A gloss-to-clip sequence must not be advertised as a linguistically validated natural TİD sentence.

## People and use cases

The proposal considers Deaf/hard-of-hearing TİD users, people who sign due to speech limitations, hearing people who do not know TİD, and accessibility needs involving blind/low-vision users. Illustrative contexts include hospital information desks, pharmacies, university conversations and everyday purchases.

The four proposal personas—**Ayşe, Mehmet, Zeynep and Can**—have documented successful paths in [SoW happy paths](docs/sow/happy-paths.md). For Zeynep, the **MVP-compatible mediated flow** is distinct from the optional **independent blind-user flow (HP-3P)**. Blind-specific additions remain an open scope decision (**D-23**); general keyboard, caption and screen-reader accessibility remains in scope.

> The healthcare examples are research scenarios, **not clinical or medication-advice tools**. Correct understanding is to be evaluated, not assumed.

## Planned MVP experience

1. **Sign → Voice:** Identify supported isolated signs, display glosses and a generated Turkish sentence, then allow **confirmation or editing before speaking**.
2. **Voice → Sign:** Transcribe or accept Turkish text, map supported content to glosses and play prepared avatar clips with captions, replay and speed controls.
3. **Two-way Conversation:** Alternate between the two directions for a short exchange.
4. **Quick Phrases:** Save and replay frequently used expressions, subject to the final storage/privacy design.

Cross-cutting goals include clear text, accessible controls, keyboard/screen-reader navigation, and testing against **WCAG 2.2 AA**. Proposed blind-specific voice commands, spoken framing prompts and delivery cues are **not confirmed MVP commitments**.

## Dataset strategy and realistic scope

- **Primary candidate:** [AUTSL](docs/datasets/SB-16_AUTSL_Access_Request.md), originally described with **226 isolated-sign classes**; [BosphorusSign22k](docs/datasets/tid-dataset-exploration.md) (744 classes) is an alternative for evaluation, subject to access and usage rights.
- An access process for AUTSL was completed and sample decoding/label matching was reported. **Full dataset integrity, label semantics, licensing, signer-independent evaluation and application-specific coverage still require verification.** A matching class name alone does not establish that a particular scenario's intended TİD sign is covered.
- MediaPipe-extracted landmarks, augmentation and signer-independent dataset splits are planned for recognition experiments; live-webcam performance must be evaluated separately.
- Vocabulary and supported scenarios will be finalized after a **coverage audit**. The original **at least 300 avatar signs plus Turkish fingerspelling alphabet** is a **proposed delivery target**, not a completed library. It is separate from AUTSL's 226 recognition classes.
- Supplementary sign recordings are **conditional**, only if gaps justify them and after advisor agreement, required ethics approval, participant consent and data-use arrangements. Existing datasets remain the priority.

See [dataset exploration](docs/datasets/tid-dataset-exploration.md), [MediaPipe feasibility notes](docs/MEDIAPIPE_EVAL.md) and [avatar approach research](docs/SB-25-3D-Avatar-Approach-Research.md).

## Proposed technical architecture

```text
                         Accessible React / PWA interface
                         ┌──────────────────────────────┐
TİD signer → camera ────►│ Browser MediaPipe landmarks │
                         └──────────────┬───────────────┘
                                        ▼
                            Isolated-sign classifier
                                        ▼
                              Gloss → Turkish text
                                        ▼
                               Confirm / edit → TTS

Turkish voice / typed text → STT (if needed) → gloss mapping + rules
                                        ▼
                            Prepared sign-animation library
                                        ▼
                         Browser 3D avatar + captions / replay
```

Technologies investigated or proposed include **React / Next.js, Python / FastAPI, WebSocket, MediaPipe, PyTorch, ONNX Runtime Web / TensorFlow.js, Three.js, Blender and glTF/GLB**. These are **candidates**, not an assertion that each component is implemented.

[SB-25 avatar research](docs/SB-25-3D-Avatar-Approach-Research.md) recommends investigating Three.js rendering with Blender rig preparation; actual animation authoring (manual keyframes versus video-assisted retargeting), correctness and throughput require a pilot. It does **not** represent a finished avatar.

### Data protection

The proposed design processes **raw camera video on the device**, without uploading or storing it in the application. **Landmark sequences may be transferred** if server-assisted classification is selected. Microphone audio, glosses and Turkish text may involve back-end or third-party STT/LLM/TTS services depending on the final architecture. Providers, transfers, retention and legal bases are **not finalized**. Research-session recordings are a separate activity from live application processing.

Read [ETHICS.md](docs/ETHICS.md) and the [Turkish](docs/consent/onam-formu-TR.md) / [English](docs/consent/consent-form-EN.md) draft participant documents. These are for advisor/institutional review; **no ethics approval or participant-ready consent form is claimed**.

## Research and evaluation

Planned evaluation distinguishes:
- **Dataset benchmarks:** signer-independent recognition accuracy and relevant classification baselines.
- **Live system tests:** camera processing throughput, speech recognition, end-to-end response time and avatar playback.
- **Usability/accessibility studies:** task completion, SUS, comprehension and accessibility checks; simulated-condition and target-user groups reported separately.

The proposal includes research targets such as **≥85% top-1**, **≥95% top-5** for recognition on the selected vocabulary, **≥15 fps** browser landmark processing on a mid-range laptop, median latency goals of **≤2.0 s** (end of signing to speech, excluding user confirmation) and **≤2.5 s** (end of speech to avatar onset), **≥80%** task completion and **SUS ≥70**. **These are targets, not measured results.** See the [proposal](docs/SignBridge-TR_Project_Proposal.pdf) for definitions and qualification.

No participant evaluation or new recordings should begin until the required institutional/ethics arrangements and consent are in place.

## Repository map

```text
signBridge/
├── .github/workflows/        # Jira Done gate automation
├── backend/                  # Reserved for backend implementation
├── frontend/                 # Reserved for frontend implementation
├── ml/eval/                  # MediaPipe evaluation scripts
├── docs/
│   ├── SignBridge-TR_Project_Proposal.pdf
│   ├── SB-18_Proposal_List_of_Changes.md
│   ├── SB-8_Project_Proposal_and_Scope.md
│   ├── SB-18_Supporting_Technical_Notes.md
│   ├── BRANCHING.md
│   ├── JIRA_DONE_AUTOMATION.md
│   ├── ETHICS.md
│   ├── consent/              # Draft participant information / consent
│   ├── datasets/             # Dataset access and exploration notes
│   ├── literature-review/    # Review, bibliography and references
│   ├── sow/                  # Statement of Work and happy paths
│   └── SB-25-3D-Avatar-Approach-Research.md
├── .gitignore
└── README.md
```

The `frontend/` and `backend/` folders are **placeholders**, not runnable applications. No unsupported installation or deployment commands are provided. The tracked-file check recorded under [SB-26](https://el-dili.atlassian.net/browse/SB-26) found no committed `.venv/` files on the inspected branch; this is **not** an audit of every historical commit or branch.

## Project documents

| Resource | Purpose |
|---|---|
| [Revised project proposal](docs/SignBridge-TR_Project_Proposal.pdf) | Project goals, limitations, methods and planned targets |
| [Proposal change log](docs/SB-18_Proposal_List_of_Changes.md) | Revisions and open decisions; historical status notes may predate the merged SB-18 issue |
| [Scope companion](docs/SB-8_Project_Proposal_and_Scope.md) | Objectives and functional requirements |
| [SoW index](docs/sow/README.md) and [happy paths](docs/sow/happy-paths.md) | Deliverables, personas, workflows and later use-case work |
| [Literature review](docs/literature-review/SB-13_Literature_Review_SignBridge.md) | Related work |
| [Avatar feasibility research](docs/SB-25-3D-Avatar-Approach-Research.md) | 3D engine, rigging and animation trade-offs |
| [Ethics and consent planning](docs/ETHICS.md) | Participant/data-processing safeguards |
| [Branch / PR policy](docs/BRANCHING.md) | Team contribution rules |
| [Jira Done automation](docs/JIRA_DONE_AUTOMATION.md) | Gate behavior and review protections |

**Collaboration:** [Jira SB project](https://el-dili.atlassian.net/jira/software/projects/SB) · [SIGNBRIDGE Confluence space](https://el-dili.atlassian.net/wiki/spaces/SIGNBRIDGE) · [Statement of Work page](https://el-dili.atlassian.net/wiki/spaces/SIGNBRIDGE/pages/5046283/Statement+of+Work)

## Team and academic advisor

**Advisor:** Dr. Öğr. Üyesi Kazım Erdoğdu

**Team:** Ege Sarp Erdem · Ceren Bilgenoğlu · Emir Ersan · Barış Hansu · Yasmin Malgir · Kutay Çalışkan

## Contribution workflow

Follow the [repository branching strategy](docs/BRANCHING.md) and the course Handbook:

1. Create or select a Jira issue and work in `story/SB-XX`, `task/SB-XX` or `bug/SB-XX`, matching the Jira issue type.
2. Open a focused PR to `main` with the issue key and Jira link; keep documentation and evidence up to date.
3. Obtain an **independent review on the latest commit**, resolve any requested changes and review discussions, and satisfy the required checks.
4. Merge using the protected **squash-and-merge** process. The GitHub Actions workflow then verifies the merged PR and may transition the matching Jira issue to **Done**. Do not bypass checks or assume a PR is ready solely because its structural `gate` is green.

See [SB-30 gate behavior documentation](docs/JIRA_DONE_AUTOMATION.md) for the distinction between structural validation and GitHub's native approval protection.

---

**Scope note:** SignBridge-TR is a research prototype under development. This README deliberately distinguishes **existing documentation and experiments**, **planned deliverables**, **experimental targets**, and **decisions still awaiting confirmation**.
