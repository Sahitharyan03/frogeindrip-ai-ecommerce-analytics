"""Pydantic schemas for AI Copilot inputs, tool arguments, and verified responses."""

from typing import Any

from pydantic import BaseModel, Field


class ToolCallRequest(BaseModel):
    tool_name: str = Field(description="Name of the approved analytics function to execute")
    arguments: dict[str, Any] = Field(default_factory=dict, description="Validated arguments for the tool")


class CopilotAnswer(BaseModel):
    question: str
    selected_tool: str
    evidence_tier: str
    reporting_period: str
    data_provenance: str
    summary_markdown: str
    metrics: dict[str, Any]
    observation: str
    interpretation: str
    recommendation: str
    limitations: str | None = None
    is_llm_generated: bool = False
