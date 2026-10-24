# Ethics Committee & Data Privacy Compliance (SignBridge-TR)

> **Status:** DRAFT — pending advisor and institutional review.
> The committee, required documents and unresolved data-processing decisions
> must be confirmed before submission or participant activities.
>
> **Revision:** SB-19 draft — 24 October 2026.
> **Original task:** SB-9. Original documentation owner: Emir Ersan.
> **Current task:** SB-19 — Share Ethics Documentation with Advisor.
> **Current task owner:** Yasmin Malgir.
> **Alignment source:** SB-18 proposal v1.1, r5 draft, 23 October 2026.
>
> This document does not record an ethics application, approval or advisor
> endorsement of the proposed protocol.

## 1. Purpose

This document records:

- The research activities requiring advisor and ethics review.
- The proposed application data flows and research-data handling.
- The decisions and documents to confirm with the advisor.
- The actual sharing and application status.

The advisor will guide the ethics committee process. The exact committee,
submission procedure, responsible investigator and required signatures
remain to be confirmed.

Participant-facing documents:

- [Turkish information and consent draft](consent/onam-formu-TR.md)
- [English information and consent draft](consent/consent-form-EN.md)

These forms remain drafts. They must be aligned with the agreed protocol
and applicable institutional requirements before participant use.

## 2. Related Work and Current Status

### AUTSL access — SB-16

The team contacted the AUTSL authors, received access instructions and
accessed dataset files. Completeness and integrity checks for the full
local dataset remain a separate verification step.

Dataset access and related correspondence are tracked under
[SB-16](https://el-dili.atlassian.net/browse/SB-16).

Access does not by itself establish permission to redistribute source
recordings, derived landmarks or animations. Applicable usage terms and
any additional permissions must be checked.

### Participant recruitment enquiry — SB-20

Initial contact has been made with Yaşar University's Disabled Student
Unit to ask about approximate eligible student numbers and the possible
distribution of a future voluntary participation invitation. No individual
student details were requested.

The enquiry and subsequent responses are tracked under
[SB-20](https://el-dili.atlassian.net/browse/SB-20).

This contact does not establish that participants have been recruited or
that participant testing has been authorised. Recruitment arrangements
remain subject to confirmation.

Private correspondence is not reproduced here. Dataset passwords, private
access links and participant information must not be published in the
repository.

## 3. Research Activities and Approval Conditions

| Activity | Planned approach | Review and conditions |
|---|---|---|
| Training with existing datasets | Prioritise AUTSL, with BosphorusSign22k as the alternative described in the proposal. | Check licence terms, permitted processing and citation requirements. Confirm any institutional requirements for secondary use with the advisor. |
| Simulated-condition pre-tests | Volunteers complete evaluation tasks under defined simulated conditions. | These are participant activities. No participant pre-test begins before applicable ethics approval and informed consent. |
| Target-user evaluation | Suitable Deaf/hard-of-hearing TİD users, blind users and other relevant volunteers evaluate the application if they can be reached. | No participant evaluation begins before applicable ethics approval and informed consent. |
| Supplementary training recordings | Not currently scheduled; a conditional option if the coverage audit demonstrates a need. | Require advisor agreement, applicable ethics approval, informed consent and appropriate data-use arrangements before collection. |

### Existing datasets

The team must check the applicable terms before processing or sharing
dataset materials, derived landmarks or animations.

### Evaluation

Evaluation may include task completion measurements, accuracy and latency
results, application interaction records, SUS questionnaires and interviews.

Simulated pre-tests and target-user evaluation are reported separately,
with actual participant numbers, groups and limitations. Simulated results
do not establish usability for Deaf or blind users.

Disability-related eligibility information must be limited to what the
approved protocol needs and handled as sensitive participant information.

### Supplementary training recordings

The current plan prioritises existing datasets. Any supplementary recording
requires a separate, agreed collection protocol.

Evaluation data are research data and are not reused for training under
the current plan. The usability consent forms do not automatically cover
a separate training-data collection activity.

## 4. Application Data Flows

The table describes the proposed application design, not a completed
implementation or a verified network-traffic audit.

| Data | Processing and possible transfer | Storage and open decisions |
|---|---|---|
| Raw camera video | Processed on the device by MediaPipe. Never transmitted by the application. | Not stored by the application. |
| Microphone audio | Used for speech-to-text and voice commands. May leave the device if an external speech service or server-based browser recognition is used. | Not stored by the application. Provider processing, location and retention must be confirmed. |
| Landmark sequences | Processed on the device. May be sent to the project's back-end only if server-assisted classification is selected. | Not stored under the proposed application design. Whether transmission is needed remains undecided. |
| Glosses and Turkish text | Used by the back-end, LLM and TTS components. May be processed by external services depending on the selected deployment. | Providers, logs, caches and retention must be defined before participant evaluation. |

Landmarks must not be described as automatically anonymous. Their
identifiability and protection requirements depend on the actual processing.

Before selecting external STT, LLM, TTS or browser speech services, their
processing terms must be reviewed with the advisor and the relevant
institutional office as needed. No provider, processing location, retention
period or absence of third-party transfer is assumed.

The application's camera-video policy is separate from any research-session
recording. A session recording, if proposed, must be explicitly described in
the research protocol and participant information.

## 5. Research Data and Consent Drafts

The proposed evaluation may collect:

- Task completion, accuracy and latency measurements.
- Application usage and interaction records.
- SUS questionnaire and interview responses.
- Necessary participant eligibility information.
- Participant information and consent records.
- Session audio or video, only if included in the agreed and approved protocol.

Whether evaluation sessions will be recorded on audio or video is not yet
decided. Both consent drafts must reflect the agreed recording decision
before participant use.

Scripted, fictional service scenarios and no real patient data are proposed
for evaluation. This remains subject to team and advisor confirmation.

The protocol and both consent forms must consistently specify:

- Data categories, purposes and collection methods.
- Whether recording is required, optional or excluded.
- Data-controller identity and participant contact details.
- Storage location, authorised access and security measures.
- External services and any data transfers.
- Retention and deletion arrangements.
- Withdrawal procedures and any limits after irreversible anonymisation.
- Accessible information and consent procedures.

The appropriate legal basis, privacy wording and any references to legislation
must be confirmed through the institutional review process. This document
does not establish legal compliance by itself.

Bracketed fields remain clearly marked until confirmed. Participant names,
signed forms, identifiable recordings and private correspondence must not
be committed to the public repository.

## 6. Which Committee? — To Be Confirmed

The exact committee name must be confirmed with Dr. Öğr. Üyesi Kazım Erdoğdu
and, where necessary, Yaşar University's relevant research or ethics office.

Do not assume a committee name or submission route.

Questions for the advisor:

1. Which ethics committee should receive the application?
2. Which official forms, supporting documents and signatures are required?
3. Who should be named as the responsible investigator and data controller?
4. Which contact details should appear in the consent forms?
5. Should evaluation sessions include audio or video recordings?
6. What storage, retention, access, deletion and withdrawal arrangements
   should be used?
7. How should external speech, LLM and TTS services and associated data
   transfers be addressed?
8. What additional review and consent materials would be needed if
   supplementary training recordings become necessary?
9. What are the application deadlines and expected review schedule?

Committee page, official checklist and confirmed decisions will be recorded
after they are provided or verified.

## 7. Application Documents — Working List

The following list is for preparation. It is not a confirmed committee
checklist.

- The committee's official application form.
- Project summary and research protocol.
- Turkish and English participant information and consent forms.
- Recruitment materials and eligibility criteria.
- Evaluation tasks, SUS questionnaire and interview questions.
- Data-management and external-service information.
- Researcher and advisor details and required signatures.
- Separate supplementary-recording materials, if that activity is proposed.

The advisor and the committee's official instructions determine the final
requirements.

## 8. Submission Steps and Timing

1. Align this document and both consent drafts with the revised proposal.
2. Obtain team review through the SB-19 pull request.
3. Send ETHICS.md and both consent drafts to the advisor, labelled as drafts,
   and ask the questions in Section 6.
4. Record the actual sending date, exact versions shared and response status
   in this document and Confluence.
5. Revise the documents following advisor and institutional feedback.
6. Confirm the committee and submit the required materials through the
   agreed process.
7. Begin participant activities only after applicable approval and informed
   consent requirements are satisfied.

The proposal plans an application in the first semester and allows for an
estimated review period of two to three months. The actual deadlines and
review duration must be confirmed with the institution.

No participant test, including simulated pre-tests, begins before approval.
Any supplementary training recording must also satisfy its separate
approval, consent and data-use conditions.

Sending documents to the advisor is not submission to an ethics committee
and is not ethics approval.

## 9. Advisor Sharing and Application Record

| Item | Current record |
|---|---|
| SB-19 document sharing | Pending — sending not yet recorded |
| Actual sending date | Not yet recorded |
| Intended recipient | Advisor: Dr. Öğr. Üyesi Kazım Erdoğdu |
| Documents to share | ETHICS.md; onam-formu-TR.md; consent-form-EN.md |
| Exact versions or commit reference sent | To be recorded after sending |
| Advisor response and decisions | Not yet recorded |
| Confluence record | Link to be added |
| SB-19 Pull Request | Link to be added |
| Confirmed committee and official checklist | Not yet recorded |
| Ethics application date and reference | Not yet recorded |
| Ethics approval date and reference | No approval recorded |

Update this record only after the relevant action occurs. Keep any sending
evidence in an appropriate restricted location. Do not publish private
e-mail content or personal contact details.

## 10. Links and Revision History

- Consent drafts: [docs/consent/](consent/)
- Original Jira task:
  https://el-dili.atlassian.net/browse/SB-9
- Original documentation Pull Request:
  https://github.com/EgeErdem35/signBridge/pull/12
- Current advisor-sharing task:
  https://el-dili.atlassian.net/browse/SB-19
- AUTSL access task:
  https://el-dili.atlassian.net/browse/SB-16
- Disabled Student Unit contact task:
  https://el-dili.atlassian.net/browse/SB-20
- Committee page and regulations: to be confirmed.

### SB-19 draft revision — 24 October 2026

- Aligned the documentation with the SB-18 v1.1 r5 proposal draft.
- Added related-work references to SB-16 and SB-20 without reproducing
  private correspondence.
- Replaced the blanket no-own-recording statement with the conditional
  supplementary-recording approach.
- Distinguished application processing, evaluation data and training data.
- Removed the assumption that landmarks are anonymous.
- Marked session recording, service selection and retention as unresolved.
- Added advisor questions and a sharing/application record.
- Preserved the SB-9 documentation history.
