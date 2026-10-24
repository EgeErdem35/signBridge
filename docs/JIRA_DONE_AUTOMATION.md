# SB-27 — Repository-wide Jira Done automation

**Status:** Proposed implementation; not active until this PR is approved and merged into `main`, and Jira credentials are configured.

## Purpose

Apply the same workflow to **every SignBridge teammate**, not just one assignee. On all pull requests targeting `main`, the GitHub Action validates the Handbook branch/PR rules. Only a **merged** PR that passes these gates can transition its corresponding Jira issue to the **Done** status category.

This Action **does not merge PRs**. Merge is still a separate authorized action, and branch protection/rulesets should be enabled to prevent bypassing checks.

## Event flow

- `pull_request_target` on opened, reopened, synchronize, ready_for_review and closed; plus `pull_request_review` submitted or dismissed.
- No PR code is checked out or executed. The trusted workflow accesses GitHub REST/GraphQL APIs and the Atlassian Jira API only.
- On open/review: checks criteria, posts (or edits) an explanatory bot PR comment on violations and **fails the gate check**; otherwise leaves Jira unchanged.
- On PR closed-and-merged: rechecks all criteria; if every condition passes, calls Jira's issue transition API to move the issue to Done. If anything fails, **Jira stays unchanged** and a PR comment explains why.
- A PR closed without merge is never completed in Jira.

## Criteria validated

1. PR base is `main`; source branch exactly `story/SB-123`, `task/SB-123`, or `bug/SB-123`, without suffix.
2. Jira issue exists and its **actual issue type** matches the branch prefix. Turkish and English type names are supported.
3. PR title contains the correct SB key, and PR body includes its Jira issue URL.
4. At least one **independent reviewer approval on the latest head commit**; the latest review per reviewer must not be `CHANGES_REQUESTED`.
5. No unresolved inline review discussion threads.
6. All observable checks on the exact head SHA are completed successfully (or neutral/skipped); failing/pending commit statuses block closure. GitHub branch-protection rules determine which checks are mandatory; configure those explicitly.
7. PR is not a draft and **is merged to main** before Jira Done.
8. Jira API confirms an available transition to a Done-category status; current Done issues are not transitioned twice.

This automation is **fail-closed with respect to Jira transitions**. An API error, missing secrets, or invalid criteria does **not** mark Jira Done. It cannot guarantee that a collaborator cannot merge an invalid PR unless branch-protection rules prevent it.

## Required one-time GitHub repository setup

At **GitHub → repository Settings → Secrets and variables → Actions**, add repository secrets:

| Secret | Purpose |
|---|---|
| `JIRA_BASE_URL` | `https://el-dili.atlassian.net` (site base URL, without `/wiki`) |
| `JIRA_EMAIL` | Email of a designated **authorized Jira automation account** |
| `JIRA_API_TOKEN` | API token for that account, with read issue / transition issue permissions |

**Never** put the API token or actual credentials in the repository, PR body, chat, build output, or Confluence. Rotate/revoke the token if exposed. The Jira account must be permitted to browse and transition all in-scope SB issues.

At **Settings → Actions → General**, allow this workflow and ensure the GitHub token has the **Issues: write** permission it needs for feedback. Organizations may restrict the default token or workflow use; adjust repository action permissions according to organizational policy.

At **Settings → Rules → Rulesets**, or **Settings → Branches → Branch protection rule** for `main`, configure where your repo plan permits:
- Require a PR before merging, with **at least one approving review**.
- Dismiss stale approvals on new commits.
- Require all conversations resolved.
- Require status checks to pass: include **`gate` (Jira Done gate)** once it has run, plus your CI/test checks.
- Prohibit direct pushes and force pushes to `main` and prevent bypasses by ordinary contributors.

**Important:** There may be plan or private-repo limitations on enforcement; document any unimplemented protection requirement explicitly. The Action itself is not a substitute for branch protection.

## Verification / rollout plan

1. Merge **SB-27's own PR only after independent review**. A workflow file added to a feature branch is **not active on main** beforehand. (An owner can configure secrets before or after merge.)
2. Create a disposable **test Jira Task** through standard workflow, or use a safe test issue. Open a matching `task/SB-... ` PR.
3. Confirm that missing approval triggers a **failed gate check with precise PR feedback** and **does not change Jira**.
4. Obtain fresh independent approval; resolve review threads; confirm any required tests pass.
5. Merge the PR to `main`. Check that a new Action run transitions the correct test Jira issue to Done and leaves other issues untouched.
6. Open a PR with a wrong prefix/issue type or a failing required check; confirm **no Done transition**, appropriate feedback and no permitted merge when branch rules are enabled.
7. Test idempotence by re-running the workflow on an already completed issue; it must not perform a second transition.

**Deployment caveat:** No live end-to-end GitHub-to-Jira automation can be claimed verified until repository secrets, GitHub rules and independent merge/testing are completed.

## Relationship with existing SB-25 reminder

A previous **ChatGPT hourly watch for SB-25** remains separate from this repo-wide action. After the new action is tested and confirmed operational, disable the older watch to avoid redundant actions.

## Related resources

- [Jira SB-27](https://el-dili.atlassian.net/browse/SB-27)
- [Existing branch and PR policy](BRANCHING.md)
- [SignBridge Jira](https://el-dili.atlassian.net/jira/software/projects/SB)
