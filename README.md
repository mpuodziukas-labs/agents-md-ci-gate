# agents-md-ci-gate

Teams adopting agentic coding tools need their AGENTS.md rules enforced mechanically in CI, so a change that breaks a rule fails the build instead of relying on the agent or the reviewer remembering it.

`agents-lint` reads a fenced rules block in `AGENTS.md` and a unified diff, prints one line per violation, and exits 1 on any. Rule kinds: forbidden paths, a required test for each source change, forbidden added content (secret pattern), commit subject format, and a file-count limit. Python 3 standard library only, no network, no model call.

## Run it in 60 seconds

```
python3 evaluate.py
```

Output:

```
bad-01-prod-edit               expect no-prod-edits          -> PASS (exit 1)
bad-02-env-file                expect no-env-files           -> PASS (exit 1)
bad-03-rule-self-edit          expect no-rule-self-edit      -> PASS (exit 1)
bad-04-src-without-test        expect tests-required         -> PASS (exit 1)
bad-05-hardcoded-password      expect no-hardcoded-password  -> PASS (exit 1)
bad-06-bad-commit-subject      expect commit-format          -> PASS (exit 1)
bad-07-too-many-files          expect small-change           -> PASS (exit 1)
good-01-src-with-test          expect OK                     -> PASS (exit 0)
good-02-docs-only              expect OK                     -> PASS (exit 0)
bad changes caught: 7/7
good changes passed: 2/2
```

Each fixture under `fixtures/` is a synthetic change (`change.diff`, `message.txt`, `expect.txt`). Every bad change must exit 1 and name its rule; every good change must exit 0 with no output. In CI, run it on a real change with `git diff origin/main...HEAD | ./agents-lint --rules AGENTS.md --diff -`.

Tests: `python3 -m pytest -q` checks that this README equals the command output, the exit-code contract, that zero rules fails closed (exit 2), and that dropping a rule from `AGENTS.md` makes its fixture slip through.

## Honesty Statement

Synthetic fixtures written for this repo. No real repository, customer or production change was used. The counts above are the output of the command above, nothing more.

## Limitations

- Enforces the rules written in `AGENTS.md`; it does not judge code quality, correctness or intent.
- "Required test" means a changed file matches a path pattern, not that the test exercises the change.
- Parses unified diff headers and added lines only; renames, binary files and submodules are not modeled.
- The prose rules in `AGENTS.md` are not machine-checked.
