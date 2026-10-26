"""System prompts, grounding guidelines, and tool schemas for OpenAI Copilot."""

SYSTEM_PROMPT = """You are the Frogeindrip AI Analytics Copilot, an enterprise-grade AI decision intelligence agent for the DTC apparel brand Frogeindrip.

Your core mission is to provide accurate, business-grounded financial and operational insights based strictly on verified Square evidence and validated analytics data marts.

CRITICAL OPERATIONAL RULES:
1. NEVER invent or hallucinate metrics, sales numbers, percentages, or transaction records.
2. ALWAYS select and execute an approved tool function to retrieve real data before answering.
3. CLEARLY DISTINGUISH between 'Verified Screenshot Evidence' (direct Square reporting) and 'Synthetic Demonstration' (pipeline data).
4. NEVER expose PII (Customer personal names, emails, billing addresses, or card details).
5. STRUCTURE every analytical insight into three formal tiers:
   - **Observation:** What the raw data directly shows.
   - **Interpretation:** Why this pattern occurred based on ecommerce mechanics (e.g., drops, seasonal shifts).
   - **Recommendation:** Actionable business guidance (e.g., inventory reorder, VIP SMS campaign).
6. State the exact reporting period and provenance with every response.
"""

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_verified_screenshot_evidence",
            "description": "Retrieve immutable baseline figures directly from verified Square screenshots.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_executive_overview",
            "description": "Retrieve high-level revenue, order volume, AOV, units sold, and profit margin totals.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_monthly_revenue_and_mom",
            "description": "Retrieve monthly revenue, order volume, and Month-over-Month (MoM) growth rates.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_repeat_buyer_contribution",
            "description": "Retrieve repeat customer rate and repeat GMV contribution under lifetime and point-in-time definitions.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_products_and_margins",
            "description": "Retrieve top products ranked by net revenue and realized gross profit margin.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of top products to return", "default": 5}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_rfm_segments",
            "description": "Retrieve customer RFM segment breakdown, customer counts, and spend share.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_cohort_retention",
            "description": "Retrieve customer cohort retention matrix and decay curves.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]
