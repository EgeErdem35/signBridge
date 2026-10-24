# SB-27 — Repository-wide Jira Done automation

**Status (24 October 2026):** Implemented and merged into `main` through SB-27 PR #18, then corrected in SB-28 PR #19. The SB-28 merge was reported to complete Jira SB-28 and post a success bot comment. The `gate` check has now been configured as a required status check in the `main-branch-protection` ruleset; this requirement is being independently verified with a fresh PR (SB-29).

## Purpose

Apply the same workflow to **every SignBridge teammate**, not just one assignee. On all pull requests targeting `main`, the GitHub Action validates the Handbook branch/PR rules. Only a **merged** PR that passes these gates can transition its corresponding Jira issue to the **Done** status category.

This Action **does not merge PRs**. Merge is still a separate authorized action, and branch protection/rulesets should be enabled to prevent bypassing checks.

## Event flow

- `pull_request_target` on opened, reopened, synchronize, ready_for_review and closed; plus `pull_request_review` submitted or dismissed.
- The workflow itself performs **no PR code checkout or execution**; it calls GitHub APIs and Jira APIs. **Security caveat:** `pull_request_review` runs in a different security context from `pull_request_target`; review events associated with same-repository branches can expose repository secrets to a modified workflow file. Keep workflow edits strictly protected by independent review and branch access controls. Prefer a dedicated least-privilege Jira service account long-term; the project owner has explicitly elected to use their Jira account for the initial rollout and accepts that actions will be attributed to that account. This consent does not eliminate the need to avoid untrusted PR code or protect secrets.
- On open/review: checks criteria, posts (or edits) an explanatory bot PR comment on violations and **fails the gate check**; otherwise leaves Jira unchanged.
- On PR closed-and-merged: rechecks all criteria; if every condition passes, calls Jira's issue transition API to move the issue to Done. If anything fails, **Jira stays unchanged** and a PR comment explains why.
- A PR closed without merge is never completed in Jira.

## Criteria validated

1. PR base is `main`; source branch exactly `story/SB-123`, `task/SB-123`, or `bug/SB-123`, without suffix.
2. Jira issue exists and its **actual issue type** matches the branch prefix. Turkish and English type names are supported.
3. PR title contains the correct SB key, and PR body includes its Jira issue URL.
4. At least one **independent reviewer approval on the latest head commit**; the latest review per reviewer must not be `CHANGES_REQUESTED`.
5. No unresolved inline review discussion threads.
6. All observable checks on the exact head SHA are completed successfully (or neutral/skipped); failing/pending **existing** commit statuses block closure; zero GitHub commit statuses are not treated as pending. `COMMENTED` review events do not supersede an approval or change request. GitHub branch-protection rules determine which checks are mandatory; configure those explicitly.
7. PR is not a draft and **is merged to main** before Jira Done.
8. Jira API confirms an available transition to a Done-category status; current Done issues are not transitioned twice.

**Feedback permissions and recovery:** GitHub event/repository token policies can reject PR comment writes with HTTP 403 (observed on merged PR #18, Actions run 40099333409). This does not by itself mean the Jira transition failed. SB-28 also requests explicit `pull-requests: write` permission for its PR-feedback API, while retaining `issues: write`; the team must verify the granted permissions and comment creation in a post-merge Actions run before declaring the 403 resolved. The gate emits the feedback and 403 details as an Actions job annotation/warning if the PR comment cannot be published. A validation blocker still makes the job fail, while a completed Jira transition remains a successful job even if writing the success comment is denied. Verify the Jira status separately and do not repeat the Jira transition merely to fix a comment. A rerun of the merged event is idempotent when the issue is already Done. If the team requires bot comments on every PR, investigate GitHub event policy/token write restrictions or install a narrowly permissioned GitHub App; do not broaden Jira privileges to address GitHub 403s.

This automation is **fail-closed with respect to Jira transitions**. An API error, missing secrets, or invalid criteria does **not** mark Jira Done. It cannot guarantee that a collaborator cannot merge an invalid PR unless branch-protection rules prevent it.

## Required one-time GitHub repository setup

At **GitHub → repository Settings → Secrets and variables → Actions**, add repository secrets:

| Secret | Purpose |
|---|---|
| `JIRA_BASE_URL` | `https://el-dili.atlassian.net` (site base URL, without `/wiki`) |
| `JIRA_EMAIL` | Email of the authorized Jira account (owner's personal account for initial rollout by their explicit choice; a dedicated automation account remains the safer long-term option) |
| `JIRA_API_TOKEN` | API token for that Jira account, with permissions to browse SB issues and perform allowed transitions |

**Never** put the API token or actual credentials in the repository, PR body, chat, build output, or Confluence. Rotate/revoke the token if exposed. The chosen Jira account must be permitted to browse and transition all in-scope SB issues. API actions will be attributed to that account; the owner should periodically audit Jira history and rotate the token, and can later replace the secrets with a dedicated account.

At **Settings → Actions → General**, allow this workflow and ensure the GitHub token has the **Issues: write** permission it needs for feedback. Organizations may restrict the default token or workflow use; adjust repository action permissions according to organizational policy.

At **Settings → Rules → Rulesets**, or **Settings → Branches → Branch protection rule** for `main`, configure where your repo plan permits:
- Require a PR before merging, with **at least one approving review**.
- **Mandatory:** Dismiss stale approvals on new commits (the gate demands an approval on the exact head SHA). Also enable approval of the most recent reviewable push where supported.
- Require all conversations resolved.
- Require status checks to pass: include **`gate` (Jira Done gate)** once it has run, plus your CI/test checks.
- Prohibit direct pushes and force pushes to `main` and prevent bypasses by ordinary contributors.

**Important:** There may be plan or private-repo limitations on enforcement; document any unimplemented protection requirement explicitly. The Action itself is not a substitute for branch protection.

## Recovery and failure modes

If a merged PR's final gate run cannot transition Jira to Done (temporary Jira outage, permission issue, missing required transition fields or a fixable validation problem), correct the issue and use **GitHub → Actions → Jira Done gate → the closed/merged workflow run → Re-run jobs**. It fetches the current PR and Jira state and is safe to rerun. Never manually alter Jira to hide a failing gate; resolve the reported issue first. Some Jira Done transitions require a screen field (for example Resolution); if a transition returns HTTP 400, configure the workflow transition or add the required field only after confirming its value with the Jira administrator.

The `gate` status check was configured as required in the `main-branch-protection` ruleset after the workflow appeared in GitHub. A fresh PR is needed to verify the rule blocks merging with a failing check and allows merging after independent approval and successful validation. Do not claim that the ruleset's enforcement is proven merely because its settings were saved.

## Verification / rollout plan

1. Merge **SB-27's own PR only after independent review**. A workflow file added to a feature branch is **not active on main** beforehand. (An owner can configure secrets before or after merge.)
2. Create a disposable **test Jira Task** through standard workflow, or use a safe test issue. Open a matching `task/SB-... ` PR.
3. Confirm that missing approval triggers a **failed gate check with precise PR feedback** and **does not change Jira**.
4. Obtain fresh independent approval; resolve review threads; confirm any required tests pass.
5. Merge the PR to `main`. Check that a new Action run transitions the correct test Jira issue to Done and leaves other issues untouched.
6. Open a PR with a wrong prefix/issue type or a failing required check; confirm **no Done transition**, appropriate feedback and no permitted merge when branch rules are enabled.
7. Test idempotence by re-running the workflow on an already completed issue; it must not perform a second transition.

**Verification caveat:** SB-28 is Done following merged PR #19 and a bot success comment was reported; nevertheless the required-check ruleset must be tested on a new PR, and both positive and negative gate cases recorded. Passing a single merged PR is not proof of every rejection scenario.

## Related resources

- [Jira SB-27](https://el-dili.atlassian.net/browse/SB-27)
- [Existing branch and PR policy](BRANCHING.md)
- [SignBridge Jira](https://el-dili.atlassian.net/jira/software/projects/SB)

## Pre-merge script syntax validation

For any change to the inline `actions/github-script` script, extract its JavaScript from the YAML `script: |` block and run `node --check` on the extracted `.js` file before merging. A `pull_request_target` run uses the workflow on the trusted base branch and therefore **does not prove the candidate feature-branch YAML/script parses correctly**. The SB-28 changes were also syntax-checked as an async JavaScript function before review.
