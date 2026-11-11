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
> reviewed it, [ETHICS.md](ETHICS.md) remains the project's working policy.
> Nothing in this record removes or relaxes an ETHICS.md requirement.

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
They are not current project policy; the requirements in ETHICS.md continue
to apply until the advisor has reviewed this guidance.

### A. Existing dataset use

- For an academic, non-commercial project, no ethics committee application
  was indicated as necessary for using AUTSL.
- Showing sample frames publicly was not specifically addressed. The AUTSL
  licence terms still apply (see open item 7).

### B. Participant evaluation

- If volunteers (including Deaf users) only use the application, with no
  experiment and no personal data collection, no ethics committee
  application was indicated as necessary.
- The guidance stated that participants must sign an information form and a
  KVKK notice stating that camera image and audio are used during the
  session but are not stored by the project's system.

### C. Supplementary collection

- If the dataset is insufficient and new recordings of people are needed,
  the Department Head must be consulted before any recording takes place.

### Extra. External services

- Not answered. No guidance was received on sending audio, text or
  landmarks to external services.

## 5. Classification

| Topic | Classification | Reason / condition |
|---|---|---|
| AUTSL for training and internal experiments | Can proceed under current ETHICS.md conditions | Uses existing SB-16 access. The ETHICS.md conditions for existing datasets still apply: check licence terms, permitted processing and citation requirements; confirm any institutional requirements for secondary use with the advisor; check the applicable terms before processing or sharing dataset materials, derived landmarks or animations. Access does not by itself permit redistribution of source recordings, derived landmarks or animations. The verbal guidance does not remove any of these conditions. |
| AUTSL sample frames in public reports or demos | Needs confirmation before acting | Licence terms must be checked first (open item 7). |
| Usability testing with volunteers | Needs confirmation before acting | Requires the information + KVKK notice form (open item 4), the agreed privacy constraint (open item 2), the final evaluation protocol, which is still pending (open item 3), and advisor review of this guidance (open item 1). Under ETHICS.md, no participant test begins before applicable ethics approval and informed consent (open item 9). |
| "Not stored" claim in participant information | Needs confirmation before acting | Holds only if speech-to-text runs on the device or the external provider also does not store data (open item 5). |
| External services (audio, text, landmarks) | Needs confirmation before acting | Question not answered. To be resolved under SB-37 and with the advisor. |
| Supplementary recordings (including team members) | Referred unit: Head of the Software Engineering Department | Must be consulted before any recording (open item 6). Consultation is not the only prerequisite: any supplementary recording also remains subject to the ETHICS.md protocol requirements of advisor agreement, applicable ethics approval, informed consent and data-use arrangements. |
| Any change to the academic/non-commercial status | Referred unit: Head of the Software Engineering Department | All guidance above depends on this status (open item 8). |

## 6. Open Items

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Share the consultation outcome with the advisor at the next meeting. | Emir Ersan | Pending |
| 2 | Privacy constraint for usability feedback: anonymous and non-identifying; no names, no stored video/audio, no disability status linked to a person and no combinable demographics. Free-text responses: participants are told not to include names or identifying details; any identifying detail that appears is removed before the response is stored; free text is never linked to a person. | Team | Agreed (privacy constraint only) |
| 3 | Final evaluation protocol and metrics. Task completion, difficulty, 1–5 satisfaction and a free comment are proposed only; ETHICS.md also lists SUS questionnaires and interviews as possible measures. | Team | Pending (to be finalised with the advisor under ETHICS.md) |
| 4 | Adapt the SB-9 consent drafts into an information + KVKK notice form (TR/EN). To be tracked as a follow-up issue before the Spring 2027 usability test. | Emir Ersan | Pending (follow-up issue) |
| 5 | Decide on on-device or external speech-to-text. If external, the "not stored" claim must also hold for the third party. Linked to the SB-37 data-flow policy. | Team | Pending |
| 6 | Consult the Department Head before any supplementary recording, including recordings of team members. Consultation is not the only prerequisite: any supplementary recording also remains subject to the ETHICS.md protocol requirements of advisor agreement, applicable ethics approval, informed consent and data-use arrangements. | Team | Conditional (only if recordings are needed) |
| 7 | Check the AUTSL licence terms before showing sample frames publicly. | Team | Pending |
| 8 | Re-consult if the project stops being academic and non-commercial. | Team | Noted |
| 9 | ETHICS.md requires ethics approval before participant tests; reconcile with the Department Head's verbal guidance after the advisor's view. | Emir Ersan | Pending |

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
