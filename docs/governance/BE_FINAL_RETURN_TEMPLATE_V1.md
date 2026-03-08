# BE FINAL RETURN TEMPLATE V1

## Purpose

AUTONOMY-04 standardizes backend final return format so CD receives deterministic, comparable outputs across milestones.

## Required Final Return Fields

Every BE final return must include:

- milestone name
- reviewed commit SHA
- live build SHA
- routes tested
- changed files
- proof folder
- acceptance notes
- risk notes
- post-execution state

## Canonical Template

```text
FROM: VS
TO: BE-Core v1.4
SUBJECT: <MILESTONE> — EXECUTION RESULT
OBJECTIVE: <one-line objective>

PROMPT:

STATUS:
COMPLETE or BLOCKED

REVIEWED_COMMIT_SHA:
<sha>

LIVE_BUILD_SHA:
<sha>

ROUTES_TESTED:
<route list>

CHANGED_FILES:
<path list>

PROOF_FOLDER:
<repo-relative deterministic folder>

ACCEPTANCE_NOTES:
<deterministic pass/fail notes>

RISK_NOTES:
<risk list or NONE>

POST_EXECUTION_STATE:
<branch/worktree/deploy state>

PROOF PACK A — raw
<commit proof>

PROOF PACK B — raw
<changed files>

PROOF PACK C — raw
<raw diffs>

PROOF PACK D — raw
<bundle contents>

PROOF PACK E — raw
<validation outputs>

FINAL STATE:
<single deterministic paragraph>

HOLD:
AWAITING BE VALIDATION
```

## Alignment Notes

- This template is additive and aligned to existing autonomy packet markers.
- It does not replace the worker packet contracts.
- It standardizes BE-to-CD milestone closure for reduced manual relay burden.
