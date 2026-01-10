"""
Output schemas for code review agent.

Defines structured Pydantic models for type-safe outputs from the
code review analysis.
"""

from __future__ import annotations

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class CodeIssue(BaseModel):
    """Represents a single code issue found during review."""
    
    severity: Literal["critical", "high", "medium", "low", "info"] = Field(
        description="Severity level of the issue"
    )
    category: str = Field(
        description="Category of the issue (e.g., security, performance, style, bug)"
    )
    line_reference: Optional[str] = Field(
        default=None,
        description="Line number or code section reference"
    )
    title: str = Field(
        description="Brief title describing the issue"
    )
    description: str = Field(
        description="Detailed description of the issue"
    )
    suggestion: str = Field(
        description="Suggested fix or improvement"
    )
    code_example: Optional[str] = Field(
        default=None,
        description="Example of correct/improved code"
    )


class SecurityAnalysis(BaseModel):
    """Security-focused analysis results."""
    
    vulnerabilities_found: int = Field(
        description="Number of security vulnerabilities found"
    )
    risk_level: Literal["critical", "high", "medium", "low", "none"] = Field(
        description="Overall security risk level"
    )
    owasp_categories: List[str] = Field(
        default_factory=list,
        description="Relevant OWASP categories for issues found"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Security recommendations"
    )


class PerformanceAnalysis(BaseModel):
    """Performance-focused analysis results."""
    
    complexity_issues: List[str] = Field(
        default_factory=list,
        description="Algorithmic complexity concerns"
    )
    memory_concerns: List[str] = Field(
        default_factory=list,
        description="Memory usage concerns"
    )
    optimization_opportunities: List[str] = Field(
        default_factory=list,
        description="Potential performance optimizations"
    )


class CodeQualityMetrics(BaseModel):
    """Code quality assessment metrics."""
    
    readability_score: Literal["excellent", "good", "fair", "poor"] = Field(
        description="Code readability assessment"
    )
    maintainability_score: Literal["excellent", "good", "fair", "poor"] = Field(
        description="Code maintainability assessment"
    )
    test_coverage_suggestion: str = Field(
        description="Suggestions for test coverage"
    )
    documentation_quality: Literal["excellent", "good", "fair", "poor", "missing"] = Field(
        description="Documentation quality assessment"
    )


class CodeReviewOutput(BaseModel):
    """Complete code review output."""
    
    summary: str = Field(
        description="Executive summary of the code review"
    )
    overall_rating: Literal["excellent", "good", "needs_improvement", "poor", "critical"] = Field(
        description="Overall code quality rating"
    )
    issues: List[CodeIssue] = Field(
        default_factory=list,
        description="List of all issues found"
    )
    security_analysis: SecurityAnalysis = Field(
        description="Security analysis results"
    )
    performance_analysis: PerformanceAnalysis = Field(
        description="Performance analysis results"
    )
    code_quality: CodeQualityMetrics = Field(
        description="Code quality metrics"
    )
    positive_aspects: List[str] = Field(
        default_factory=list,
        description="Positive aspects of the code"
    )
    priority_fixes: List[str] = Field(
        default_factory=list,
        description="Top priority items to fix, in order"
    )
    learning_resources: List[str] = Field(
        default_factory=list,
        description="Recommended resources for improvement"
    )

