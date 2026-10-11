import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).parent
LINT = [sys.executable, str(ROOT / "agents-lint")]

def rows(rules=ROOT / "AGENTS.md"):
    out = []
    for d in sorted((ROOT / "fixtures").iterdir()):
        expect = (d / "expect.txt").read_text().strip()
        p = subprocess.run(LINT + ["--rules", str(rules), "--diff", str(d / "change.diff"),
                                   "--message", str(d / "message.txt")], capture_output=True, text=True)
        names = [l.split(":")[0] for l in p.stdout.splitlines()]
        bad = expect != "OK"
        ok = (p.returncode == 1 and expect in names) if bad else (p.returncode == 0 and not names)
        out.append({"name": d.name, "bad": bad, "expect": expect, "ok": ok, "rc": p.returncode})
    return out

def results(rules=ROOT / "AGENTS.md"):
    rs = rows(rules)
    lines = [f"{r['name']:<30} expect {r['expect']:<22} -> {'PASS' if r['ok'] else 'FAIL'} (exit {r['rc']})" for r in rs]
    bad = [r for r in rs if r["bad"]]; good = [r for r in rs if not r["bad"]]
    lines.append(f"bad changes caught: {sum(r['ok'] for r in bad)}/{len(bad)}")
    lines.append(f"good changes passed: {sum(r['ok'] for r in good)}/{len(good)}")
    return "\n".join(lines)

if __name__ == "__main__":
    out = results()
    print(out)
    sys.exit(0 if " FAIL " not in out and "/" in out and all(r["ok"] for r in rows()) else 1)
