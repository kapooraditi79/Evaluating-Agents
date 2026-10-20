import json
from pathlib import Path

import pytest

from evaluation.g0.checks import TOOLS_BY_NAME, grade_case, looks_like_tool_json, wilson
from evaluation.g0.stub_tools import DATA_RANGE, TOOLS

TRACE_ID = "c71d08e53fa2946b0d8e1a3c57b92f04"
CONTEXT_MSG = {
    "role": "tool",
    "tool_name": "find_traces",
    "content": f'{{"rows":[["T2","{TRACE_ID}",2310.7,"OK"]]}}',
}

LOGS = {
    "mode": "call",
    "tools": {"search_logs": {"service": {"equals": "payment"}, "severity": {"equals": "ERROR"}}},
}


def call(name, **arguments):
    return {"content": "", "tool_calls": [{"function": {"name": name, "arguments": arguments}}]}


def case(expect, messages=None):
    return {"expect": expect, "messages": messages or [{"role": "user", "content": "x"}]}


GOOD = dict(
    service="payment", severity="ERROR", start="2026-03-14T14:05:00Z", end="2026-03-14T14:13:00Z"
)


def test_valid_call_passes_all_levels():
    r = grade_case(call("search_logs", **GOOD), case(LOGS))
    assert r["passed"] and r["failure"] is None
    assert all(r["levels"].values())


def test_unknown_tool_name():
    r = grade_case(call("search_log", **GOOD), case(LOGS))
    assert r["failure"] == "unknown_tool" and r["levels"]["tool_exists"] is False


def test_missing_required_argument_is_schema_violation():
    args = {k: v for k, v in GOOD.items() if k != "end"}
    assert grade_case(call("search_logs", **args), case(LOGS))["failure"] == "schema_violation"


def test_wrong_argument_type_is_schema_violation():
    r = grade_case(call("search_logs", **GOOD, limit="5"), case(LOGS))
    assert r["failure"] == "schema_violation"


def test_extra_argument_is_schema_violation():
    r = grade_case(call("search_logs", **GOOD, verbose=True), case(LOGS))
    assert r["failure"] == "schema_violation"


@pytest.mark.parametrize(
    "override",
    [
        {"service": "payments"},  # not a real service
        {"start": "2026-03-14T14:13:00Z", "end": "2026-03-14T14:05:00Z"},  # reversed
        {"start": "2026-03-14T13:00:00Z"},  # outside the data range
        {"start": "14:05"},  # not an ISO timestamp
        {"end": "2026-03-14T14:13:00+00:00"},  # wrong format (offset instead of Z)
    ],
)
def test_semantic_violations(override):
    r = grade_case(call("search_logs", **{**GOOD, **override}), case(LOGS))
    assert r["failure"] == "semantic_violation", r["problems"]
    assert r["levels"]["schema_ok"] is True and r["levels"]["semantic_ok"] is False


def test_trace_id_must_be_copied_exactly_from_context():
    expect = {"mode": "call", "tools": {"get_trace": {"trace_id": {"equals": TRACE_ID}}}}
    ok = grade_case(call("get_trace", trace_id=TRACE_ID), case(expect, [CONTEXT_MSG]))
    assert ok["passed"]
    one_char_off = TRACE_ID[:-1] + "5"
    bad = grade_case(call("get_trace", trace_id=one_char_off), case(expect, [CONTEXT_MSG]))
    assert bad["failure"] == "semantic_violation"
    invented = grade_case(call("get_trace", trace_id=TRACE_ID), case(expect))  # no context
    assert invented["failure"] == "semantic_violation"


def test_wrong_tool_and_wrong_argument():
    r = grade_case(
        call(
            "query_metric",
            service="payment",
            metric="error_count",
            start=GOOD["start"],
            end=GOOD["end"],
        ),
        case(LOGS),
    )
    assert r["failure"] == "wrong_tool"
    r = grade_case(call("search_logs", **{**GOOD, "service": "checkout"}), case(LOGS))
    assert r["failure"] == "wrong_arg"


def test_no_call_mode():
    expect = {"mode": "no_call"}
    assert grade_case({"content": "p95 is the 95th percentile."}, case(expect))["passed"]
    assert grade_case(call("list_services"), case(expect))["failure"] == "unneeded_call"


def test_missing_call_when_one_is_needed():
    r = grade_case({"content": "Let me look into that."}, case(LOGS))
    assert r["failure"] == "missing_call"


def test_tool_call_written_as_text_is_its_own_failure():
    text = '{"name": "search_logs", "arguments": {"service": "payment"}}'
    r = grade_case({"content": text}, case(LOGS))
    assert r["failure"] == "tool_call_as_text" and r["levels"]["json_ok"] is False
    assert looks_like_tool_json("```json\n" + text + "\n```")
    assert not looks_like_tool_json("p95 means the 95th percentile")


def test_forbidden_tool_even_when_arguments_are_valid():
    expect = {
        "mode": "call_or_none",
        "tools": {"search_logs": {}},
        "forbidden_tools": ["get_dependencies"],
    }
    r = grade_case(call("get_dependencies", start=DATA_RANGE[0], end=DATA_RANGE[1]), case(expect))
    assert r["failure"] == "forbidden_tool"
    assert grade_case({"content": "Payment is restarting after OOM kills."}, case(expect))["passed"]


def test_string_arguments_are_parsed_or_flagged():
    msg = {
        "content": "",
        "tool_calls": [{"function": {"name": "search_logs", "arguments": json.dumps(GOOD)}}],
    }
    assert grade_case(msg, case(LOGS))["passed"]
    msg["tool_calls"][0]["function"]["arguments"] = "{not json"
    assert grade_case(msg, case(LOGS))["failure"] == "json_unparsed"


def test_wilson_interval_for_27_of_30():
    lo, hi = wilson(27, 30)
    assert 0.73 < lo < 0.76 and 0.96 < hi < 0.97


# --- the case file itself --------------------------------------------------

PILOT = Path(__file__).resolve().parents[2] / "evaluation" / "g0" / "pilot_cases.json"


def _cases():
    return json.loads(PILOT.read_text(encoding="utf-8"))["cases"]


def test_pilot_file_is_marked_pilot_and_ids_are_unique():
    spec = json.loads(PILOT.read_text(encoding="utf-8"))
    assert spec["phase"] == "pilot"
    ids = [c["id"] for c in spec["cases"]]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("c", _cases(), ids=lambda c: c["id"])
def test_every_case_is_satisfiable(c):
    """The known-good answer stored with each case must pass the grader."""
    expect = c["expect"]
    assert expect["mode"] in ("call", "no_call", "call_or_none")
    for tool in expect.get("tools", {}):
        assert tool in TOOLS_BY_NAME
    example = c["example_pass"]
    if example is None:
        assert expect["mode"] != "call"
        message = {"content": "a plain text answer"}
    else:
        message = call(example["name"], **example["arguments"])
    result = grade_case(message, c)
    assert result["passed"], result["problems"]


def test_nine_tools_are_offered():
    assert len(TOOLS) == 9
