"""Gate G0 runner: can a local model call tools reliably enough to build on?

    python -m evaluation.g0.run --model qwen2.5-coder:7b --cases evaluation/g0/pilot_cases.json

Output (mirrors the layout in the Agent Skills evaluation guide):
    runs/g0/<model>/iteration-N/
        meta.json  summary.json
        <case-id>/request.json response.json grading.json timing.json

A `pilot` case file never produces a verdict. Only a `gate` file is compared with the
pre-registered thresholds below.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path

import requests

from .checks import grade_case, wilson
from .stub_tools import DATA_RANGE, TOOLS

# Pre-registered gate thresholds. Do not edit after seeing results.
GATE_MIN_PASS_RATE = 0.90
GATE_MAX_INVALID_TOOL_NAMES = 0

SYSTEM_PROMPT = (
    "You are an incident investigator for a microservice online shop. You can only read "
    "telemetry through the tools provided; you cannot change anything.\n"
    "Telemetry covers {start} to {end} (UTC). The alert or report that started this "
    "investigation refers to {ref}.\n"
    "Use a tool when you need data. Answer directly when you do not. Always write "
    "timestamps as YYYY-MM-DDTHH:MM:SSZ (UTC)."
)


def slug(model: str) -> str:
    return "".join(c if c.isalnum() or c in "-." else "_" for c in model)


def shell(cmd: list[str]) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return (out.stdout or out.stderr).strip()
    except Exception as e:  # best-effort metadata only
        return f"unavailable: {e}"


def chat(host: str, model: str, messages: list, options: dict, timeout: float) -> dict:
    r = requests.post(f"{host}/api/chat", timeout=timeout, json={
        "model": model, "messages": messages, "tools": TOOLS,
        "stream": False, "options": options, "keep_alive": "10m"})
    r.raise_for_status()
    return r.json()


def timing_of(resp: dict, wall_s: float) -> dict:
    ev, ev_ns = resp.get("eval_count", 0), resp.get("eval_duration", 0)
    pe, pe_ns = resp.get("prompt_eval_count", 0), resp.get("prompt_eval_duration", 0)
    return {
        "total_tokens": ev + pe,
        "duration_ms": round(wall_s * 1000),
        "prompt_tokens": pe,
        "completion_tokens": ev,
        "load_ms": round(resp.get("load_duration", 0) / 1e6),
        "eval_tokens_per_s": round(ev / (ev_ns / 1e9), 1) if ev and ev_ns else None,
        "prompt_tokens_per_s": round(pe / (pe_ns / 1e9), 1) if pe and pe_ns else None,
    }


def run_case(case: dict, args, options: dict, out_dir: Path) -> dict:
    system = SYSTEM_PROMPT.format(start=DATA_RANGE[0], end=DATA_RANGE[1],
                                  ref=case["reference_time"])
    messages = [{"role": "system", "content": system}, *case["messages"]]
    case_dir = out_dir / case["id"]
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "request.json").write_text(json.dumps(
        {"model": args.model, "options": options, "messages": messages}, indent=2))

    started = time.time()
    try:
        resp = chat(args.host, args.model, messages, options, args.timeout)
        grading = grade_case(resp.get("message", {}), case)
    except requests.RequestException as e:
        resp = {"error": str(e)}
        grading = {"passed": False, "failure": "request_error", "problems": [str(e)],
                   "mode": case["expect"]["mode"], "n_calls": 0, "calls": [], "levels": {}}
    timing = timing_of(resp, time.time() - started)

    (case_dir / "response.json").write_text(json.dumps(resp, indent=2))
    (case_dir / "grading.json").write_text(json.dumps(grading, indent=2))
    (case_dir / "timing.json").write_text(json.dumps(timing, indent=2))
    return {"case": case, "grading": grading, "timing": timing, "response": resp}


def summarize(phase: str, results: list[dict]) -> dict:
    n = len(results)
    passed = sum(r["grading"]["passed"] for r in results)
    lo, hi = wilson(passed, n)
    by_cat: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    failures: Counter = Counter()
    for r in results:
        cat = by_cat[r["case"]["category"]]
        cat[1] += 1
        cat[0] += int(r["grading"]["passed"])
        if r["grading"]["failure"]:
            failures[r["grading"]["failure"]] += 1
    ev = [r["timing"]["eval_tokens_per_s"] for r in results if r["timing"]["eval_tokens_per_s"]]
    summary = {
        "phase": phase, "n": n, "passed": passed,
        "pass_rate": round(passed / n, 3) if n else 0.0,
        "wilson95": [round(lo, 3), round(hi, 3)],
        "invalid_tool_names": failures.get("unknown_tool", 0),
        "failures": dict(failures),
        "by_category": {k: f"{v[0]}/{v[1]}" for k, v in by_cat.items()},
        "mean_eval_tokens_per_s": round(sum(ev) / len(ev), 1) if ev else None,
        "mean_prompt_tokens": round(sum(r["timing"]["prompt_tokens"] for r in results) / n) if n else 0,
        "max_prompt_tokens": max((r["timing"]["prompt_tokens"] for r in results), default=0),
    }
    if phase == "gate":
        ok = (summary["pass_rate"] >= GATE_MIN_PASS_RATE
              and summary["invalid_tool_names"] <= GATE_MAX_INVALID_TOOL_NAMES)
        summary["verdict"] = "PASS" if ok else "FAIL"
    else:
        summary["verdict"] = "none (pilot runs never produce a verdict)"
    return summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--cases", type=Path, required=True)
    ap.add_argument("--host", default="http://localhost:11434")
    ap.add_argument("--num-ctx", type=int, default=4096)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--timeout", type=float, default=600)
    ap.add_argument("--out", type=Path, default=Path("runs/g0"))
    ap.add_argument("--only", nargs="*", help="run only these case ids")
    args = ap.parse_args()

    spec = json.loads(args.cases.read_text(encoding="utf-8"))
    cases = [c for c in spec["cases"] if not args.only or c["id"] in args.only]
    options = {"temperature": args.temperature, "seed": args.seed, "num_ctx": args.num_ctx}

    base = args.out / slug(args.model)
    n = 1 + max((int(p.name.split("-")[1]) for p in base.glob("iteration-*")), default=0)
    out_dir = base / f"iteration-{n}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"model={args.model} phase={spec['phase']} cases={len(cases)} options={options}")
    results = []
    for case in cases:
        res = run_case(case, args, options, out_dir)
        results.append(res)
        g, t = res["grading"], res["timing"]
        status = "PASS" if g["passed"] else f"FAIL[{g['failure']}]"
        print(f"  {case['id']:<26} {case['category']:<20} {status:<28} "
              f"{t['duration_ms']:>6} ms  in={t['prompt_tokens']:>5} out={t['completion_tokens']:>4}")
        for problem in g["problems"][:2]:
            print(f"      - {problem}")

    (out_dir / "meta.json").write_text(json.dumps({
        "model": args.model, "options": options, "phase": spec["phase"],
        "cases_file": str(args.cases),
        "cases_sha256": hashlib.sha256(args.cases.read_bytes()).hexdigest()[:12],
        "ollama_version": shell(["ollama", "--version"]),
        "ollama_ps": shell(["ollama", "ps"]),
        "git_sha": shell(["git", "rev-parse", "--short", "HEAD"]),
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }, indent=2))
    summary = summarize(spec["phase"], results)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))

    print("\nSUMMARY")
    print(json.dumps(summary, indent=2))
    print(f"\nwritten to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
