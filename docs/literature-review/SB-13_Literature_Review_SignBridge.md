---
title: "SB-13 - Literature Review on TİD Recognition and Translation Models"
subtitle: "Evidence-based comparison of LSTM, Transformer and GCN models for SignBridge-TR"
author: "Ceren Bilgenoğlu - SignBridge Team"
date: "15 October 2026 - Version 2.1"
lang: en
---

| Field | Value |
|---|---|
| Project / issue | SignBridge-TR / SB-13 (Story, 5 SP) |
| Epic / sprint | SB-1 / SB Sprint 1 (5-18 October 2026) |
| Author | Ceren Bilgenoğlu |
| Document status | Revised submission for peer review; approval not claimed |
| Related work | SB-8 proposal; SB-12 datasets; SB-14 gloss/lexicon; SB-15 landmarks |
| Proposal basis | Supplied SignBridge-TR Project Proposal, 9-page version |
| Revision | v2.1: experiment provenance, current proposal alignment, API versioning and qualified recommendations |

## Abstract

This review compares recurrent, attention-based and graph-based models for landmark-based Turkish Sign Language (TİD) recognition and examines their role in a bounded recognition-to-text pipeline. Published accuracy and timing evidence are separated by dataset and evaluation protocol. The review supports testing an LSTM baseline against a pose Transformer and a graph model, while treating browser compatibility, unseen-signer accuracy and transfer learning as questions requiring project measurements. It preserves the proposal's pause-separated MVP and existing success criteria. Continuous signing and sentence-level translation are reviewed to explain limitations and future extensions, rather than to expand the current implementation scope. No new model training or project benchmark is reported.

# 1. Introduction

SignBridge-TR is a proposed browser-based system connecting TİD signs with Turkish text and speech. Its reverse direction uses Turkish-to-gloss conversion and a verified avatar animation library. SB-13 concerns the recognition and translation literature supporting these components; it does not implement the complete application.

The recognition input is a time sequence of landmarks rather than raw video. This choice reduces the recogniser's visual input but makes landmark quality, missing observations and feature selection part of the learning problem. The system must distinguish a sign label from a grammatically correct Turkish sentence and must remain usable by people not represented in training.

## 1.1 Research questions

- RQ1: Which TİD resources fit the target vocabulary and evaluation setting?
- RQ2: How do LSTM, Transformer and GCN models compare under comparable landmark inputs?
- RQ3: How should pre-training and adaptation to a small domain vocabulary be assessed?
- RQ4: What separates isolated recognition, continuous recognition and translation?
- RQ5: What evidence is needed before selecting a model for browser deployment?

## 1.2 Scope and contribution

The review covers datasets, model families, landmark extraction, transfer learning, segmentation and gloss-mediated translation. Detailed avatar motion generation, speech recognition and accessibility implementation belong to other project work. The contribution is a model-selection rationale and an evaluation protocol, not a claim of a new state-of-the-art algorithm. The proposal already limits the MVP to intentionally pause-separated signs; unrestricted continuous TİD translation remains outside this scope.

# 2. Review Methodology

## 2.1 Review design and evidence base

This is a targeted narrative review, not a systematic review or an exhaustive survey of work published through 2026. The supplied v2.0 bibliography was the seed set. The present revision audited decision-critical claims against primary publications and official documentation on 15 October 2026. Earlier database search counts and screening logs were not retained, so no historical hit counts, deduplication totals or PRISMA flow are asserted.

Focused queries included "OpenHands ACL 2022 AUTSL", "BosphorusSign22k", "E-TSL continuous educational Turkish sign language dataset" and "Linguistically motivated sign language segmentation". Retrieval followed primary links from ACL Anthology, author manuscripts, dataset pages and official documentation. The audit checked retained result tables and the current landmark API (Appendix B). Foundational/application publications span 1997-2024; documentation was checked in 2026. This distribution does not imply that newer research is absent.

## 2.2 Selection and quality criteria

Include a source if it supplies a relevant model, dataset, linguistic observation, evaluation method or official deployment specification. Prefer original papers and official documentation. Exclude unsupported benchmark claims, glove-only methods and product marketing as evidence of model accuracy. A participant account [17] is retained only as supplementary deployment context; it is not a peer-reviewed result or a substitute for competition rules [16].

The bibliography has 23 entries: 17 academic publications, five official technical/competition resources and one supplementary participant write-up. All are cited. A citation does not imply that every experiment or bibliographic field was independently reproduced.

## 2.3 Reporting rules

Every retained model score is associated with its dataset, evaluation partition and input modality. Unknown signer independence is explicitly marked rather than inferred. Accuracy, translation quality and timing are different outcomes and are not ranked on one numerical scale. Dataset descriptors, API output counts and proposal targets are labelled as such; they are not project results. Findings from the literature are distinguished from engineering hypotheses and proposed future experiments.

# 3. Background: Language and Task Definitions

## 3.1 Recognition is not translation

Isolated recognition predicts a gloss from a bounded sign clip. Continuous recognition predicts a gloss sequence from an unsegmented stream. Translation produces a spoken-language sentence and must account for grammar and meaning [10], [11]. Recognition accuracy therefore cannot establish translation quality. A gloss sequence is an interface representation, not automatically grammatical Turkish.

For the MVP, the intended chain is a user-delimited sign clip, a recognised gloss, an accumulated gloss sequence and rule/LLM-assisted Turkish generation. Recognition uncertainty must remain visible to the next module instead of being silently replaced by fluent text. Section 9 discusses why this design does not amount to unrestricted continuous translation.

## 3.2 TİD-specific implications

TİD has its own linguistic structure. Zeshan [19] describes the role of non-manual features, while Kayahan and Güngör [20] discuss Turkish-to-TİD conversion. These sources support treating Turkish morphology, gloss ordering and non-manual information explicitly; they do not justify a universal word-by-word conversion rule.

For SB-14, gloss identity, Turkish equivalents, domain, variant information and non-manual annotations should be distinguishable. An annotation field does not prove that the recogniser can infer its value. Facial feature selection and language rules require validation with reliable TİD references and, where available, competent TİD users. SignBridge's recognition vocabulary and avatar library need separate coverage accounting.

# 4. Datasets and Evaluation Setting (RQ1)

| Resource | Task and modality | Relevance to SignBridge | Evaluation caution |
|---|---|---|---|
| AUTSL [1] | Isolated TİD; RGB, depth and Kinect skeleton recordings | Public pre-training and recognition benchmark; 226 classes, 43 signers, 38,336 samples | Use the intended signer-independent partition; native skeleton and re-extracted MediaPipe are different inputs. |
| BosphorusSign22k [2] | Isolated TİD; multimodal recordings; 744 glosses, six signers, 22,542 samples | Candidate domain vocabulary and training resource, already mentioned in the proposal | Record the exact held-out-signer protocol and dataset version; few signers limit generalisation evidence. |
| E-TSL [18] | Continuous educational TİD-to-Turkish; pose-derived translation baselines | Evidence about translation difficulty and domain mismatch | Published train/dev/test split must not be assumed signer-independent. |
| Google ISLR [16] | Isolated ASL competition with landmark inputs | Deployment and representation context | ASL results do not establish TİD accuracy; competition evaluation differs from the project. |

The descriptors above characterise resources, not model achievements. AUTSL's original paper demonstrates sensitivity to evaluation partition [1]. The ChaLearn challenge [3] provides further signer-independent benchmarking context. Neither a random clip split nor high performance on known signers substitutes for testing unseen users.

**Action for SB-12:** map the planned vocabulary to dataset glosses using stable identifiers; record variants, missing classes, signer coverage, acquisition conditions and permissions. Do not assume that similar Turkish labels denote identical signs. BosphorusSign22k's health vocabulary makes this mapping relevant, but inclusion as an actual training source depends on access and coverage, not merely its appearance in the proposal.

**Leakage control:** assign all clips and augmented copies from a signer to the same partition. Fit preprocessing statistics on training data only. Check public pre-training data for overlap with evaluation people or recordings where identifiers permit. Report unresolved overlap as a limitation.

# 5. Landmark Extraction and Versioned Inputs

## 5.1 Legacy and current output conventions

Legacy MediaPipe Holistic is commonly described with 543 landmarks: 33 pose, 468 face and 21 per hand [13]. The current Holistic Landmarker documentation describes 553: the face output includes 478 points, alongside the same pose and hand counts [14]. These are API/model conventions, not interchangeable feature vectors. The Web implementation guide describes the Tasks package and IMAGE/VIDEO modes [23].

The project should pin the package and model asset versions, store the selected landmark indices, and document how any legacy training representation maps to the browser representation. A newly available API does not prove that a particular checkpoint or browser configuration works. The selected export and extraction pipeline must be tested before the training format is frozen.

## 5.2 Proposed feature contract for SB-15

Use a documented upper-body, hand and facial subset rather than assuming every available point is necessary. Store timestamps, coordinate conventions, missing-point masks, handedness and preprocessing version. Normalise position and scale consistently in training and inference. Assess whether additional facial cues improve the actual classification task; a sparse pose representation does not capture all linguistic facial information.

Landmark dropout and camera framing failures should be represented explicitly. Do not replace missing coordinates with zeros without a mask and a tested convention. Mirroring must preserve left/right semantics and should only be used when linguistically valid. Any smoothing must be assessed for the delay it introduces. These are proposed engineering controls, not completed SB-15 results.

# 6. Architecture Families (RQ2)

## 6.1 LSTM and recurrent models

LSTM models [7] update a hidden state over time and can aggregate the motion represented by landmark frames. Their useful role here is a transparent sequence baseline. Bidirectional variants use future context within the clip and must not be described as strictly causal streaming models. Sequence length, hidden size, feature encoding and the export path affect cost; the family name alone does not guarantee speed or generalisation.

A recurrent classifier does not explicitly encode the joint graph unless spatial structure is added. It may therefore need feature engineering or a spatial encoder. Its simplicity makes failure analysis and controlled comparisons useful even if a more complex model later wins.

## 6.2 Transformer models

Self-attention [8] connects observations across a sequence; positional information is required to represent ordering. SPOTER [5] is a relevant pose-based recognition design. Encoder-only recognition and encoder-decoder translation have different objectives and should not be treated as one interchangeable model.

For a small custom vocabulary, overfitting and sensitivity to padding, temporal resampling and landmark noise must be assessed. Attention does not automatically encode anatomical adjacency. Compact configurations are plausible candidates, but browser support and latency depend on the exported graph and runtime. No SPOTER result from another language is used as a numerical prediction for SignBridge.

## 6.3 GCN and spatio-temporal graph models

ST-GCN [9] models joint relationships over space and time. SL-GCN in SAM-SLR [4] adapts graph-based processing to signs. Its structural bias is relevant when the input has a known joint arrangement. Graph topology and omitted hand/facial nodes can materially affect the information retained.

SAM-SLR combines multiple streams and modalities [4]; a whole-system score must not be labelled a landmark-only GCN score. Graph operations may be expressible through standard exported tensor operations, but compatibility depends on implementation, operator set and runtime. Export difficulty is therefore a test item for every family, not a universal GCN disadvantage.

# 7. Comparative Evidence and Its Limits

## 7.1 Recognition accuracy: one common benchmark

Table 1 reproduces the AUTSL row of OpenHands [6, Table 2]: MediaPipe-derived 27-point 2D inputs, published benchmark test partition, signer-independent AUTSL setting. These are source-reported best-run results, not SignBridge measurements or current state-of-the-art claims.

| Model | AUTSL top-1 accuracy | Source |
|---|---|---|
| LSTM | 77.4% | [6], Table 2 |
| BERT-style Transformer | 81.0% | [6], Table 2 |
| ST-GCN | 90.4% | [6], Table 2 |
| SL-GCN | 91.9% | [6], Table 2 |

For reproduction, retain the exact source split manifest; a matching dataset name alone is insufficient. This comparison favours graph models in this experiment, but does not establish a universal family ranking.

## 7.2 Classifier timing: a separate experiment

Table 2 is from OpenHands [6, Appendix B, Table 7]: INCLUDE test clips, pose classifier only, batch size one, Intel Xeon E5-2690 v4. It is neither AUTSL timing nor a browser/end-to-end benchmark. Signer independence of this timing set is not established here.

| Model | Mean classifier latency per video |
|---|---|
| LSTM | 8.05 ms |
| Transformer | 30.64 ms |
| ST-GCN | 23.02 ms |
| SL-GCN | 52.80 ms |

Do not combine Tables 1 and 2 into an AUTSL accuracy/latency Pareto frontier. Different clip durations, devices and runtimes require new measurements.

## 7.3 Shared decision criteria

| Criterion | LSTM | Transformer | GCN |
|---|---|---|---|
| Temporal modelling | Recurrent state | Attention plus ordering | Temporal processing with joint graph |
| Spatial prior | Must be supplied or learned | Must be supplied or learned | Explicit joint adjacency |
| Small-data concern | Overfitting remains possible | Capacity and regularisation require care | Graph validity and capacity require care |
| Streaming concern | Causal only if designed so | Attention/window policy must be specified | Temporal receptive field must be specified |
| Deployment gate | Validate export and browser execution | Validate export and browser execution | Validate export and browser execution |
| Role in this project | Baseline | Recognition candidate; translation context | Recognition candidate; possible encoder |

These criteria are an engineering comparison, not measured advantages on the proposed custom dataset. The decision gap in the reviewed evidence is the absence of a directly matched SignBridge vocabulary, unseen-signer recording protocol and browser target. The project's contribution is to evaluate that combination transparently rather than copy a benchmark ranking.

# 8. Transfer Learning and Small Datasets (RQ3)

OpenHands reports benefits from predictive pose pre-training and shows that pre-training objectives need not help equally [6]. This motivates testing transfer; it does not make it mandatory for every dataset.

For SignBridge, compare training from scratch with supervised public-data pre-training and fine-tuning. Consider self-supervised pre-training only if appropriate data, checkpoints, permissions and time are available. Keep the downstream model, split and tuning budget comparable. Record which layers are reused and how the classification head changes.

The proposal plans at least ten recording participants and a 150-sign recognition vocabulary. This describes class and signer coverage, not the number of examples: repetitions, sessions and recording conditions still need specification. More repeated clips from the same person do not substitute for signer diversity. Adaptation must not tune on the held-out test signers.

Cross-language transfer may share visual motion features, but gloss semantics and inventories remain language-specific. Report negative transfer as well as improvements. No percentage gain from another language or dataset is assumed to transfer directly to TİD.

# 9. Translation and Segmentation (RQ4)

## 9.1 Translation evidence

Neural Sign Language Translation [10] and Sign Language Transformers [11] establish important sequence-to-sequence and joint recognition/translation approaches. Their language, input and annotation conditions differ from a small domain-specific TİD MVP. Their results are not substituted for TİD recognition accuracy.

A directly relevant TİD example is E-TSL [18, Table II]. GNN-T obtains 3.28 BLEU-4 on its published test partition, with a MediaPipe-derived 53-landmark input. The publication specifies a train/dev/test split; signer-disjoint evaluation is not established by that description. BLEU is a translation overlap measure, not percent-correct sign recognition. This is a baseline in that study, not a claim about the best TİD system available in 2026.

Turkish-to-TİD work [20] motivates explicit gloss conversion, but rule reuse requires linguistic review. A fluent LLM output is not evidence that the original signs' meaning survived. Test recognised-gloss and gold-gloss inputs separately to distinguish recogniser errors from language-generation errors. Include negation, quantities, names and out-of-vocabulary cases. Assess meaning preservation through human review alongside the proposal's automatic metrics.

## 9.2 Signing detection, boundary detection and the MVP

Signing detection asks whether signing is occurring [12]. It does not identify every sign boundary. Linguistically motivated BIO segmentation [15] addresses natural streams in which neighbouring signs need not be separated by inactive frames. Its cross-domain observations do not validate a ready-made TİD segmenter for this project.

The proposal deliberately asks MVP users to pause between isolated signs. Preserve that interaction rule and explain it in the interface. Test missed boundaries, duplicate predictions, accidental motion and incomplete signs under this restricted protocol. Natural continuous signing and learned BIO segmentation are future research or a separately approved extension, not mandatory additions to the present sprint.

# 10. Browser Deployment and Measurement (RQ5)

ONNX Runtime Web [21] and TensorFlow.js [22] provide deployment routes, but framework availability alone does not certify a trained model's browser compatibility. Validate numerical agreement before/after export, supported operators, loading time, memory use and inference on the intended browser/device. The selected Web landmark API must be tested independently [23].

The Kaggle competition [16] and participant account [17] provide examples of constrained landmark-based recognition. Their constraints are platform-specific. This review does not convert them into a browser performance guarantee or retain unverified memory/time caps as project requirements.

Keep three proposal measures separate: O1's browser throughput target of at least 15 FPS, sign-end-to-spoken-output median latency of at most 2.0 seconds, and speech-end-to-avatar-start median latency of at most 2.5 seconds. These are existing project targets, not published model results. Define exactly which pipeline stage the FPS measure covers before testing; record extraction and classification rates separately.

For Direction A, timestamp sign completion, segmentation decision, recognition, gloss conversion and speech start. Measure network/LLM/TTS delays as well as landmark processing. Report distributions and device configuration, not only one favourable average. Profile to locate the bottleneck rather than assuming it is the extractor. Schedule heavy work to preserve UI responsiveness and include low-end failure behaviour in the feasibility assessment.

# 11. Consistency with the Supplied Project Proposal (SB-8)

The comparison below uses the supplied nine-page proposal. It distinguishes existing commitments from suggested changes; it does not amend the proposal.

| Proposal item and location | Assessment | Recommended action |
|---|---|---|
| Product concept and H1 name a Transformer; Methods already includes comparison with a graph network (pp. 2, 7). | Comparison is already planned. The hypothesis and final model-selection language need clarification. | Retain the Transformer as a candidate; agree whether H1 tests it specifically or the selected model. Record the decision with SB-8's owner. |
| BosphorusSign22k appears in the background and references; the resource plan names AUTSL (pp. 1, 8). | The dataset is already acknowledged. Its use for training is not yet established. | Ask SB-12 to assess domain overlap, permission and signer coverage before adding it as a committed resource. |
| Holistic and normalised hand/body/face features are planned (pp. 2, 7). | Consistent in principle; legacy/current API conventions need separation. | Pin extractor/model versions and feature schema under SB-15 (Section 5). |
| O1/H1 specify at least 85% top-1 on unseen signers; O1 also specifies top-5 and throughput targets (pp. 4, 7). | These are hypotheses/acceptance targets, not literature guarantees. | Preserve the current targets. Do not invent a 75% pass threshold; any change requires team/advisor agreement. |
| MVP uses short pauses; continuous translation is explicitly excluded (p. 2). | This is an intentional, feasible scope boundary. | Preserve it. Review natural signing limitations without making BIO segmentation a compulsory MVP feature. |
| Sign recognition feeds gloss-to-Turkish generation; reverse direction uses a separate animation library (pp. 2, 7). | Bounded recognition and language generation are distinct modules. | Evaluate the modules separately and document vocabulary limitations. Do not claim general continuous SLT. |

The proposal's 150 recognised signs and at least 300 avatar signs are different deliverables. SB-13 neither changes those counts nor requires model training, animation creation or a database implementation to complete this literature task. Proposal changes should be logged as decisions and agreed with the responsible owner, rather than treated as already approved.

# 12. Recommendation and Proposed Evaluation Protocol

## 12.1 Candidate models and scope

Begin with one LSTM baseline, a compact pose Transformer and one graph candidate. Prefer ST-GCN as the first graph implementation if resources are limited; add SL-GCN only if justified by feasibility. Candidate selection is provisional. Reuse public checkpoints only when their licence, feature schema and model configuration are compatible. A failed export should be documented rather than silently changing the evaluation pipeline.

## 12.2 Controlled comparison

Use identical selected landmarks, normalisation, vocabulary, sequence policy and signer partitions. Specify a comparable tuning budget rather than forcing identical hyperparameters on different architectures. Use validation data for selection; reserve the test set for final evaluation. Report repeated-run variation when resources permit, along with exact configurations and split manifests.

Measure top-1/top-5 accuracy, per-class errors, confusion patterns and failure cases on unseen signers. Record model size, memory, latency and throughput on the target browser/hardware with the same test clips. Separate numerical agreement after export from task accuracy. Report abstention/rejection behaviour for non-signing, unknown signs and low-confidence inputs.

## 12.3 Decision gates and dependencies

First verify that the model and extractor run correctly in the intended browser. Then compare recognition quality subject to the existing proposal's performance and usability requirements. Choose among feasible candidates using accuracy, resource cost and maintainability. Any weighting or tie-break rule must be agreed before final test evaluation; this review does not introduce an arbitrary accuracy-gap threshold.

SB-12 supplies vocabulary/data compatibility; SB-14 supplies stable gloss identifiers and metadata; SB-15 supplies the versioned landmark contract and extraction feasibility. SB-8 records approved model/scope decisions. Training and deployment experiments are subsequent implementation work, subject to sprint planning, not results already produced for SB-13.

# 13. Limitations

The review is selective and not a complete 2026 literature census. The most directly matched recognition comparison is historical and comes from one benchmark study. No new training, browser experiment or participant study was performed. A paper's reported score is not independently reproduced here. Competition and participant evidence is secondary to peer-reviewed comparisons.

Source-reported timing, languages, signer partitions and extraction versions differ. Some published splits do not establish unseen-signer testing; these are explicitly marked. No result guarantees performance on the custom vocabulary, hardware or users. Linguistic rules and non-manual annotations need validation, and public visibility of data does not establish permission to train on or redistribute it.

# 14. Conclusion

The literature supports evaluating recurrent, attention-based and graph-based recognisers under a shared landmark and unseen-signer protocol. It does not justify fixing the winner before the project's accuracy and browser measurements. Public pre-training is a strong candidate strategy, with its benefit tested against an appropriate baseline. The proposal's pause-separated, vocabulary-bounded MVP remains the implementation scope. The next decisions concern compatible data, a versioned feature contract and controlled evaluation, while continuous TİD translation remains a documented extension.

# Appendix A. Traceability to SB-13

| Acceptance criterion | Evidence in this document / delivery requirement |
|---|---|
| Documented review method | Section 2 and Appendix B; targeted search and audit limitations explicit |
| At least 15 academic/official sources, cited in text | References: 23 entries; supplementary [17] separately identified |
| LSTM vs Transformer vs GCN; result context | Sections 6-7; accuracy and timing separated |
| Landmark extraction, transfer, translation, segmentation | Sections 5, 8 and 9 |
| Model recommendation and proposal check | Sections 11-12 |
| MD, BibTeX, PDF on story/SB-13; teammate PR approval | Deliverable files accompany this document; actual commit and approval must be recorded in PR #2 |
| Jira PDF and Confluence Documentation summary | Upload this revised PDF and publish the accompanying summary; document existence is not proof of completion |

# Appendix B. Targeted Source-Audit Record

Audit date: 15 October 2026. These are focused retrievals for this revision and its preceding assessment, not a reconstructed historical systematic-search log.

| Retrieval / source | Audit purpose and outcome |
|---|---|
| OpenHands ACL PDF [6], Table 2 and Appendix B | Checked recognition and timing provenance; separated AUTSL accuracy from INCLUDE timing. |
| AUTSL author manuscript [1] | Checked dataset description and signer-independent evaluation rationale. |
| BosphorusSign22k project page [2] | Checked dataset relevance; no new training-use permission inferred. |
| E-TSL author manuscript [18], Sections III and Table II | Checked pose input, published partition and test translation metric; signer-disjoint status not inferred. |
| Google Holistic overview and Web guide [14], [23] | Checked current output schema and Web API; no project device test claimed. |
| ACL segmentation publication [15] | Checked task/boundary distinction and relevance to natural continuous signing. |
| Supplied proposal (pp. 1-2, 4, 7-8) | Checked existing dataset mention, restricted MVP, model language and unchanged targets. |

# References

[1] O. M. Sincan and H. Y. Keles, "AUTSL: A large scale multi-modal Turkish Sign Language dataset and baseline methods," *IEEE Access*, vol. 8, pp. 181340–181355, 2020, doi: 10.1109/ACCESS.2020.3028072.

[2] O. Özdemir, A. A. Kındıroğlu, N. C. Camgöz, and L. Akarun, "BosphorusSign22k sign language recognition dataset," in *Proc. LREC 2020 9th Workshop on the Representation and Processing of Sign Languages*, 2020, pp. 181–188.

[3] O. M. Sincan, J. C. S. Jacques Junior, S. Escalera, and H. Y. Keles, "ChaLearn LAP large scale signer independent isolated sign language recognition challenge: Design, results and future research," in *Proc. IEEE/CVF CVPR Workshops*, 2021, pp. 3472–3481.

[4] S. Jiang, B. Sun, L. Wang, Y. Bai, K. Li, and Y. Fu, "Skeleton aware multi-modal sign language recognition," in *Proc. IEEE/CVF CVPR Workshops*, 2021, pp. 3413–3423.

[5] M. Boháček and M. Hrúz, "Sign pose-based transformer for word-level sign language recognition," in *Proc. IEEE/CVF WACV Workshops*, 2022, pp. 182–191.

[6] P. Selvaraj, G. NC, P. Kumar, and M. Khapra, "OpenHands: Making sign language recognition accessible with pose-based pretrained models across languages," in *Proc. 60th Annual Meeting of the ACL (Vol. 1: Long Papers)*, 2022, pp. 2114–2133, doi: 10.18653/v1/2022.acl-long.150.

[7] S. Hochreiter and J. Schmidhuber, "Long short-term memory," *Neural Computation*, vol. 9, no. 8, pp. 1735–1780, 1997.

[8] A. Vaswani *et al.*, "Attention is all you need," in *Advances in Neural Information Processing Systems 30 (NeurIPS)*, 2017.

[9] S. Yan, Y. Xiong, and D. Lin, "Spatial temporal graph convolutional networks for skeleton-based action recognition," in *Proc. AAAI Conference on Artificial Intelligence*, 2018.

[10] N. C. Camgöz, S. Hadfield, O. Koller, H. Ney, and R. Bowden, "Neural sign language translation," in *Proc. IEEE/CVF CVPR*, 2018, doi: 10.1109/CVPR.2018.00812.

[11] N. C. Camgöz, O. Koller, S. Hadfield, and R. Bowden, "Sign language transformers: Joint end-to-end sign language recognition and translation," in *Proc. IEEE/CVF CVPR*, 2020.

[12] A. Moryossef, I. Tsochantaridis, R. Aharoni, S. Ebling, and S. Narayanan, "Real-time sign language detection using human pose estimation," in *Proc. ECCV Workshops (SLRTP)*, 2020.

[13] I. Grishchenko and V. Bazarevsky, "MediaPipe Holistic — Simultaneous face, hand and pose prediction, on device," Google Research Blog, Dec. 2020.

[14] Google AI Edge, "Holistic landmark detection guide," MediaPipe Solutions documentation. [Online]. Available: https://developers.google.com/edge/mediapipe/solutions/vision/holistic_landmarker (accessed 15.10.2026).

[15] A. Moryossef, Z. Jiang, M. Müller, S. Ebling, and Y. Goldberg, "Linguistically motivated sign language segmentation," in *Findings of the Association for Computational Linguistics: EMNLP 2023*, 2023, pp. 12703–12724, doi: 10.18653/v1/2023.findings-emnlp.846.

[16] Google, Georgia Tech, and Deaf Professional Arts Network, "Google – Isolated Sign Language Recognition," Kaggle competition, 2023. [Online]. Available: https://www.kaggle.com/competitions/asl-signs (accessed 15.10.2026).

[17] "Isolated sign language recognition: 2nd place solution write-up (Kaggle ISLR 2023)," Habr, 2024. [Online]. Available: https://habr.com/en/articles/795109 (accessed 15.10.2026).

[18] Ş. Öztürk and H. Y. Keles, "E-TSL: A continuous educational Turkish Sign Language dataset with baseline methods," in *Proc. Int. Congress on Human-Computer Interaction, Optimization and Robotic Applications (HORA)*, 2024, doi: 10.1109/HORA61326.2024.10550648.

[19] U. Zeshan, "Aspects of Türk İşaret Dili (Turkish Sign Language)," *Sign Language & Linguistics*, vol. 6, no. 1, pp. 43–75, 2003, doi: 10.1075/sll.6.1.04zes.

[20] D. Kayahan and T. Güngör, "A hybrid translation system from Turkish spoken language to Turkish Sign Language," in *Proc. IEEE Int. Symp. on INnovations in Intelligent SysTems and Applications (INISTA)*, 2019, doi: 10.1109/INISTA.2019.8778246.

[21] Microsoft, "ONNX Runtime Web," ONNX Runtime documentation. [Online]. Available: https://onnxruntime.ai/docs/tutorials/web/ (accessed 15.10.2026).

[22] D. Smilkov *et al.*, "TensorFlow.js: Machine learning for the web and beyond," in *Proc. Machine Learning and Systems (MLSys)*, 2019.

[23] Google AI Edge, "Holistic landmark detection guide for Web," MediaPipe Solutions documentation. [Online]. Available: https://developers.google.com/edge/mediapipe/solutions/vision/holistic_landmarker/web_js (accessed 15.10.2026).
