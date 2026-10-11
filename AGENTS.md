# AGENTS.md

Rules for any coding agent or human changing this repository.
The block below is machine-checked by `agents-lint` on every change.
Each line is `rule-id | kind | argument`.

```agents-lint
no-prod-edits | forbid-path | ^infra/prod/
no-env-files | forbid-path | (^|/)\.env
no-rule-self-edit | forbid-path | ^AGENTS\.md$
tests-required | require-paired | ^src/ => ^tests/
no-hardcoded-password | forbid-added | (?i)password\s*=\s*["'][^"']+["']
commit-format | commit-message | ^(feat|fix|docs|test|chore|refactor): [a-z].{0,70}$
small-change | max-files | 5
```

## Prose rules (not machine-checked)

- Explain intent in the commit body when the change is not obvious.
- Prefer the smallest change that satisfies the task.
