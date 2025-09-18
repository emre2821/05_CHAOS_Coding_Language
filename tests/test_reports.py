from chaos_reports import generate_business_report, render_report_lines
from chaos_runtime import run_chaos


def test_generate_business_report_highlights_top_emotion():
    src = """[ACCOUNT]: A-19\n[STAGE]: Negotiation\n[EMOTION:JOY:8]\n[EMOTION:FEAR:2]\n{Momentum is strong; keep the executive briefing tight.}\n"""
    env = run_chaos(src)
    report = generate_business_report(env)
    assert report["top_emotion"] == "JOY"
    assert "ACCOUNT" in report["structured"]
    lines = render_report_lines(report)
    assert any("JOY" in line for line in lines)
    assert any("Momentum is strong" in line for line in lines)
