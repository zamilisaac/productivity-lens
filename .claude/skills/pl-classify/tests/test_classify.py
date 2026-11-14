"""Run: python .claude/skills/pl-classify/tests/test_classify.py  (no extra packages needed)"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SCRIPT = HERE.parent / "scripts" / "classify.py"
sys.path.insert(0, str(SCRIPT.parent))
import classify as C  # noqa: E402


def base(**kw):
    a = dict(id="x", company="Ex", code="0", fy="2026", initiative="i", page="1", source="AR",
             quote="raised output from 10 to 20", category="operations", status="achieved",
             result_kind="capacity", input="machine_time", figure="before_after", area="line_machinery")
    a.update(kw)
    return a


def test_playbook_examples_all_agree():
    r = subprocess.run([sys.executable, str(SCRIPT), "test", str(HERE / "playbook_examples.csv"), "--min", "100"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_capacity_is_enabler_never_lesson():
    c = C.classify(base())
    assert (c["counted"], c["grade"], c["evidence_type"], c["lesson_eligible"]) == ("Y", "A", "Enabler", "N")


def test_planning_words_warn():
    c = C.classify(base(quote="The line will raise output to 20,000"))
    assert any("planning words" in w for w in c["warnings"])


def test_sustainability_only_needs_operating_measure():
    c = C.classify(base(source="SR", result_kind="none", figure="none", quote="improved efficiency"))
    assert c["counted"] == "N" and "sustainability" in c["fail_reason"]


def test_rule_override_is_recorded():
    c = C.classify(base(result_kind="revenue_profit", rule="R099", rule_outcome="pass"))
    assert c["counted"] == "Y" and any("R099" in w for w in c["warnings"])


def test_uncertain_goes_to_decisions():
    c = C.classify(base(uncertain="Y", uncertain_reason="two plants mixed"))
    assert c["decision_needed"] == "Y"


def test_reported_result_numbers_must_be_in_quote():
    c = C.classify(base(quote="raised output from 10 to 20", reported_result="10 -> 25"))
    assert any("not in quote" in w for w in c["warnings"])


def test_number_words_count_as_figures():
    c = C.classify(base(quote="expected to make approximately one million pieces a day"))
    assert not any("no number" in w for w in c["warnings"])


def test_input_saving_passes_tier3():
    c = C.classify(base(area="resource", result_kind="input_saving", input="energy", figure="single_impact",
                        quote="diesel use cut by over 141,000 litres"))
    assert (c["counted"], c["tier"], c["grade"], c["evidence_type"]) == ("Y", 3, "A", "Operating result")


def test_tier3_never_a_lesson_under_R035():
    rows = [base(id=f"t{i}", area="resource", result_kind="input_saving", input="energy", figure="single_impact",
                 quote="diesel use cut by 141,000 litres", type=f"Resource {i}") for i in range(3)]
    res = C.run_rows(rows)
    assert all(r["counted"] == "Y" and r["lesson_eligible"] == "N" for r in res)
    assert C.select_lessons(res) == []


def test_tier3_allowed_once_when_policy_allows():
    C.POLICY["tier3_lessons"] = True
    try:
        rows = [base(id=f"t{i}", area="resource", result_kind="input_saving", input="energy", figure="single_impact",
                     quote="diesel use cut by 141,000 litres", type=f"Resource {i}") for i in range(3)]
        assert len(C.select_lessons(C.run_rows(rows))) == 1
    finally:
        C.POLICY["tier3_lessons"] = False


def test_consolidation_needs_result_R040():
    c = C.classify(base(area="consolidation", result_kind="investment_scale", input="space", quote="sold farm, cows 3,394 to 1,614"))
    assert c["counted"] == "N" and "R040" in c["fail_reason"]
    c = C.classify(base(area="consolidation", result_kind="cost", input="space", figure="single_impact", quote="saved RM2m a year"))
    assert c["counted"] == "Y"


def test_skip_and_environment_only_not_listed():
    assert C.classify(base(rule="R041", rule_outcome="skip"))["listed"] == "N"
    c = C.classify(base(result_kind="environmental_only", area="resource", quote="581 million litres recycled"))
    assert (c["counted"], c["listed"]) == ("N", "N")


def test_repeat_type_when_too_few_types_R035():
    rows = [base(id=f"x{i}", result_kind="time", input="people", figure="single_impact", quote="lead time cut 20%", type="Process redesign") for i in range(3)]
    assert len(C.select_lessons(C.run_rows(rows))) == 3


def test_lessons_prefer_tier1_productivity_and_distinct_types():
    rows = [base(id="a", area="resource", result_kind="cost", input="water", figure="single_impact", quote="saved RM1m", type="Resource substitution"),
            base(id="b", result_kind="time", input="people", figure="single_impact", quote="lead time cut 20%", type="Process redesign"),
            base(id="c", result_kind="output_per_input", input="people", figure="single_impact", quote="output per worker up 15%", type="New/upgraded line"),
            base(id="d", result_kind="downtime", input="machine_time", figure="single_impact", quote="downtime fell 30%", type="New/upgraded line")]
    ids = [r["id"] for r in C.select_lessons(C.run_rows(rows))]
    assert ids == ["c", "b", "d"], ids  # Tier 3 "a" never chosen (R035); type repeated instead


def test_validate_rejects_unknown_values():
    assert C.validate([base(result_kind="productivity")])


if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn(); print("PASS", name)
            except AssertionError as e:
                fails += 1; print("FAIL", name, e)
    sys.exit(1 if fails else 0)
