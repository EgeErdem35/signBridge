---
title: "SB-13 — Literature Review on TİD Recognition and Translation Models"
subtitle: "A comparative review of LSTM, Transformer and GCN architectures for landmark-based Turkish Sign Language (TİD) recognition and translation"
author: "SignBridge Team — prepared by Ceren Bilgenoğlu"
date: "15.10.2026 — Version 2.0"
lang: en
---

| Field | Value |
|---|---|
| Project | SignBridge |
| Jira issue | SB-13 (Story, 5 SP) |
| Epic | SB-1 PROJECT_MANAGEMENT_AND_DOCUMENTATION |
| Sprint | SB Sprint 1 (05.10.2026 – 18.10.2026) |
| Author | Ceren Bilgenoğlu |
| Reviewer(s) | *to be filled after PR review* |
| Related issues | SB-8 (Proposal), SB-12 (Datasets), SB-14 (Gloss/Lexicon), SB-15 (MediaPipe) |
| Status | Draft for review |

# 1. Introduction

SignBridge aims to translate between Turkish Sign Language (Türk İşaret Dili, TİD) and Turkish in a web browser: signed input is captured by a camera, converted into body landmarks, and recognised; in the opposite direction, Turkish speech or text is mapped to signs rendered by a 3D avatar. The machine-learning core of the system is a **landmark-based** sign recogniser, i.e. a model that receives sequences of keypoints (hands, body, face) rather than raw RGB frames.

Jira issue SB-13 asks for *"a comprehensive literature review on existing Sign Language Recognition (SLR) models, comparing Transformer vs. LSTM vs. GCN architectures for landmark-based TİD translation."* This document answers that request and is written so that its conclusions can be used directly by SB-8 (Project Proposal), SB-12 (dataset exploration), SB-14 (gloss/lexicon schema) and SB-15 (MediaPipe feasibility).

## 1.1 Research questions

- **RQ1.** Which public TİD datasets are available, and how should models trained on them be evaluated?
- **RQ2.** How do LSTM, Transformer and GCN architectures compare for landmark-based isolated sign recognition, in accuracy, cost and data needs?
- **RQ3.** Can models pre-trained on large datasets be transferred to a small, project-specific vocabulary?
- **RQ4.** What does the literature say about sign language *translation* (sentence level) and about segmenting continuous signing?
- **RQ5.** What constraints does real-time, in-browser execution impose on the model choice?

## 1.2 Scope

In scope: isolated and continuous SLR, sign language translation (SLT), pose/landmark-based methods, TİD resources, and deployment on consumer devices. Out of scope: sensor-glove methods, sign language *production* with avatars (covered by the AVATAR_3D_VISUALIZATION epic), and speech recognition (covered by the proposal).

# 2. Review Methodology

**Sources searched:** Google Scholar, arXiv, IEEE Xplore, CVF Open Access (CVPR/ICCV/WACV workshops), ACL Anthology, and the Kaggle competition archive.

**Search strings (combined with AND/OR):** "sign language recognition", "Turkish Sign Language" / "TİD" / "TSL", "AUTSL", "BosphorusSign22k", "skeleton-based" / "pose-based" / "landmark", "graph convolutional network", "transformer", "LSTM", "sign language translation", "sign language segmentation", "MediaPipe".

**Inclusion criteria:** (i) peer-reviewed papers, theses or official benchmark/competition documentation; (ii) published 1997–2025 (foundational architecture papers are included regardless of age); (iii) reports quantitative results on a public benchmark, or provides a TİD resource or linguistic description; (iv) relevance to at least one research question.

**Exclusion criteria:** non-reproducible claims without a public benchmark, sensor/glove-only systems, and secondary blog posts when a primary source exists (blogs are used only for competition rules not published elsewhere).

**Quality rule used throughout:** every number in this review is reported together with (a) the dataset, (b) the split (random vs. signer-independent) and (c) the input modality, because results that differ in any of these are not comparable. Where two numbers come from different papers, this is stated explicitly.

The final set contains **22 references** (see References). Every reference is cited in the text.

# 3. Background

## 3.1 Recognition vs. translation

*Isolated SLR* classifies a pre-segmented clip into one sign (gloss). *Continuous SLR* outputs a gloss sequence from an unsegmented video. *Sign language translation (SLT)* produces a spoken-language sentence, which requires handling different word order and grammar [10], [11]. SignBridge's sign-to-text direction combines isolated recognition with a segmentation step (Section 9) and a gloss-to-Turkish step (Section 8).

## 3.2 Linguistic properties of TİD relevant to modelling

TİD is a full natural language with its own grammar. Zeshan's typological description documents, among others, three types of non-manual negation (headshake, backward head tilt, puffed cheeks), a negator that cliticises to the preceding predicate, and a question particle [19]. Kayahan and Güngör's Turkish-to-TİD work notes that TİD glosses carry no suffixes (verbs in infinitive form, nouns in nominative), that meaning carried by Turkish suffixes is often expressed through non-manual markers such as head tilt, eye gaze and mouthing, and that proper nouns are fingerspelled [20].

**Implication:** a recogniser that uses only hand landmarks cannot see negation, questions or many grammatical markers. Face and head landmarks must be part of the input (Section 5), and the gloss schema in SB-14 must store non-manual markers explicitly.

# 4. Datasets (RQ1)

| Dataset | Language | Classes | Signers | Samples | Modalities | Split used for reported results |
|---|---|---|---|---|---|---|
| AUTSL [1] | TİD | 226 | 43 | 38,336 | RGB, depth, skeleton (Kinect v2) | Signer-independent |
| BosphorusSign22k [2] | TİD | 744 (428 health, 163 finance, 174 general) | 6 | 22,542 | RGB 1920×1080 @ 30 fps, depth, Kinect + OpenPose keypoints | Signer-independent (1 signer held out) |
| E-TSL [18] | TİD (continuous) | – (sentence level) | 11 | 1,410 videos (~24 h) | RGB | Translation (BLEU) |
| Google ISLR (Kaggle) [16] | ASL | 250 | – | ~95,000 training examples | MediaPipe Holistic landmarks only | Hidden test set |

**AUTSL.** The largest isolated TİD dataset. Its authors report that the same CNN+LSTM baseline reaches **95.95 % on a random split but only 62.02 % on the signer-independent split** [1]. This gap is the most important methodological lesson for SignBridge: *results on random splits overestimate real-world accuracy for unseen users.* AUTSL was later used for the ChaLearn LAP 2021 signer-independent challenge [3].

**BosphorusSign22k.** Smaller in signer count but larger in vocabulary, and **428 of its 744 classes are from the health domain** [2]. Because SignBridge targets health/pharmacy scenarios, this dataset is the most relevant source of domain vocabulary, and should be added to the proposal's dataset table (see Section 11). Its baselines are RGB-based (IDT 88.53 %, MC3 3D-ResNet 78.85 % top-1, signer-independent) [2]; no landmark-based baseline is reported in that paper.

**E-TSL.** A continuous TİD translation dataset built from online school lessons. 64 % of its vocabulary words are singletons and the best reported baseline reaches only **3.28 BLEU-4** [18]. It shows that open-vocabulary TİD translation is far from solved.

**Google ISLR.** Not TİD, but it is the closest public benchmark to SignBridge's technical setting: input is *only* MediaPipe Holistic landmarks and submissions had to run under strict on-device constraints [16], [17] (see Section 10).

**Action for SB-12:** compute the class overlap between AUTSL, BosphorusSign22k and SignBridge's planned 150-sign vocabulary, and record licence/access conditions for each dataset.

# 5. Landmark Extraction (input to all models)

**MediaPipe Holistic** combines pose, face and hand models and outputs **543 landmarks per frame: 33 pose, 468 face and 21 per hand** [13], [17]. It is available for the web through the MediaPipe Tasks API (`@mediapipe/tasks-vision`, *Holistic Landmarker*); the current web guide documents the IMAGE and VIDEO running modes [14].

The literature consistently uses a **reduced subset** rather than all 543 points:

- OpenHands uses MediaPipe Holistic and selects **27 keypoints** (upper body, hands, face) [6].
- SAM-SLR uses an HRNet whole-body estimator (133 keypoints) reduced to a **27-node graph** (10 per hand, 7 upper body) [4].
- In the Kaggle ISLR competition, a 2nd-place team used 80 points for a CNN (both hands, lips, arms, brows, nose) and 61 points for a Transformer [17].

**Implications for SB-15:** (i) use Holistic, not Hands-only, because face/head cues carry grammar (Section 3.2); (ii) define a fixed, documented subset (≈ 27–80 points) and normalisation (e.g. shoulder-centred, scale-normalised); (iii) measure in-browser FPS on target hardware, since no published browser FPS figure for Holistic was found in the reviewed sources.

# 6. Architectures (RQ2)

## 6.1 Recurrent networks (LSTM / GRU)

LSTMs [7] model a landmark sequence step by step. They are small and fast: in OpenHands, an LSTM needs ≈ 8 ms per video on a Xeon CPU, an order of magnitude less than SL-GCN [6]. The AUTSL baselines are CNN + (Bi)LSTM models with attention [1]. **Weaknesses:** no explicit modelling of the spatial structure between joints, and the lowest accuracy among pose-based models on AUTSL (Section 7).

## 6.2 Transformers

Transformers [8] use self-attention over the whole sequence and parallelise well.

- **SPOTER** is a pose-based Transformer designed for low computational cost; it reports 63.18 % on WLASL100, 43.78 % on WLASL300 and 100 % on LSA64 [5].
- In OpenHands, a pose Transformer reaches **81.0 % on AUTSL** (MediaPipe input) [6].
- In the Kaggle ISLR competition, most top teams used 1D convolutions combined with Transformers, and a reduced-size BERT/DeBERTa Transformer reached 0.78 accuracy for one top team [17].
- For *translation*, Transformers are the standard: Sign Language Transformers jointly learn recognition and translation (Section 8) [11].

**Weaknesses:** data-hungry, and they do not encode the skeleton graph unless it is added explicitly.

## 6.3 Graph Convolutional Networks (GCN)

GCNs treat the skeleton as a graph (joints = nodes, bones = edges) and convolve over space and time.

- **ST-GCN** introduced spatial-temporal graph convolutions for skeleton-based action recognition [9].
- **SL-GCN** (part of SAM-SLR) adapts this to sign language. On AUTSL validation, SL-GCN alone reaches **95.02 % (joint stream)** and **95.45 % (four-stream ensemble)** using HRNet keypoints [4].
- The full SAM-SLR system (skeleton + RGB + depth ensemble) won the ChaLearn LAP 2021 challenge with **98.42 % (RGB track) and 98.53 % (RGB-D track)** on the AUTSL test set [3], [4]. *These are whole-system results, not GCN-only results.*
- In OpenHands with MediaPipe input, ST-GCN reaches **90.4 %** and SL-GCN **91.9 %** on AUTSL [6].

**Weaknesses:** more complex to implement and export; SL-GCN is the slowest model in OpenHands' CPU measurements (≈ 53 ms per video on a Xeon) [6].

# 7. Comparative Analysis

## 7.1 Same pipeline, same dataset

The fairest comparison found is OpenHands [6], where all four models use **the same MediaPipe Holistic input, the same AUTSL split and the same training data**:

| Model | AUTSL test accuracy | CPU latency per video (Xeon E5-2690 v4) | Notes |
|---|---|---|---|
| LSTM | 77.4 % | ≈ 8 ms | Fastest, least accurate |
| Transformer | 81.0 % | ≈ 31 ms | Simple to export |
| ST-GCN | 90.4 % | ≈ 23 ms | Best accuracy/speed trade-off |
| SL-GCN | 91.9 % | ≈ 53 ms | Most accurate, slowest |

*Source: [6]. Latency rankings vary by CPU; on an AMD Ryzen 7 3750H, ST-GCN was slower than the Transformer [6].*

## 7.2 Qualitative comparison

| Criterion | LSTM | Transformer | GCN (ST-GCN / SL-GCN) |
|---|---|---|---|
| Accuracy on AUTSL, MediaPipe input [6] | Lowest | Medium | **Highest** |
| Best reported pose-only AUTSL result | – | 81.0 % [6] | 95.45 % (HRNet, val.) [4] |
| Uses skeleton structure | No | Only if added | **Yes (built-in)** |
| Data needs | Low–medium | **High** | Medium |
| Inference cost | **Lowest** | Medium | Medium–high |
| Browser export (ONNX/TF.js) | Easy | Easy | Graph ops need care; must be tested |
| Suitable for translation (seq2seq) | Possible | **Standard** [11] | Used as encoder (e.g. GNN-T [18]) |

## 7.3 Evidence caveats

1. The 98.42 / 98.53 % SAM-SLR figures include RGB and depth; they are not achievable with landmarks alone.
2. HRNet keypoints [4] are more accurate than MediaPipe keypoints; OpenHands attributes its lower AUTSL score partly to this [6].
3. Random-split numbers (e.g. 95.95 % on AUTSL [1]) must never be compared with signer-independent numbers.

**Answer to RQ2.** For landmark-based isolated TİD recognition, GCNs are the most accurate family in like-for-like comparisons; Transformers are second and are the natural choice for translation and for simple browser export; LSTMs are the cheapest and are the right *baseline*.

# 8. Transfer Learning and Small Datasets (RQ3)

SignBridge plans to pre-train on a public dataset and fine-tune on its own 150-sign recordings. The literature supports this, with conditions:

- OpenHands shows that self-supervised pre-training (predictive coding, DPC) on pose data improves ST-GCN on INCLUDE from 91.2 % to 94.7 %, and that **the gain grows as labelled data shrinks**: 79.7 → 86.27 % with 10 samples per class, 45 → 57.35 % with 5 [6].
- Other pre-training strategies (masking, contrastive) gave little or no gain in the same study [6], so the pre-training method matters.
- Cross-lingual pre-training (Indian SL → other sign languages) improved low-resource fine-tuning, e.g. LSA64 with 3 samples per class from 39.7 % to 57.19 % [6].
- On BosphorusSign22k, a 3D-CNN fine-tuned from pre-trained weights reached 78.85 % top-1, compared with 57.76 % when trained from scratch [2]. This is an RGB result, but it shows the same pattern.

**Implications:** (i) SignBridge's 150 signs × 10 signers is a low-resource setting, so pre-training is necessary, not optional; (ii) class overlap with AUTSL/BosphorusSign22k (SB-12) determines how much transfer is possible; (iii) signer diversity matters more than repetitions by the same signer, because evaluation must be signer-independent.

# 9. Translation and Continuous Signing (RQ4)

## 9.1 Sign language translation

- **Neural SLT** [10] introduced end-to-end translation on RWTH-PHOENIX-Weather-2014T (German SL). Its Sign2Text model reached **9.58 BLEU-4 (test)**, and the two-step Sign2Gloss2Text reached **18.13** [10], [11].
- **Sign Language Transformers** [11] (a *later* paper by the same group) jointly train recognition and translation with CTC; the best model reaches **21.32 BLEU-4 (test) when tuned for translation** and 21.80 when tuned for recognition, with 24.49 % WER for recognition.

*Note:* 9.58 → 21.32/21.80 is a comparison between **two different papers** (2018 vs. 2020) on the same benchmark.

- **For TİD**, translation results are much lower: E-TSL's best model reaches 3.28 BLEU-4 [18]. In the opposite direction (Turkish → TİD gloss), a hybrid rule-based + statistical system reached 12.64 BLEU-4 on 3,561 sentence pairs [20].

**Implication:** full sentence-level TİD-to-Turkish translation is a research problem with no strong public baseline. A realistic scope for SignBridge is **isolated-sign recognition of a fixed vocabulary + gloss sequence + rule/LLM-assisted gloss-to-Turkish generation**, with gloss as the interface between modules (SB-14). For the Turkish → avatar direction, the rule-based findings in [20] (suffix removal, ŞİMDİ/BİTTİ tense markers, DEĞİL negation, fingerspelled proper nouns) can be used directly for the gloss schema.

## 9.2 Segmentation of continuous signing

SignBridge's proposal segments signs using pauses. The literature shows this is not sufficient:

- Moryossef et al. [12] detect *whether* someone is signing in real time from pose, which is useful as a first gate (signing vs. not signing).
- Moryossef et al. [15] show that continuous signing often has **no gap between signs**, and replace IO tagging with **BIO tagging** of signs and phrases. Their LSTM model on **MediaPipe Holistic** input reaches sign IoU 0.69 and phrase IoU 0.82–0.85 on the DGS corpus (vs. 0.46/0.70 for the earlier baseline) [15].

**Implication:** use a two-stage pipeline: (1) a lightweight signing/not-signing detector; (2) a BIO segmenter (or a sliding window with confidence thresholds) feeding the isolated recogniser. Pause-based segmentation can be the first prototype but must be evaluated against this.

# 10. Real-time, In-browser Deployment (RQ5)

The proposal targets in-browser inference (≥ 15 FPS landmark extraction, ≤ 2 s end-to-end latency). Relevant evidence:

- The Google ISLR competition required a **TFLite** model, ≈ **100 ms per video** and a **40 MB memory cap** [16], [17]. Top solutions under these limits used compact 1D-CNN + Transformer models [17], which shows that landmark-only, on-device sign recognition with a few hundred classes is feasible.
- OpenHands' CPU latencies (8–53 ms per video, Section 7.1) are well below a 2 s budget, so **landmark extraction, not the classifier, is the likely bottleneck** [6].
- Browser runtimes: models can be exported to ONNX and run with ONNX Runtime Web [21] or converted to TensorFlow.js [22]. LSTM and Transformer layers are widely supported. GCNs use graph/einsum operations that **must be tested for export** before committing to them.

**Implication for SB-15:** measure Holistic FPS and the classifier latency in the browser on a mid-range laptop and phone *before* finalising the model.

# 11. Consistency with the Project Proposal (SB-8)

| # | Proposal statement | Literature finding | Required change |
|---|---|---|---|
| 1 | The recogniser is a *keypoint-based Transformer* (Hypothesis H1) | On AUTSL with MediaPipe input, GCNs outperform the Transformer by ≈ 9–11 points [6] | Rephrase as *"a keypoint-based model; Transformer and GCN are the candidates, with an LSTM baseline, and the final choice follows the SB-13 evaluation protocol (Section 12)"*. H1 should not assume the architecture. |
| 2 | Pre-training on AUTSL only | BosphorusSign22k has 428 health-domain classes [2] | Add BosphorusSign22k to the dataset table; justify AUTSL vs. BosphorusSign22k after SB-12's overlap analysis. |
| 3 | MediaPipe Holistic as input | Consistent with [6], [14], [15] | Keep. State the selected landmark subset (Section 5). |
| 4 | O1: ≥ 85 % top-1 on unseen signers | Best MediaPipe-based AUTSL result is 91.9 % on 226 classes with 43 signers [6]; the custom set has only 10 signers | Split into a **target** (≥ 85 %) and a **minimum acceptable** value (e.g. ≥ 75 %), always measured signer-independently. |
| 5 | Pause-based segmentation | Gaps between signs are often absent [15] | Mention BIO segmentation [15] as the fallback/upgrade. |
| 6 | Sign-to-sentence translation | TİD SLT baseline is 3.28 BLEU-4 [18] | Limit the claim to vocabulary-bounded recognition + gloss-to-text. |

# 12. Recommendation for SignBridge

1. **Baseline (Sprint 2):** LSTM/GRU on the selected MediaPipe Holistic subset, trained on AUTSL with the official signer-independent split.
2. **Candidates:** (a) ST-GCN or SL-GCN; (b) a SPOTER-style pose Transformer. Train both on the same input and split.
3. **Decision criteria (in priority order):** signer-independent top-1 accuracy; in-browser latency and model size after ONNX/TF.js export; fine-tuning accuracy on the first SignBridge recordings.
4. **Expected outcome from the literature:** GCN wins on accuracy [4], [6]; the Transformer may win on ease of export. If the accuracy gap after export is < 3 points, prefer the model that is easier to deploy.
5. **Pre-training:** use self-supervised pose pre-training (DPC-style) before fine-tuning on the 150-sign set [6].
6. **Segmentation:** prototype with pauses, evaluate against a BIO segmenter [15].

# 13. Limitations of this Review

- Most comparable numbers come from a single like-for-like study [6]; results on other datasets may differ.
- No published in-browser FPS figure for MediaPipe Holistic was found; this must be measured (SB-15).
- Kaggle competition details are taken from the competition page and a participant write-up [16], [17], not from a peer-reviewed paper.
- This review did not run experiments; all recommendations must be confirmed in Sprint 2.

# 14. Conclusion

For landmark-based TİD recognition, the evidence favours GCN-based models on accuracy, Transformers on flexibility and translation, and LSTMs as a fast baseline. The most important methodological rule is to evaluate on **signer-independent** splits. The most important project risks are the small custom dataset (mitigated by pre-training), segmentation of continuous signing, and browser performance. The proposal should be updated so that the model choice follows the evaluation protocol in Section 12 instead of being fixed in advance.

# Appendix A — Traceability to SB-13

| SB-13 requirement | Where addressed |
|---|---|
| Comprehensive review of existing SLR models | Sections 2, 4, 6; 22 references |
| Comparison of Transformer vs. LSTM vs. GCN | Sections 6, 7 |
| Landmark-based | Sections 5, 7.1 |
| TİD focus | Sections 3.2, 4, 9.1 |
| Recognition *and translation* (title) | Sections 8, 9 |
| Usable for the project | Sections 10, 11, 12 |

# References

[1] O. M. Sincan and H. Y. Keles, "AUTSL: A large scale multi-modal Turkish Sign Language dataset and baseline methods," *IEEE Access*, vol. 8, pp. 181340–181355, 2020, doi: 10.1109/ACCESS.2020.3028072.

[2] O. Özdemir, A. A. Kındıroğlu, N. C. Camgöz, and L. Akarun, "BosphorusSign22k sign language recognition dataset," in *Proc. LREC 2020 9th Workshop on the Representation and Processing of Sign Languages*, 2020, pp. 181–188.

[3] O. M. Sincan, J. C. S. Jacques Junior, S. Escalera, and H. Y. Keles, "ChaLearn LAP large scale signer independent isolated sign language recognition challenge: Design, results and future research," in *Proc. IEEE/CVF CVPR Workshops*, 2021, pp. 3472–3481.

[4] S. Jiang, B. Sun, L. Wang, Y. Bai, K. Li, and Y. Fu, "Skeleton aware multi-modal sign language recognition," in *Proc. IEEE/CVF CVPR Workshops*, 2021, pp. 3413–3423.

[5] M. Boháček and M. Hrúz, "Sign pose-based transformer for word-level sign language recognition," in *Proc. IEEE/CVF WACV Workshops*, 2022, pp. 182–191.

[6] P. Selvaraj, G. NC, P. Kumar, and M. Khapra, "OpenHands: Making sign language recognition accessible with pose-based pretrained models across languages," in *Proc. 60th Annual Meeting of the ACL (Vol. 1: Long Papers)*, 2022, pp. 2114–2133.

[7] S. Hochreiter and J. Schmidhuber, "Long short-term memory," *Neural Computation*, vol. 9, no. 8, pp. 1735–1780, 1997.

[8] A. Vaswani *et al.*, "Attention is all you need," in *Advances in Neural Information Processing Systems 30 (NeurIPS)*, 2017.

[9] S. Yan, Y. Xiong, and D. Lin, "Spatial temporal graph convolutional networks for skeleton-based action recognition," in *Proc. AAAI Conference on Artificial Intelligence*, 2018.

[10] N. C. Camgöz, S. Hadfield, O. Koller, H. Ney, and R. Bowden, "Neural sign language translation," in *Proc. IEEE/CVF CVPR*, 2018, doi: 10.1109/CVPR.2018.00812.

[11] N. C. Camgöz, O. Koller, S. Hadfield, and R. Bowden, "Sign language transformers: Joint end-to-end sign language recognition and translation," in *Proc. IEEE/CVF CVPR*, 2020.

[12] A. Moryossef, I. Tsochantaridis, R. Aharoni, S. Ebling, and S. Narayanan, "Real-time sign language detection using human pose estimation," in *Proc. ECCV Workshops (SLRTP)*, 2020.

[13] I. Grishchenko and V. Bazarevsky, "MediaPipe Holistic — Simultaneous face, hand and pose prediction, on device," Google Research Blog, Dec. 2020.

[14] Google AI Edge, "Holistic landmark detection guide for Web," MediaPipe Solutions documentation. [Online]. Available: https://developers.google.com/edge/mediapipe/solutions/vision/holistic_landmarker/web_js (accessed 15.10.2026).

[15] A. Moryossef, Z. Jiang, M. Müller, S. Ebling, and Y. Goldberg, "Linguistically motivated sign language segmentation," in *Findings of the Association for Computational Linguistics: EMNLP 2023*, 2023.

[16] Google, Georgia Tech, and Deaf Professional Arts Network, "Google – Isolated Sign Language Recognition," Kaggle competition, 2023. [Online]. Available: https://www.kaggle.com/competitions/asl-signs (accessed 15.10.2026).

[17] "Isolated sign language recognition: 2nd place solution write-up (Kaggle ISLR 2023)," Habr, 2024. [Online]. Available: https://habr.com/en/articles/795109 (accessed 15.10.2026).

[18] Ş. Öztürk and H. Y. Keles, "E-TSL: A continuous educational Turkish Sign Language dataset with baseline methods," in *Proc. Int. Congress on Human-Computer Interaction, Optimization and Robotic Applications (HORA)*, 2024, doi: 10.1109/HORA61326.2024.10550648.

[19] U. Zeshan, "Aspects of Türk İşaret Dili (Turkish Sign Language)," *Sign Language & Linguistics*, vol. 6, no. 1, pp. 43–75, 2003, doi: 10.1075/sll.6.1.04zes.

[20] D. Kayahan and T. Güngör, "A hybrid translation system from Turkish spoken language to Turkish Sign Language," in *Proc. IEEE Int. Symp. on INnovations in Intelligent SysTems and Applications (INISTA)*, 2019, doi: 10.1109/INISTA.2019.8778246.

[21] Microsoft, "ONNX Runtime Web," ONNX Runtime documentation. [Online]. Available: https://onnxruntime.ai/docs/tutorials/web/ (accessed 15.10.2026).

[22] D. Smilkov *et al.*, "TensorFlow.js: Machine learning for the web and beyond," in *Proc. Machine Learning and Systems (MLSys)*, 2019.
