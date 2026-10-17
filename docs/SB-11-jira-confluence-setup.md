# SB-11 — Jira and Confluence Workspace Setup

## Purpose
Document the Jira and Confluence project-management setup carried out for SignBridge under [SB-11](https://el-dili.atlassian.net/browse/SB-11). This file records and links to existing configuration; it does **not** claim that the configuration was created by this commit.

## Jira workflow
- Project: [SignBridge (SB)](https://el-dili.atlassian.net/jira/software/projects/SB/boards/3)
- Board columns: **To Do → In Progress → Review → Done**.
- Work is moved to **Review** for teammate inspection before **Done**.
- Sprint 1 tasks are tracked in Jira and referenced from the Confluence sprint page.

## Confluence space
- Canonical team space: [signBridge (key: SIGNBRIDGE)](https://el-dili.atlassian.net/wiki/spaces/SIGNBRIDGE).
- The Jira project's Documents section was linked to the team Confluence space.
- An additional space with key `S` exists and should not be confused with the canonical `SIGNBRIDGE` space.
- [Sprint 1 — Planning & Progress](https://el-dili.atlassian.net/wiki/spaces/SIGNBRIDGE/pages/3080195) includes the sprint goal, a live Jira issues view, work ready for review, and risks.

## Handbook-aligned page organization
The space was organized with these sections:

```text
signBridge
├── Documentation
├── Meetings
│   ├── Technical
│   └── Scrum
│       └── Sprint 1
│           ├── Refinement
│           ├── Review
│           ├── Retrospective
│           └── Planning
│               └── Sprint 1 - Planning Meeting
├── Proposal
├── Statement of Work
└── Sprint Notes
    └── Sprint 1 - Planning & Progress
```

The Planning Meeting page uses Confluence's official Meeting Notes template. Meeting attendance, decisions, and outcomes must reflect **actual meetings**; creating a template does not prove a meeting was held.

## Access and checks still pending
- Verify each team member can view/edit the canonical space. Emir Ersan's invitation/access was not yet confirmed during setup.
- Confirm attendees can publish their assigned documentation; keep unnecessary administrator access under review.
- Verify the Jira Documents link points to `SIGNBRIDGE`, not the similarly named `S` space.
- Record actual Refinement, Planning, Review, Retrospective and Technical meetings with the evidence required by the project handbook.
- SB-11 should stay **Review** until another team member inspects and accepts the setup.

## Verification evidence
- [Jira SB-11](https://el-dili.atlassian.net/browse/SB-11)
- [SignBridge Jira board](https://el-dili.atlassian.net/jira/software/projects/SB/boards/3)
- [Canonical Confluence space](https://el-dili.atlassian.net/wiki/spaces/SIGNBRIDGE)
- [Sprint 1 documentation](https://el-dili.atlassian.net/wiki/spaces/SIGNBRIDGE/pages/3080195)

This documentation commit is the GitHub traceability record for SB-11; the actual Jira/Confluence actions preceded it.
