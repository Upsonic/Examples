"""
Output schemas for the AI Lexicon Agent.

This module defines the Pydantic models for structured output
from the AI governance lexicon explanations.
"""

from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class FAQ(BaseModel):
    """A single frequently asked question with its answer."""
    
    question: str = Field(
        description="A common question about the AI governance term"
    )
    answer: str = Field(
        description="A comprehensive answer to the question"
    )


class LexiconEntry(BaseModel):
    """
    Complete lexicon entry for an AI governance term.
    
    This represents the full output of the AI Lexicon agent,
    containing a brief explanation and FAQs for the given term.
    """
    
    term: str = Field(
        description="The AI governance term being explained"
    )
    brief_explanation: str = Field(
        description="A detailed but concise explanation of the term, covering its definition, importance, and practical applications in AI governance"
    )
    faqs: List[FAQ] = Field(
        default_factory=list,
        description="List of frequently asked questions and their answers about the term"
    )
    
    def format_output(self) -> str:
        """Format the lexicon entry as a readable string."""
        output_lines = [
            f"{self.term}:",
            "",
            self.brief_explanation,
            "",
            "FAQs:",
            ""
        ]
        
        for i, faq in enumerate(self.faqs, 1):
            output_lines.append(f"Q{i}: {faq.question}")
            output_lines.append(f"A{i}: {faq.answer}")
            output_lines.append("")
        
        return "\n".join(output_lines)
