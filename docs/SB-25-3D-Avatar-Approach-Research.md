# SB-25 — 3D Avatar Approach Research

**Project:** SignBridge-TR · **Issue:** [SB-25](https://el-dili.atlassian.net/browse/SB-25) · **Sprint:** 2  
**Type:** Comparative technical research and feasibility assessment — **no implementation included**  
**Status:** Research recommendation, subject to advisor review and future pilot validation  
**Baseline:** SignBridge-TR Project Proposal v1.1 (October 2026); Senior Project Handbook rev2.

> **Executive decision:** Recommend **Three.js for web rendering** and **Blender for rig preparation**, while comparing Babylon.js and Godot. Investigate **manual keyframing versus video-assisted landmark retargeting** as production strategies; neither is demonstrated in this issue. Retain the proposal's **at least 300 signs plus fingerspelling** target until a feasibility pilot and advisor decision. Do not label preliminary estimates as measured results.

## 1. Purpose, scope and research questions

The proposed SignBridge-TR browser-based PWA has two directions: (A) camera-based isolated TİD signs to Turkish text/speech; (B) Turkish text/speech to a *prepared* library of TİD animation clips played by a 3D avatar. The project proposal explicitly excludes fully generative avatar motion as the initial method. Recognition vocabulary and avatar clip vocabulary are **separate**. The proposal also excludes continuous signing and sentence-level TİD translation from the recognition MVP; the avatar's planned sequence playback does **not** prove natural connected TİD.

This issue asks which browser engine displays signs, how accurate signs could be produced offline, whether 300 clips can be completed, and what evidence is missing. **No avatar, pipeline, benchmarks or user tests are claimed to have been built.** The research is intended to inform the Statement of Work review before **13 November 2026**.

Questions: (1) Which of three candidate renderers best fits React/PWA? (2) Which authoring workflow could produce correct handshape, location, movement, orientation and non-manual features? (3) What data and rights are available? (4) How much work might each sign require? (5) What must a future pilot demonstrate?

## 2. What the technology terms actually mean

- **Avatar/mesh:** the on-screen humanoid's visible geometry, not the motions themselves.
- **Rig/skeleton:** connected virtual bones; fine finger bones and controllable face are essential prerequisites.
- **Skinning:** deforms geometry as the rig moves.
- **Keyframe animation:** an artist sets important poses and times; software interpolates intermediate frames. Quality depends on correct poses and timing.
- **Inverse kinematics (IK):** derives plausible joint angles for a hand/limb target. It does not itself understand TİD.
- **Morph targets / blendshapes:** stored facial mesh deformations (e.g. eyebrow or mouth states); their availability depends on the model and format.
- **Landmarks:** estimated points from recorded images. 2D/3D keypoints are *not* rig bone rotations, and a depth estimate is not guaranteed accurate.
- **Retargeting:** maps recorded motion to a different rig, handling coordinate frames, limb proportions, joint constraints and missing data.
- **glTF 2.0 / GLB:** interoperable 3D asset specification and binary packaging. They can carry skeletal and morph-target animations but do not encode the linguistic correctness of signs.
- **Rendering engine:** loads and displays prepared motion. It does not create verified signs out of ordinary text.
- **Gloss:** a label identifying a sign in the planned lexicon; not a complete grammatical translation.

TİD signs may depend on **handshape, palm orientation, position, movement, timing and non-manual cues** (face/head/body). Rendering a smooth hand wave is not proof of a correct sign. A visual demo and comprehension test provide different evidence.

## 3. Rendering alternatives — comparable criteria

The following describes documented capabilities and project-specific architectural judgments, **not experimental rankings**.

| Criterion | Three.js | Babylon.js | Godot Engine |
|---|---|---|---|
| Category | Browser-oriented JS 3D library | Browser-oriented JS/TS 3D engine | Full standalone engine with web export |
| Browser delivery | Embedded directly in web UI | Embedded directly in web UI | Export WebAssembly/web application and bridge to host UI |
| Fit to React/PWA | Strong; direct JS composition | Strong; engine/scene lifecycle needs integration | More integration and deployment work for existing React architecture |
| Rigged hand/body animation | Imported skeletal clips; depends on rig | Imported skeletal clips; depends on rig | Skeleton/animation capabilities; depends on rig |
| Facial movement | Morph targets/skinning supported by appropriate assets | Morph targets/skinning with suitable assets | Blend shapes/animation with suitable assets |
| glTF/GLB | GLTFLoader glTF 2.0 | glTF loader/import workflow | glTF 2.0 asset import/export workflows |
| Core cost/license | No software fee; MIT | No software fee; Apache-2.0 | No software fee; MIT |
| Sign animation generation built in? | **No** | **No** | **No** |
| SignBridge-specific risk | Custom playback and transition logic | Added engine surface/complexity | Web export/browser requirements and React integration |

**Three.js.** A JavaScript library with GLTFLoader and animation playback (AnimationMixer). React application state can choose a gloss, resolve its verified asset and play/transition clips. Suitable when the 3D element is one feature in a web PWA. Challenges: managing memory, clip mixing, skeletal conventions, responsive performance and non-manual animation. Source: [R1–R3].

**Babylon.js.** A browser 3D engine with animation groups, skeleton and morph-target tools and glTF support. A credible competing web solution, potentially useful for a more demanding 3D scene. It still requires offline sign-asset production and a React lifecycle adapter. Source: [R4–R5].

**Godot.** An integrated open-source game engine with 3D skeletal animation and glTF workflows. Its web-exported application is not as directly integrated into a React PWA as a JS rendering library; actual deployment constraints must be tested on target devices. It remains technically capable; the fit assessment is an engineering judgment, not a claim that its animations are less accurate. Source: [R6–R7].

**License caution.** Engine licenses do not confer rights to commercial characters, motion files, reference videos, downloaded models or derived assets. Verify each separately; the use of a dataset for academic analysis does not automatically authorize public distribution of transformed animation clips.

### Preliminary recommendation

**Three.js** is the first renderer to prototype because the proposal already specifies Three.js/Blender and a React-based PWA. **Babylon.js** is a meaningful fallback and should be tested with the *same* rig/clip to fairly compare integration and runtime; Godot is a third researched option, not eliminated on unsupported performance claims. This is a recommendation, not an irreversible technical decision.

## 4. Three animation production strategies

### A. Manual keyframe authoring (baseline)

1. Obtain a legally usable TİD reference (dictionary/video).
2. Verify sign identity, handshape, location, orientation, timing, movement and non-manual features with qualified linguistic input where available.
3. Use a properly rigged humanoid with articulated fingers and face controls in Blender.
4. Set key poses, transitions and facial motion; check self-intersection and timing.
5. Export compatible glTF clips and validate in the browser engine.
6. Seek independent technical and TİD reference/conformance review.

**Advantages:** control over subtle articulation; reproducible edits; feasible baseline for a small vocabulary. **Limitations:** substantial per-clip labor; expertise required; quality variance and revision costs. This method does not magically make a clip linguistically verified.

### B. Video → landmarks → retargeting → manual correction (candidate)

1. Use a permitted sign recording (RGB and possibly depth) as input.
2. Extract hand, body and relevant face points with MediaPipe or another validated estimator.
3. Handle uncertain/missing detections, crossed hands, occlusion and jitter.
4. Convert coordinate systems (camera vs world, handedness, scale, mirrored recording) and recover an appropriate articulated pose.
5. Map joint motion onto the avatar rig using kinematic constraints; solve twist/orientation ambiguity and motion timing.
6. Manually correct incorrect handshapes, contact, facial movement and collisions.
7. Export and compare with reference; obtain independent assessment where possible.

**Advantages:** repeatable pipeline may reduce work after setup, potentially scaling beyond a small sample. **Limitations:** landmarks are imperfect measurements, not final rotations; hands may be invisible; smoothing may destroy meaningful fast changes; 3D reconstruction from monocular images is ambiguous; manual cleanup can outweigh automation gains.

The 2024 **SignAvatars** work shows large-scale 3D holistic pose reconstruction is an active research area, but its results are not an out-of-the-box AUTSL-to-GLB converter or evidence that the SignBridge team can replicate its pipeline [R10]. **Spoken2Sign** demonstrates the architectural importance of separating text-to-gloss, a gloss-to-3D dictionary, motion connection and rendering; it does not validate SignBridge's planned TİD clips [R11].

### C. Symbolic notation (HamNoSys/SiGML; research alternative)

Describe signs using linguistically meaningful notation, then transform these descriptions into a form consumable by a compatible signing avatar. **Potential:** structured reusable motion, consistency and rule-driven authoring. **Requirements:** TİD-specific notation entries, qualified annotators, compatible engine and semantic/non-manual validation. A Turkish text word is **not** a HamNoSys specification. Given unknown resource availability, this is an alternative to investigate rather than the default MVP method [R12].

| Method | Setup effort | Effort per sign | Main uncertainty | Proposed role |
|---|---|---|---|---|
| Manual keyframes | Rig and animator workflow | Potentially high | Quality/review and schedule | Establish quality/effort baseline |
| Landmark + retargeting | Potentially substantial R&D | Potentially lower *after* setup | Fidelity and correction hours | Investigate in later pilot |
| HamNoSys/SiGML | Notation and compatible animation infrastructure | Depends on prepared notations | TİD resources and expertise | Document as further alternative |

**Important:** Do not conflate recognizing a sign from video (Direction A) with producing a full-body animation (Direction B). Both use motion representations but solve different tasks.

## 5. AUTSL, vocabulary and license limitations

Ankara University's AUTSL description specifies **226 isolated sign classes, 43 signers, 38,336 samples, RGB/depth at 512×512 and (x,y) coordinates for 25 body joints** [R8]. Those 25 points are **not** an articulated finger-and-face character rig. Potential additional extraction from RGB/depth recordings is a **hypothesis to test**, not a demonstrated conversion. Access, file completeness, annotation details and rights must be confirmed by the separate dataset access/audit work.

The proposal correctly distinguishes **recognition classes** from the **avatar clip lexicon**; the latter may draw on dictionary references and other permitted assets. The simple arithmetic 300 − 226 = 74 is *not a guaranteed exact coverage gap*: it only shows that 226 AUTSL classes cannot alone represent 300 distinct target signs. Actual vocabulary overlap may be lower; a gloss-by-gloss coverage audit is necessary. BosphorusSign22k's larger label inventory does not itself ensure access, redistribution rights or ready avatar motion.

**Copyright/privacy:** a dictionary video used for scholarly reference need not be redistributable, and deriving motion may require checking license terms. Do not commit source recordings or third-party avatars to the repository without explicit permission. User-study recording and ethics approval are separate from reusing an existing dataset; the proposal prohibits own **training-data** recording but has separately unresolved user-study recording decisions.

## 6. 300-sign feasibility — honest estimates

Proposal v1.1 **O4 and Expected Deliverables** retain **≥300 signs plus Turkish fingerspelling**. **SB-25 cannot lower or silently change that target.** The proposal directs the team to discuss the avatar approach, estimated effort and any target change with the advisor in advance of the SoW milestone on **13 November 2026**.

Define N = number of clips; M = manually authored/reviewed hours per clip; P = one-time setup hours for semi-automated pipeline; C = extraction + correction + review hours per clip.

- Manual: **T_manual = N × M**.
- Semi-automatic: **T_semi = P + N × C**.
- If M > C, the theoretical break-even is **N > P/(M − C)**; otherwise automation does not save hours under these assumptions.

**Illustrative assumptions, NOT measured results**:

| Scenario | Inputs | 300-clip labor |
|---|---|---|
| Optimistic manual | M = 0.5 h/clip | 150 h |
| Working manual example | M = 2 h/clip | 600 h |
| Conservative manual | M = 4 h/clip | 1,200 h |
| Example assisted | P = 80 h; C = 0.75 h/clip | 305 h |

At M=2, P=80, C=0.75, theoretical break-even is **64 clips** (equal effort at 64; savings above 64). None of these values was sampled from the team's actual work. **Excluded:** initial avatar design, rigging, licensing/access, review by TİD users, wrong/missing glosses, revisions, fingerspelling, clip transitions, integration, tool learning and schedule contingency. Therefore the estimates must never be reported as project measurements.

Difficulty differs by sign (one/two hands, complex finger articulation, face/head cues, hand contact, change of handshape). A fixed minutes-per-sign estimate is insufficient without sampling diverse signs. **Feasibility verdict:** technically plausible as a target, **not established as achievable in the remaining schedule**. A future pilot must measure the actual workload and quality before claiming feasibility.

## 7. Pilot validation specification (FUTURE WORK; not performed in SB-25)

The proposal's risk register anticipates a small pilot and advisor review, but this research issue explicitly excludes code development. This section therefore specifies a *subsequent, separately assigned* experiment; do not mark it completed or fabricate evidence.

Choose **5–10 permitted, linguistically sourced signs** spanning simple/complex handshape, one/two hands, face proximity, motion trajectory and non-manual features. Record sign ID, gloss, licensed source, annotator, complexity class and whether the sign overlaps the target vocabulary.

**Rendering A/B:** Same rig and GLB clips in Three.js and Babylon.js, same desktop/mobile browsers and hardware. Log integration hours, compatibility defects, first-load time, frame rate distribution, missing frames, memory, animation transitions and browser versions. No claims about performance are made before measurement.

**Authoring A/B:** For the same sign set, measure elapsed active manual-animation hours, initial pipeline setup, extraction runtime, retargeting correction hours, number of revisions and final clip duration. Record whether each clip passes (i) technical checks (finger bone motion, no collisions, consistent orientation, no jitter) and (ii) independently assessed linguistic conformance (handshape, location, orientation, movement, applicable face/head cues). Independent native/fluent TİD input should be sought. Reference matching without Deaf participant testing is **not** comprehension evidence.

**Study safeguards:** Recruitment, consent and actual user comprehension evaluation follow the ethics approval process in the proposal; no participant recording/testing begins before approval. The pilot may first use legally usable public reference material and technical inspection.

**Go/no-go review with advisor:** dataset/asset rights; percentage of target vocabulary covered; required hand/face fidelity; correction hours vs manual baseline; projected 300+fingerspelling labor; team capacity; accessibility/performance; expert feedback. A failed gate calls for documented scope discussion, **not** unilateral rewriting of O4.

## 8. Risks, evidence and mitigations

| Risk | Why it matters | Mitigation / unresolved evidence |
|---|---|---|
| Incorrect finger articulation | Changes sign identity | Articulated rig, detailed technical + TİD check; pilot |
| Missing face/head cues | Can alter meaning/grammar | Rig capability and non-manual-feature review |
| Kinect body skeleton mistaken for complete motion | Missing finger and face motion | Explicit AUTSL 25-point constraint; evaluate supplemental extraction |
| Occlusion / mirrored coordinates | Wrong handshape/orientation | Source review, axis calibration and correction tests |
| Vocabulary < target coverage | Missing clips | Gloss mapping; permitted alternatives; advisor scope review |
| Labor/time overrun | 300 clips may be infeasible | Measure per-sign and setup costs; revisit O4 only with advisor |
| Unlicensed assets | Ethical/legal distribution risk | Per-asset license inventory before publishing |
| Clips concatenate unnaturally | Sequence not equivalent to fluent TİD | Transition/coarticulation research and signer assessment |
| Poor browser performance | Mobile PWA usability | Repeatable device benchmark before commitment |
| Research mistaken for completed prototype | Misleading grading/evaluation | Label all scenarios as assumptions; no tests asserted |

## 9. Final recommendation and decision boundary

1. **Recommend Three.js for web rendering**, consistent with proposal v1.1; compare Babylon.js during a future controlled pilot, retaining Godot as a documented third alternative.
2. **Recommend Blender as the initial rig/clip authoring tool**, assuming an appropriately licensed avatar with independent finger/face controls.
3. **Prioritize a manual quality baseline and investigate a hybrid video-landmark-retargeting workflow**. Do not commit to fully automatic conversion, an AI-driven motion generator or an existing ready-made AUTSL animation library.
4. **Preserve the ≥300 signs and fingerspelling proposal target for now**; describe it as *not yet validated as feasible*, not as an already delivered or unilaterally reduced requirement.
5. **Seek a specific advisor decision before the 13 November SoW scope freeze** after the proposed pilot supplies actual effort and quality measurements.

This is an evidence-supported **research recommendation**, not an approved engineering selection or completed implementation.

## 10. Compliance and traceability

- **Jira SB-25:** three alternatives; browser/license/cost, hand/face and glTF; animation production methods; effort per sign and 300-sign assessment; cited recommendation; **no code** — covered above.
- **Proposal:** Separate Direction A recognition vocabulary and Direction B clip lexicon; prepared clips rather than generative signs; Three.js/Blender baseline; O4 ≥300 + alphabet; no own training-data recording; ethics before participants; advisor review before SoW — explicitly preserved.
- **Handbook rev2:** Issue type is **Story**, so branch **`story/SB-25`**, commit history and PR linked to Jira; teammate review before merge; research documentation is itself a work product and should go through Review; Confluence Documentation entry linked to repo and issue.
- **Limitations:** no performance benchmark, production pilot, verified TİD sign, license clearance or advisor technology approval was performed in this issue.

## References (primary/academic sources)

- **[R1]** Three.js, *GLTFLoader documentation*. https://threejs.org/docs/pages/GLTFLoader
- **[R2]** Three.js, *Animation System*. https://threejs.org/manual/pages/animation-system.html
- **[R3]** Three.js, *MIT License*. https://threejs.org/license/
- **[R4]** Babylon.js, *Official documentation*. https://doc.babylonjs.com/
- **[R5]** Babylon.js, *Source and Apache-2.0 license*. https://github.com/BabylonJS/Babylon.js
- **[R6]** Godot, *Official documentation and web export*. https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html
- **[R7]** Godot, *Exporting 3D scenes and glTF limitations*. https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/exporting_3d_scenes.html
- **[R8]** Ankara University CVML, *AUTSL Dataset*. https://cvml.ankara.edu.tr/datasets/
- **[R9]** Google AI Edge, *MediaPipe Hand Landmarker*. https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker
- **[R10]** Yu, Z. et al., *SignAvatars: A Large-scale 3D Sign Language Holistic Motion Dataset and Benchmark*, ECCV 2024. https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/653_ECCV_2024_paper.php
- **[R11]** Zuo, R. et al., *A Simple Baseline for Spoken Language to Sign Language Translation with 3D Avatars*, ECCV 2024. https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/6499_ECCV_2024_paper.php
- **[R12]** *HamNoSys to SiGML Conversion System for Sign Language Automation*, Procedia Computer Science (2016). https://doi.org/10.1016/j.procs.2016.06.063
- **[R13]** Khronos Group, *glTF 2.0 specification*. https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
- **[R14]** Blender Foundation, *Blender manual*. https://docs.blender.org/manual/en/latest/

**Internal authoritative documents:** *SignBridge-TR Project Proposal v1.1* (October 2026), especially Introduction/Direction B, O4, Methods §3/§7 and risk register; *Senior Project Handbook rev2*, Working Stories/Branch Naming/Confluence structure; [SB-25](https://el-dili.atlassian.net/browse/SB-25).
