# agents-md-ci-gate

Teams adopting agentic coding tools need their AGENTS.md rules enforced mechanically in CI, so a change that breaks a rule fails the build instead of relying on the agent or the reviewer remembering it.

## Run it in 60 seconds

```
python3 -m pip install pytest
python3 evaluate.py
python3 -m pytest -q
```

## Results

| bad caught | good passed |
|---|---|
| 1/1 | 1/1 |

## Honesty Statement

Synthetic data. Not production, not client data.

## Limitations

Small synthetic corpus. Replace before drawing conclusions.
