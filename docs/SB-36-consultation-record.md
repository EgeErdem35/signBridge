# SB-36 – Consultation Record: Datasets, Participant Testing and Supplementary Recordings

**Issue:** SB-36
**Owner:** Emir Ersan
**Advisor:** Dr. Öğr. Üyesi Kazım Erdoğdu
**Consultation date:** 11 November 2026
**Related issues:** SB-9 (consent form drafts), SB-19 (ethics documentation), SB-20 (disability unit contact), SB-37 (data-flow policy)
**Related milestone:** Advisor Review 2 (2 November 2026)

## 1. Status Note

> This document records **verbal guidance** received during an informal
> consultation on 11 November 2026. It is verbal guidance, **not** an ethics
> committee decision.
>
> The guidance was given verbally and has not been confirmed in writing.
> It has not yet been shared with the advisor. Until the advisor has
> reviewed it, the conditions in [ETHICS.md](ETHICS.md) remain the project's
> working position.

## 2. Scope of Questions

The questions were grouped into three separate areas, plus one additional
question.

| Area | Topic | Question asked |
|---|---|---|
| A | Existing dataset use | Can the team use AUTSL (Ankara University, academic/non-commercial licence) for model training and experiments, and show sample frames in reports and demos? |
| B | Participant evaluation | What steps are needed before contacting Deaf / TİD-using volunteers for usability testing, and what is required for consent and testing? |
| C | Supplementary collection | What is required if AUTSL is insufficient and new sign video/audio recordings are needed? |
| Extra | External services | What applies to sending audio, text or landmarks to external services (for example cloud speech-to-text)? |

## 3. Consultation Log

| # | Date | Unit contacted | Attended by | Response | Referral |
|---|---|---|---|---|---|
| 1 | 11 November 2026 | BTTO / Project Support Office | Emir Ersan | Stated that the topic is outside the office's scope. No guidance on the questions was given. | Referred to the Head of the Software Engineering Department. |
| 2 | 11 November 2026 | Head of the Software Engineering Department | Emir Ersan | Verbal guidance on areas A, B and C (see Section 4). The external services question was not answered. | Supplementary recordings: consult the Department Head again before recording. |

Both contacts were in person. No written response was received.

## 4. Guidance Received

All points below are verbal guidance from the Head of the Software
Engineering Department. They are recorded as understood by the attendee and
are conditional on the project remaining academic and non-commercial.

### A. Existing dataset use

- For an academic, non-commercial project, no ethics committee application
  was indicated as necessary for using AUTSL.
- Showing sample frames publicly was not specifically addressed. The AUTSL
  licence terms still apply (see open item 6).

### B. Participant evaluation

- If volunteers (including Deaf users) only use the application, with no
  experiment and no personal data collection, no ethics committee
  application was indicated as necessary.
- Participants must sign an information form and a KVKK notice stating that
  camera image and audio are used during the session but are not stored by
  the project's system.

### C. Supplementary collection

- If the dataset is insufficient and new recordings of people are needed,
  the Department Head must be consulted before any recording takes place.

### Extra. External services

- Not answered. No guidance was received on sending audio, text or
  landmarks to external services.

## 5. Classification

| Topic | Classification | Reason / condition |
|---|---|---|
| AUTSL for training and internal experiments | Can proceed now | Consistent with the verbal guidance and with existing SB-16 access. Licence terms continue to apply. |
| AUTSL sample frames in public reports or demos | Needs confirmation before acting | Licence terms must be checked first (open item 6). |
| Usability testing with volunteers | Needs confirmation before acting | Requires the information + KVKK notice form (open item 3), the anonymous feedback design (open item 2) and advisor review of this guidance (open item 1). ETHICS.md currently requires ethics approval before participant tests (open item 8). |
| "Not stored" claim in participant information | Needs confirmation before acting | Holds only if speech-to-text runs on the device or the external provider also does not store data (open item 4). |
| External services (audio, text, landmarks) | Needs confirmation before acting | Question not answered. To be resolved under SB-37 and with the advisor. |
| Supplementary recordings (including team members) | Referred unit: Head of the Software Engineering Department | Must be consulted before any recording (open item 5). |
| Any change to the academic/non-commercial status | Referred unit: Head of the Software Engineering Department | All guidance above depends on this status (open item 7). |

## 6. Open Items

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Share the consultation outcome with the advisor at the next meeting. | Emir Ersan | Pending |
| 2 | Limit usability feedback to anonymous, non-identifying data: task completion, difficulty, 1–5 satisfaction and a free comment. No names, no stored video/audio, no disability status linked to a person and no combinable demographics. | Team | Decided |
| 3 | Adapt the SB-9 consent drafts into an information + KVKK notice form (TR/EN). To be tracked as a follow-up issue before the Spring 2027 usability test. | Emir Ersan | Pending (follow-up issue) |
| 4 | Decide on on-device or external speech-to-text. If external, the "not stored" claim must also hold for the third party. Linked to the SB-37 data-flow policy. | Team | Pending |
| 5 | Consult the Department Head before any supplementary recording, including recordings of team members. | Team | Conditional (only if recordings are needed) |
| 6 | Check the AUTSL licence terms before showing sample frames publicly. | Team | Pending |
| 7 | Re-consult if the project stops being academic and non-commercial. | Team | Noted |
| 8 | ETHICS.md requires ethics approval before participant tests; reconcile with the Department Head's verbal guidance after the advisor's view. | Emir Ersan | Pending |

Pending responses:

- External services question: no answer received from any unit.
- Advisor review of this guidance: not yet requested (open item 1).

## 7. Privacy Note

Apart from the team member and the project advisor, people are referred to
by role only. This record contains
no e-mail addresses, phone numbers, private messages or other personal
details.

## 8. References

- Jira issue: https://el-dili.atlassian.net/browse/SB-36
- Ethics and data privacy draft: [ETHICS.md](ETHICS.md) (SB-9, SB-19)
- Consent drafts: [docs/consent/](consent/) (SB-9)
- Disability unit contact: [SB-20-disability-unit-contact.md](SB-20-disability-unit-contact.md)
- AUTSL access request: [datasets/SB-16_AUTSL_Access_Request.md](datasets/SB-16_AUTSL_Access_Request.md)
- Data-flow policy: https://el-dili.atlassian.net/browse/SB-37
