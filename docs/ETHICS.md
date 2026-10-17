# Ethics Committee & Data Privacy Compliance (SignBridge-TR)

> **Status:** DRAFT — committee name and exact document list must be confirmed
> with the advisor and Yaşar University's research/ethics office before submission.
> Jira: SB-9. Owner: Emir Ersan.

## 1. Purpose
This document records (a) whether SignBridge-TR needs ethics committee approval,
(b) which committee it goes to, and (c) what must be submitted and when. The
participant-facing forms live under [`docs/consent/`](consent/).

## 2. Do we need ethics approval? — our analysis

**Short answer: most likely yes, triggered by the user study (not by training data).**

| Activity | Real human participants? | Personal / special-category data? | Triggers ethics review? |
|---|---|---|---|
| Model training | No — we use existing/found datasets (e.g. AUTSL). We are **not** recording our own signers. | No new personal data collected by us | No (only dataset licence compliance + citation) |
| **User study / usability test** | **Yes** — Deaf and other volunteers use the app | **Yes** — session audio + video recordings (face/hands, voice), app-usage/performance data, SUS survey, interviews, and participants' disability status (health data) | **Yes** |

Why the user study triggers it:
- It involves **real human participants**, which is the actual trigger for ethics
  review — recording sign language is **not** the trigger by itself.
- We **record audio and video** of participants. These are **personal data**. They are
  **not** special-category "biometric" data here, because biometric data is personal data
  processed **for the purpose of uniquely identifying** a person (KVKK Art. 6 / GDPR
  Art. 4(14)), and this study does **not** process the recordings for identification.
  Processing them still requires the participant's consent.
- Participants' **disability status (hearing impairment)** is **health data**, which is
  **special-category personal data** under KVKK Art. 6 / GDPR Art. 9 — on its own it
  requires *explicit consent*, even if nothing were recorded.

> Note on the product vs. the study: in normal product operation raw video is
> never stored — only anonymous keypoints and text leave the device. The
> recordings covered here are **study-session recordings kept for evaluation**,
> which is a separate activity and is what the consent forms authorise.

## 3. Which committee?  *(to be confirmed)*
Turkish universities usually run several ethics committees. A non-medical,
non-interventional engineering study that collects data from human participants
normally goes to a **social-sciences / human-research (non-interventional)**
committee — **not** a clinical ("Girişimsel Olmayan Klinik Araştırmalar")
committee.

- **Action:** confirm with advisor (Dr. Öğr. Üyesi Kazım Erdoğdu) and/or Yaşar's
  research office: the exact committee name, whether a ready template/form exists,
  and the meeting calendar.
- **Placeholder until confirmed:** *Yaşar University [Social & Human Sciences /
  Non-interventional] Research Ethics Committee.*

## 4. Documents typically required for the application
(Confirm the exact set from the committee's own checklist.)
- Application form (committee's own form)
- Short project summary / research protocol (purpose, method, participants, data)
- Participant information & consent documents — see [`docs/consent/`](consent/)
- Data management note: what is collected, where/how long it is stored, who has
  access, how it is anonymised, when it is deleted
- Measurement instruments: SUS questionnaire + interview question list
- Researcher & advisor details; advisor's approval/signature

## 5. Submission steps & timing
1. Confirm committee + obtain its form/checklist (§3).
2. Fill the application form; attach the §4 documents.
3. **Advisor signs** as the responsible investigator — a student normally cannot
   apply alone.
4. Submit to the committee secretariat before its meeting cut-off.
5. Wait for the decision; only **after approval** may recording/testing begin.

> **Why apply early (now, not at test time):** committees usually meet about once
> a month, approval can take weeks, and most committees will **not** review a study
> that has **already started**. The proposal commits us to apply in the first month
> for this reason.

## 6. Links (fill in)
- Consent forms: [`docs/consent/`](consent/)
- Committee page / regulation: _TBD_
- Related Jira issue: SB-9
- Pull Request: https://github.com/EgeErdem35/signBridge/pull/12
