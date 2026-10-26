"""Unit tests for AI Copilot intent routing, tool execution, and security."""

from frogeindrip.ai.copilot import FrogeindripCopilot


def test_copilot_intent_classification():
    """Verify that deterministic pattern matching maps inquiries to correct tools."""
    copilot = FrogeindripCopilot()

    assert copilot.classify_intent_offline("What are the verified Square sales figures?") == "get_verified_screenshot_evidence"
    assert copilot.classify_intent_offline("What percentage of GMV came from repeat customers?") == "get_repeat_buyer_contribution"
    assert copilot.classify_intent_offline("How did revenue change month over month?") == "get_monthly_revenue_and_mom"
    assert copilot.classify_intent_offline("Which products have the highest gross profit margins?") == "get_top_products_and_margins"
    assert copilot.classify_intent_offline("What does our cohort retention curve look like?") == "get_cohort_retention"
    assert copilot.classify_intent_offline("Who are our Champion and Loyal customer segments?") == "get_rfm_segments"


def test_copilot_deterministic_answer_generation():
    """Verify that offline execution produces fully grounded structured responses."""
    copilot = FrogeindripCopilot()
    answer = copilot.ask("What was our Average Order Value and total net sales?")

    assert answer.selected_tool == "get_executive_overview"
    assert answer.evidence_tier is not None
    assert answer.reporting_period is not None
    assert len(answer.observation) > 0
    assert len(answer.interpretation) > 0
    assert len(answer.recommendation) > 0
    assert answer.is_llm_generated is False


def test_copilot_security_sql_injection_defense():
    """Verify that unauthorized SQL commands or PII requests are blocked."""
    copilot = FrogeindripCopilot()
    malicious_query = "DROP TABLE raw_orders; SELECT * FROM passwords;"
    answer = copilot.ask(malicious_query)

    assert answer.selected_tool == "SECURITY_GUARDRAIL"
    assert answer.metrics.get("blocked") is True
    assert "Security Alert" in answer.summary_markdown
