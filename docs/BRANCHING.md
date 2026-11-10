# Branching and Pull Request Strategy

This document defines the Git workflow for SignBridge.

## Branches

- `main`: stable integration branch. Do not push changes directly; use pull requests.
- `SB-<issue-number>`: exact Jira issue key for all new work (for example, `SB-46`).

Create branches from the latest `main` and keep each branch focused on one Jira issue. Use the issue key without a prefix or suffix.

## Pull Requests

1. Open a PR from your working branch into `main`.
2. Include the Jira issue key in the PR title and link to the issue in the description.
3. Describe the changes and how they were tested.
4. Request at least one teammate review; the author should not approve their own PR.
5. Address review feedback and ensure required checks pass before merging.
6. Prefer squash merges to keep the main history readable, and delete merged branches.

## Proposed GitHub protection settings for `main`

- Require a pull request before merging.
- Require at least one approving review.
- Dismiss stale approvals after new commits, if available.
- Require conversation resolution before merging.
- Block force pushes and branch deletion.
- Require CI status checks after workflows have been created and verified.

These are documented team policies. Enforcing them requires configuring a GitHub ruleset or branch protection rule separately. Availability and enforcement depend on repository plan and visibility.
