# SignBridge-TR — Participant Information, Research Participation Consent and Personal Data Documents

> **DRAFT — For advisor and institutional review; not ready for participant signatures.**
>
> Bracketed fields and unresolved decisions must be completed according to
> the approved research protocol. No participant testing or research
> recording begins before the required ethics approval and informed
> consent. This condition also applies to volunteer pre-tests under
> simulated conditions.
>
> **Version / date:** v1.3 — SB-19 draft, 24 October 2026.
> **Alignment sources:** SB-18 proposal v1.1, r6, 24 October 2026;
> [ETHICS.md](../ETHICS.md).
>
> Research participation consent, the KVKK privacy notice and explicit
> consent are presented as separate sections with separate declarations.

## Preparation Note for the Research Team

This section is for preparation. Resolve open decisions and remove
preparation notes before presenting the documents to participants.

- Confirm participant groups, eligibility criteria, tasks and session
  duration. Under R6 decision D-23, blind-specific features and related
  evaluation remain subject to a team/advisor decision; general
  accessibility remains in scope. This draft does not resolve D-23.
- Decide whether audio and video will be recorded. If recording is
  planned, specify separately whether each is required or optional and
  how refusal affects participation. Remove unused recording options
  from the final text.
- Confirm the data controller, responsible investigator, contact
  details, specific legal basis for each processing activity,
  retention periods and transfer arrangements with the institution.
- Check the data flows of the application version used in the study.
  Do not process participant data through external services before
  identifying the providers and explaining the transfer arrangements.
- Report simulated-condition pre-tests separately from target-user
  evaluation. Do not present simulated results as usability findings
  for the corresponding target-user group.
- This form covers evaluation. Under the current plan, evaluation data
  are not reused for model training. Conditional supplementary
  training-data collection requires a separate protocol, the necessary
  approvals, consent and data-use arrangements.
- Do not upload signed forms, participant identities, identifiable
  recordings or private correspondence to the public GitHub repository.

---

## Section A — Participant Information and Research Participation Consent

### A.1. Study Details

**Study title:** Usability and performance evaluation of the
SignBridge-TR Turkish Sign Language ↔ Turkish communication prototype.

**Institution:** Yaşar University, Faculty of Engineering, Department
of Software Engineering — Capstone Project (SE4910/SE4920).

**Project advisor:** Dr. Kazım Erdoğdu.

**Responsible investigator:**
[Name, title and role to be confirmed by the institution].

**Research team:** [Names and roles].

**Study contact details:**
[Institutional email and suitable communication method].

**Ethics committee:** [Committee name to be confirmed].

**Ethics approval details:**
[Date and decision/application reference to be entered after approval].

**Nature of the study:** An academic capstone project with no
commercial purpose.

### A.2. Why Are You Being Invited?

SignBridge-TR is a browser-based prototype intended to support
communication between Turkish Sign Language and Turkish text and
speech within a selected vocabulary and limited scenarios. In the
initial version, sign recognition is limited to isolated signs and
signs separated by short pauses. The system does not claim to provide
reliable translation of unrestricted continuous TİD signing.

This study aims to evaluate the usability, understandability and
performance of the agreed features.

**Your participant group and eligibility criteria:**
[To be explained according to the approved protocol].

**Type of evaluation you will participate in:**
[Simulated-condition pre-test / target-user evaluation;
clearly specify the applicable type].

### A.3. What Will You Be Asked to Do?

During a session lasting approximately [minutes], you will complete
[tasks, input/output methods and number of repetitions]. You will
then be asked to complete [SUS usability questionnaire, if applicable]
and participate in [interview and duration, if applicable].

If scenarios are included in the approved protocol, fictional
information will be used. You will not be asked to share real patient
information or private information about other people.

The application is a research prototype and may produce incorrect
results. Its outputs during testing will not be used for real
healthcare, emergency or similarly consequential decisions.

### A.4. Application Processing and Session Recording

Under the proposed application design, camera video is processed
on the device to extract hand, face and body landmarks. The application
does not store or transmit raw camera video. Landmarks are not
automatically anonymous; they may be sent to the project's back-end
if server-assisted classification is selected.

Microphone audio may be used for speech-to-text or voice commands.
Audio may leave the device if an external speech service or
server-based browser recognition is selected. Under the proposed
design, the application does not store microphone audio; provider
processing and retention will be explained separately. Sign labels
(glosses) and Turkish text may also be processed by the selected
language-model or text-to-speech services.

**Verified data flows and services used in this session:**
[To be specified consistently with Section B].

A separate audio or video recording of the research session is
different from the application's live camera/microphone processing.

**Research-session recording decision:**
[No recording / audio only / video only / audio and video;
to be confirmed].

**If recording is planned:**
[Explain what will be recorded, why, whether it is required or
optional, and how refusing recording affects participation].

Recording will not begin before the relevant information has been
provided and the necessary consent obtained.

### A.5. Voluntary Participation and Withdrawal

Participation is voluntary. You will not face any penalty for
declining or withdrawing without giving a reason. You may take
a break or stop the session at any time.

You may request withdrawal through [communication method].
The use and deletion of research data that can be linked to you
will be handled according to the process and applicable obligations
explained below. Once data have been irreversibly anonymised,
it may no longer be possible to identify and remove your contribution.

**Withdrawal and deletion procedure; timing of anonymisation
and any retention exceptions:** [To be clearly specified].

### A.6. Possible Risks and Benefits

Tasks may cause fatigue, communication difficulties or discomfort
due to incorrect results. Collecting personal data also creates
a risk of loss of confidentiality. Breaks, stopping the session
and the data-security measures described below will be used to
reduce these risks.

No direct personal benefit is guaranteed. Your feedback may help
improve the prototype.

**Payment, incentives or reimbursement:**
[None / explain any applicable arrangements].

### A.7. Accessible Information

Information and tasks will be provided in a form appropriate to your
communication needs. [Specify the support that will actually be
available, such as written explanations, accessible digital text,
screen-reader support, a TİD interpreter or other assistance].

You will have sufficient time to ask questions and decide whether
to participate. If an interpreter or support person is present,
their role and confidentiality arrangements will be explained.
Their presence does not replace your own participation decision.

### A.8. Research Participation Declaration

The study's purpose, tasks, possible risks, voluntary nature and
withdrawal process have been explained to me in a way I can understand.
I have had the opportunity to ask questions and receive answers.
I agree to participate voluntarily in this research.

This declaration does not replace the personal-data choices in
Section C or authorise processing that has not been explained.

**Participant** — Full name: __________________
Date: __________ Signature: __________

**Researcher providing the information** — Full name: __________________
Date: __________ Signature: __________

**Interpreter / witness, if applicable** — Full name and role: __________________
Date: __________ Signature: __________

[If a participant group requiring a legal representative is planned,
the institutionally approved participation and consent arrangements
must be specified here. This draft does not automatically cover
such participation.]

---

## Section B — Draft KVKK Privacy Notice on Personal Data Processing

> **Preparation note:** This notice provides information; it does not
> request approval or consent. It must not be presented as the final
> participant privacy notice until the institution has confirmed the
> data controller, specific legal bases and the fields below.

### B.1. Data Controller and Contact Details

**Data controller:**
[Full institutional name and address confirmed by the institution].

**Contact and rights-request channel:**
[Verified contact details and request procedure].

### B.2. Data, Purposes and Legal Bases

Only data necessary for the approved protocol will be collected.
Diagnostic documents or detailed medical histories will not
automatically be requested.

| Data category | Purpose | Collection method and specific applicable legal basis |
|---|---|---|
| Necessary identity, contact and consent information | Document participation/consent and maintain necessary communication | [Fields collected, method and specific legal basis] |
| Necessary eligibility information | Determine eligibility for the approved participant group | [Minimum fields, method and specific legal basis; identify any health data separately] |
| Task completion, accuracy, latency and interaction data | Evaluate usability and performance | [Measurements and log fields; specific legal basis] |
| Questionnaire and interview responses | Evaluate user experience | [Instruments and collection method; specific legal basis] |
| Live application processing of camera video, landmarks, audio and text | Support recognition, speech-to-text, language processing or text-to-speech during tasks | [Actual data, on-device/server processing and specific legal basis for each activity] |
| Research-session audio recording — only if agreed | [Specific evaluation purpose requiring recording] | [Recording method and specific legal basis; remove this row if no audio recording is planned] |
| Research-session video recording — only if agreed | [Specific evaluation purpose requiring recording] | [Recording method and specific legal basis; remove this row if no video recording is planned] |

The legal classification of the data and appropriate legal bases
will be confirmed by the institution based on the actual processing.
Audio, video and landmarks will not automatically be assumed to be
anonymous or outside a particular legal category.

Evaluation data will not be used for model training under the current
plan. This notice does not authorise separate training-data collection.

### B.3. Access and Transfers

People who may access research data as required for their duties:
[Authorised roles and access limits].

External services used by the application will be explained separately
from the location used to store research data. The following details
will be completed for the final version:

| Service / recipient | Data processed or transferred | Purpose, processing location and any international transfer | Specific transfer basis and provider retention arrangements |
|---|---|---|---|
| [Speech-to-text / browser speech service] | [Audio and related information] | [To be confirmed] | [To be confirmed] |
| [Project back-end / language-model / text-to-speech service] | [Landmarks, glosses, text or other information actually transmitted] | [To be confirmed] | [To be confirmed] |
| [Research-data storage service, if applicable] | [Research data stored] | [To be confirmed] | [To be confirmed] |

Remove unused rows and add any other recipients. This draft does not
establish whether international transfers occur and does not request
blanket consent for transfers.

### B.4. Retention, Security and Deletion

| Data group | Storage location and authorised access | Retention period / deletion or anonymisation time |
|---|---|---|
| Identity, contact and signed consent records | [To be confirmed; kept separately from analysis data] | [Period, starting event and any mandatory retention reason] |
| Eligibility information and participant-code mapping | [To be confirmed] | [To be confirmed] |
| Measurements, interaction records, questionnaire and interview responses | [To be confirmed] | [To be confirmed] |
| Research audio/video recordings, if applicable | [To be confirmed] | [To be confirmed, including backup copies] |
| Provider logs, caches and other service records, if applicable | [To be confirmed for each provider] | [To be confirmed for each provider] |

Proposed measures include authorised access, appropriate password
and encryption measures, participant codes, separate storage of
identity mappings and deletion at the agreed times. The measures
to be implemented will be finalised in the data-management plan.

Using participant codes alone does not make data anonymous.
Reports and presentations will use non-identifying aggregate or
appropriately anonymised results. This form does not authorise
publication of identifiable audio, video or personal information
in public demonstrations, publications or repositories.

### B.5. Your Rights and Requests

The final wording of your KVKK rights and the request procedure
will be confirmed by the institution. These rights include:

- Learning whether your personal data are processed.
- Requesting information if they have been processed.
- Learning the purpose of processing and whether data are used
  consistently with that purpose.
- Knowing the third parties to whom data are transferred.
- Requesting correction of incomplete or inaccurate data.
- Requesting deletion or destruction under the applicable
  legal conditions.
- Requesting notification of relevant correction and deletion
  actions to recipients.
- Objecting to an adverse result arising solely from automated
  analysis.
- Requesting compensation for harm caused by unlawful processing.

**Request channel, identity-verification method and response procedure:**
[To be confirmed and completed by the institution].

For processing based on explicit consent, you may withdraw your
consent through [method]. The final notice will clearly explain
the prospective effect of withdrawal, deletion of relevant data
and any retention obligations based on another specific legal basis.
Withdrawal from the research is addressed separately in Section A.5.

### B.6. Acknowledgement of Receiving the Privacy Notice

This privacy notice has been provided and explained to me in a way
I can understand. I have had the opportunity to ask questions.
This acknowledgement does not mean that I give explicit consent
to personal data processing.

**Participant** — Full name: __________________
Date: __________ Signature: __________

**Person providing the privacy notice** — Full name: __________________
Date: __________ Signature: __________

---

## Section C — Separate Draft Explicit Consent Declaration for Personal Data Processing

> **Preparation note:** Include only activities for which explicit
> consent has been confirmed as the specific legal basis. Do not
> request additional consent for activities relying on other legal
> bases. Adapt the choices below to the final protocol; do not seek
> consent for unexplained purposes, data or services.

I have been informed about the processing described in Section B.
I indicate my choice separately for each activity below.
I understand that research participation consent and acknowledgement
of the privacy notice do not replace these choices.

| Activity, if confirmed to rely on explicit consent | I consent | I do not consent |
|---|---|---|
| [Processing my specified application usage and performance data for the evaluation purpose described in Section B] | [ ] | [ ] |
| [Processing my questionnaire and interview responses for the stated evaluation purpose] | [ ] | [ ] |
| [Processing the explicitly listed hearing/disability information confirmed as necessary for eligibility, for the stated purpose] | [ ] | [ ] |
| [Recording and processing audio of my research session for the explained purpose and under the stated conditions; only if audio recording is planned] | [ ] | [ ] |
| [Recording and processing video of my research session for the explained purpose and under the stated conditions; only if video recording is planned] | [ ] | [ ] |
| [Any other specific live application processing activity requiring explicit consent, described separately and clearly] | [ ] | [ ] |

Select only one option per row. A blank row or a row with both options
selected will not be treated as explicit consent.

**Effect of declining consent on participation:**
[Explain separately for each applicable activity. Distinguish refusal
of optional recording from refusal of essential test processing;
describe any available alternative without recording].

This declaration does not authorise model training, unexplained
external services, blanket international transfers or public sharing
of identifiable recordings. I understand how to withdraw consent
and the procedures explained in Sections A.5 and B.5.

**Participant** — Full name: __________________
Date: __________ Signature: __________

**Researcher providing the explanation** — Full name: __________________
Date: __________ Signature: __________

**Interpreter / witness, if applicable** — Full name and role: __________________
Date: __________ Signature: __________

You will receive a copy of the final information documents and your
signed declarations. Copies retained by the team will be subject
to the access and retention conditions in Section B.
