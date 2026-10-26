"""Utility formatting helpers for UI and reporting."""

def format_currency(value: float) -> str:
    """Format floating point numbers as currency ($XX,XXX.XX)."""
    if value is None:
        return "$0.00"
    return f"${value:,.2f}"


def format_pct(value: float, decimals: int = 1) -> str:
    """Format numbers as percentages."""
    if value is None:
        return "0.0%"
    return f"{value:.{decimals}f}%"


def format_delta(value: float, suffix: str = "%") -> str:
    """Format change delta with arrow indicator."""
    if value is None:
        return "0.0%"
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}{suffix}"
