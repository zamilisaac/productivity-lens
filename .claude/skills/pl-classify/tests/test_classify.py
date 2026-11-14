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
