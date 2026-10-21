# SB-16 - AUTSL Dataset Access Request

**Jira:** [SB-16](https://el-dili.atlassian.net/browse/SB-16)  
**Project:** SignBridge-TR, Yaşar University Software Engineering senior project  
**Record date:** 21 October 2026  
**Status:** Academic access request sent; developer response received. Archive download and extraction remain unverified.

## Access route

The team consulted the [official AUTSL dataset page](https://cvml.ankara.edu.tr/datasets/), the [dataset paper](https://arxiv.org/abs/2008.00932), and the linked [ChaLearn dataset page](https://chalearnlap.cvc.uab.es/dataset/40/description/). After the legacy university contact route returned an undeliverable-address notice, the request was sent to the developer's current university contact.

## Request and review record

- Request sent: **20 October 2026, 22:02**, as displayed in the sender's mailbox in Türkiye.
- Sender: the task owner's Yaşar University student account.
- Recipient: the AUTSL developer contacted through the current Hacettepe University faculty address.
- Pre-send review: the task owner confirmed that all teammates reviewed and approved the draft before sending.
- Advisor permission: the task owner confirmed permission to mention the advisor and include him in CC; this does not establish separate advisor approval of the email wording.
- Request contents: project name and purpose; six-person Software Engineering senior-project context; isolated-sign MVP; planned MediaPipe landmark processing and signer-independent evaluation; academic and non-commercial use; proper citation; advisor information; questions about access, licence conditions and derived-landmark use.
- The exact sent text, recipient address and evidence are retained privately. This public record summarises the request and does not reproduce the correspondence.

## Outcome and verification

The task owner reported receipt of a developer response around midday on **21 October 2026**, providing access instructions for training, validation and test data and associated labels/class mappings.

A limited connectivity check returned HTTP 206 for the class-mapping CSV and the first 1,024 bytes (reported total size: 4,063 bytes). Sample requests to the three data archives timed out in the checking environment. This does not prove that the links are broken.

Full download, extraction, completeness, class coverage and signer-independent splits have not been verified. No additional redistribution permission is assumed.

## Remaining work

- Verify archive download and extraction from the team's environment.
- Check applicable use conditions, labels and splits before training.
- Supply the exact request text and recipient record through an agreed restricted evidence location to satisfy the remaining SB-16 documentation requirement.
- Obtain teammate PR review before merging.

Private correspondence, personal email addresses, access credentials, private download URLs and dataset files are excluded from this record.
