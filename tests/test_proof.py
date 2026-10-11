import pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
import evaluate

LINT = [sys.executable, str(ROOT / "agents-lint")]

def run(rules, diff, message=None):
    cmd = LINT + ["--rules", str(rules), "--diff", str(diff)]
    if message:
        cmd += ["--message", str(message)]
    return subprocess.run(cmd, capture_output=True, text=True)

def test_readme_matches_output():
    readme = (ROOT / "README.md").read_text()
    assert evaluate.results() in readme, "README drifted from `python3 evaluate.py`"

def test_all_bad_caught_all_good_pass():
    rows = evaluate.rows()
    assert len(rows) >= 8
    assert sum(1 for r in rows if r["bad"]) >= 6
    assert sum(1 for r in rows if not r["bad"]) >= 2
    assert all(r["ok"] for r in rows)

def test_exit_code_contract():
    bad = ROOT / "fixtures" / "bad-01-prod-edit"
    good = ROOT / "fixtures" / "good-01-src-with-test"
    p = run(ROOT / "AGENTS.md", bad / "change.diff", bad / "message.txt")
    assert p.returncode == 1 and "no-prod-edits" in p.stdout
    p = run(ROOT / "AGENTS.md", good / "change.diff", good / "message.txt")
    assert p.returncode == 0 and p.stdout == ""

def test_empty_rules_is_an_error_not_a_pass(tmp_path):
    empty = tmp_path / "AGENTS.md"
    empty.write_text("# no rules here\n")
    bad = ROOT / "fixtures" / "bad-01-prod-edit"
    p = run(empty, bad / "change.diff")
    assert p.returncode == 2, "zero rules must fail closed"

def test_mutant_dropping_a_rule_uncatches_its_fixture(tmp_path):
    mutant = tmp_path / "AGENTS.md"
    mutant.write_text("\n".join(l for l in (ROOT / "AGENTS.md").read_text().splitlines()
                                if not l.startswith("no-prod-edits")) + "\n")
    bad = ROOT / "fixtures" / "bad-01-prod-edit"
    p = run(mutant, bad / "change.diff", bad / "message.txt")
    assert "no-prod-edits" not in p.stdout
