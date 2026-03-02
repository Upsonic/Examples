"""
Task description builder for code review agent.

Constructs comprehensive task descriptions based on input parameters.
"""

from __future__ import annotations

from typing import Optional, List


def build_review_task(
    code: str,
    language: str,
    focus_areas: Optional[List[str]] = None,
    context: Optional[str] = None,
) -> str:
    """Build comprehensive task description for code review.
    
    Args:
        code: The code snippet to review
        language: Programming language of the code
        focus_areas: Optional list of areas to focus on
        context: Optional context about the codebase
        
    Returns:
        Comprehensive task description string
    """
    focus_section = ""
    if focus_areas:
        focus_list = ", ".join(focus_areas)
        focus_section = f"""
    **Priority Focus Areas**: {focus_list}
    - Pay special attention to these areas during your review
    - Provide detailed analysis for each focus area"""
    
    context_section = ""
    if context:
        context_section = f"""
    **Project Context**: {context}
    - Consider this context when evaluating design decisions
    - Tailor recommendations to fit the project requirements"""
    
    task_description = f"""Perform a comprehensive code review of the following {language} code.

**Code to Review**:
```{language}
{code}
```
{focus_section}
{context_section}

**Review Requirements**:

1. **Bug Detection**: 
   - Identify potential bugs and logic errors
   - Look for edge cases that might not be handled
   - Check for null/undefined handling

2. **Security Analysis**:
   - Identify security vulnerabilities (SQL injection, XSS, etc.)
   - Check for sensitive data exposure
   - Verify input validation and sanitization
   - Use web search to find current security best practices for {language}

3. **Performance Review**:
   - Analyze algorithmic complexity
   - Identify performance bottlenecks
   - Suggest optimization opportunities
   - Look for inefficient patterns

4. **Code Quality Assessment**:
   - Evaluate code readability and structure
   - Check for proper error handling
   - Assess naming conventions
   - Review code organization and modularity

5. **Best Practices**:
   - Compare against {language} best practices
   - Suggest design pattern improvements
   - Recommend testing strategies
   - Use web search to find current industry standards

6. **Documentation**:
   - Assess documentation quality
   - Suggest necessary documentation additions
   - Check for clear and helpful comments

**CRITICAL - JSON Formatting Requirements**:

1. **NO DUPLICATE KEYS**: Each JSON key must appear only once. Do NOT repeat keys like "positive_aspects" or "priority_fixes".

2. **Plain String Values**: The following fields must be plain text strings, NOT JSON objects:
   - `suggestion`: Plain text string (e.g., "Use parameterized queries")
   - `code_example`: Plain text string with escaped quotes
   - `description`: Plain text string
   - `title`: Plain text string

3. **Proper Quote Escaping**: When a string contains quotes, escape them with backslash.
   - Correct: code_example field should be: query = "SELECT * FROM users WHERE name = ?"
     (In JSON, this becomes: "code_example": "query = \\"SELECT * FROM users WHERE name = ?\\"")
   - Wrong: Do NOT wrap in JSON objects like: "code_example": "{{ \\"example\\": \\"SELECT...\\" }}"

4. **Complete JSON**: Ensure all strings are properly closed with quotes and the entire JSON is valid.

5. **Validation**: Before returning, verify:
   - No duplicate keys exist
   - All strings are plain text (not wrapped in JSON objects)
   - All quotes inside strings are escaped with backslash
   - The entire JSON structure is valid and parseable

Provide your analysis with clear severity levels, specific code examples, actionable recommendations, and priority ordering."""
    
    return task_description

