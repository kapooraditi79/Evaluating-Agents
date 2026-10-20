"""Grading for gate G0: is a model's reply a valid, sensible tool call?

Four levels, checked in order, first failure wins:
  1 json_ok       the call arrived as a structured call with parseable arguments
  2 tool_exists   the tool name is one we offered
  3 schema_ok     the arguments satisfy the tool's JSON Schema
  4 semantic_ok   the arguments make sense (real service, timestamps in range, ids copied)

Then the reply is compared with the case's expectation (right tool, right arguments).
All rules are code. Nothing here is judged by a model.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone

from jsonschema import Draft202012Validator

from .stub_tools import DATA_RANGE, SERVICES, TOOLS

TOOLS_BY_NAME = {t["function"]["name"]: t["function"] for t in TOOLS}
TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
TS_KEYS = ("start", "end", "incident_start", "incident_end", "baseline_start", "baseline_end")
TS_PAIRS = (("start", "end"), ("incident_start", "incident_end"),
            ("baseline_start", "baseline_end"))
ID_KEYS = ("trace_id",)

FAILURES = (
    "request_error", "json_unparsed", "tool_call_as_text", "empty_reply", "missing_call",
    "unneeded_call", "unknown_tool", "forbidden_tool", "schema_violation",
    "semantic_violation", "wrong_tool", "wrong_arg",
)


def parse_ts(value) -> datetime:
    if not isinstance(value, str):
        raise ValueError("not a string")
    return datetime.strptime(value, TS_FORMAT).replace(tzinfo=timezone.utc)


def looks_like_tool_json(text: str) -> bool:
    """True when a model wrote a tool call as plain text instead of a structured call."""
    t = text.strip()
    if t.startswith("```"):
        t = t.strip("`").removeprefix("json").strip()
    if not t or t[0] not in "{[":
        return False
    try:
        obj = json.loads(t)
    except ValueError:
        return '"name"' in t and ('"arguments"' in t or '"parameters"' in t)
    objs = obj if isinstance(obj, list) else [obj]
    return any(isinstance(o, dict) and "name" in o and ("arguments" in o or "parameters" in o)
               for o in objs)


def normalize_args(raw) -> dict:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            obj = json.loads(raw)
        except ValueError as e:
            raise ValueError(f"arguments are not valid JSON: {e}") from e
        if isinstance(obj, dict):
            return obj
    raise ValueError("arguments are not a JSON object")


def semantic_problems(args: dict, context: str) -> list[str]:
    problems: list[str] = []
    lo, hi = parse_ts(DATA_RANGE[0]), parse_ts(DATA_RANGE[1])
    if "service" in args and args["service"] not in SERVICES:
        problems.append(f"service {args['service']!r} is not a known service")
    parsed: dict[str, datetime] = {}
    for key in TS_KEYS:
        if key not in args:
            continue
        try:
            parsed[key] = parse_ts(args[key])
        except ValueError:
            problems.append(f"{key}: {args[key]!r} is not 'YYYY-MM-DDTHH:MM:SSZ' UTC")
            continue
        if not lo <= parsed[key] <= hi:
            problems.append(f"{key}: {args[key]} is outside the data range")
    for a, b in TS_PAIRS:
        if a in parsed and b in parsed and parsed[a] >= parsed[b]:
            problems.append(f"{a} must be before {b}")
    for key in ID_KEYS:
        if key in args and str(args[key]) not in context:
            problems.append(f"{key} {args[key]!r} does not appear in any earlier tool result")
    return problems


def violated(name: str, args: dict, rule: dict, context: str) -> str | None:
    """Return a problem string if a per-case argument rule is not met."""
    if name not in args:
        return f"{name}: missing"
    value = args[name]
    if "equals" in rule and value != rule["equals"]:
        return f"{name}: expected {rule['equals']!r}, got {value!r}"
    if "any_of" in rule and value not in rule["any_of"]:
        return f"{name}: expected one of {rule['any_of']}, got {value!r}"
    if "ts_equals" in rule:
        try:
            same = parse_ts(value) == parse_ts(rule["ts_equals"])
        except ValueError:
            same = False
        if not same:
            return f"{name}: expected {rule['ts_equals']}, got {value!r}"
    if rule.get("in_context") and str(value) not in context:
        return f"{name}: {value!r} was not copied from an earlier tool result"
    return None


def grade_case(message: dict, case: dict) -> dict:
    expect = case["expect"]
    mode = expect["mode"]  # call | no_call | call_or_none
    raw_calls = message.get("tool_calls") or []
    content = (message.get("content") or "").strip()
    context = "\n".join(m.get("content", "") for m in case["messages"] if m.get("role") == "tool")

    result = {
        "mode": mode, "n_calls": len(raw_calls), "passed": False, "failure": None,
        "problems": [], "calls": [],
        "levels": {"json_ok": None, "tool_exists": None, "schema_ok": None, "semantic_ok": None},
    }

    def fail(kind: str, *problems: str) -> dict:
        result["failure"] = kind
        result["problems"].extend(problems)
        return result

    if not raw_calls:
        if looks_like_tool_json(content):
            result["levels"]["json_ok"] = False
            return fail("tool_call_as_text", "the tool call was written as text, not as a call")
        if mode == "call":
            return fail("missing_call", "expected a tool call, got text only")
        if not content:
            return fail("empty_reply", "no tool call and no text")
        result["passed"] = True
        return result

    if mode == "no_call":
        return fail("unneeded_call", f"called {raw_calls[0].get('function', {}).get('name')} "
                                     "but no tool was needed")

    calls = []
    for raw in raw_calls:
        fn = raw.get("function", {})
        try:
            calls.append((fn.get("name"), normalize_args(fn.get("arguments", {}))))
        except ValueError as e:
            result["levels"]["json_ok"] = False
            return fail("json_unparsed", str(e))
    result["levels"]["json_ok"] = True
    result["calls"] = [{"name": n, "arguments": a} for n, a in calls]

    unknown = [n for n, _ in calls if n not in TOOLS_BY_NAME]
    result["levels"]["tool_exists"] = not unknown
    if unknown:
        return fail("unknown_tool", *[f"unknown tool: {n}" for n in unknown])

    forbidden = set(expect.get("forbidden_tools", []))
    used_forbidden = [n for n, _ in calls if n in forbidden]
    if used_forbidden:
        return fail("forbidden_tool", f"called forbidden tool: {used_forbidden[0]}")

    schema_errors = []
    for name, args in calls:
        validator = Draft202012Validator(TOOLS_BY_NAME[name]["parameters"])
        schema_errors += [f"{name}: {e.message}" for e in validator.iter_errors(args)]
    result["levels"]["schema_ok"] = not schema_errors
    if schema_errors:
        return fail("schema_violation", *schema_errors)

    semantic = []
    for name, args in calls:
        semantic += [f"{name}: {p}" for p in semantic_problems(args, context)]
    result["levels"]["semantic_ok"] = not semantic
    if semantic:
        return fail("semantic_violation", *semantic)

    allowed = expect.get("tools", {})
    first_name, first_args = calls[0]
    if first_name not in allowed:
        return fail("wrong_tool", f"called {first_name}, expected one of {sorted(allowed)}")
    wrong = [p for p in (violated(k, first_args, r, context)
                         for k, r in allowed[first_name].items()) if p]
    if wrong:
        return fail("wrong_arg", *wrong)

    result["passed"] = True
    return result


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson score interval for k successes out of n."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - margin), min(1.0, centre + margin))
