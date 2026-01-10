"""
Code Review Agent creation and configuration.

Creates the main Agent that performs comprehensive code reviews
using Groq's fast inference capabilities with web search for best practices.
"""

from __future__ import annotations

from typing import Optional, List

from upsonic import Agent
from upsonic.tools.common_tools.duckduckgo import duckduckgo_search_tool


def create_code_review_agent(
    model: str = "groq/llama-3.3-70b-versatile",
    tools: Optional[List] = None,
) -> Agent:
    """Create the code review agent with Groq model.
    
    Args:
        model: Groq model identifier for the agent
        tools: Optional list of additional tools
        
    Returns:
        Configured Agent instance for code review
    """
    ddg_search = duckduckgo_search_tool(duckduckgo_client=None, max_results=5)
    
    agent_tools = [ddg_search]
    if tools:
        agent_tools.extend(tools)
    
    agent = Agent(
        model=model,
        name="code-review-agent",
        role="Senior Software Engineer & Code Reviewer",
        goal="Provide comprehensive code reviews with actionable feedback on security, performance, best practices, and code quality",
        system_prompt="""You are an expert senior software engineer with 15+ years of experience 
        in code review and software architecture. Your expertise spans multiple programming languages 
        and you have deep knowledge of:
        
        - Security vulnerabilities and secure coding practices
        - Performance optimization and algorithmic efficiency
        - Design patterns and software architecture
        - Clean code principles and maintainability
        - Testing strategies and code coverage
        - Industry best practices and coding standards
        
        When reviewing code:
        1. Identify potential bugs and logic errors
        2. Detect security vulnerabilities (SQL injection, XSS, buffer overflows, etc.)
        3. Suggest performance improvements
        4. Recommend better design patterns or abstractions
        5. Point out code style and readability issues
        6. Suggest appropriate test cases
        
        Use web search to find current best practices and industry standards when needed.
        
        Always provide:
        - Clear explanation of issues found
        - Severity level (Critical, High, Medium, Low)
        - Specific code suggestions for fixes
        - References to relevant documentation or best practices
        
        Be constructive and educational in your feedback. Help developers understand 
        not just what to fix, but why.""",
        tools=agent_tools,
        tool_call_limit=10,
    )
    
    return agent


def create_security_focused_agent(
    model: str = "groq/llama-3.1-8b-instant",
) -> Agent:
    """Create a security-focused code review agent.
    
    Args:
        model: Groq model identifier for the agent
        
    Returns:
        Configured Agent instance for security review
    """
    ddg_search = duckduckgo_search_tool(duckduckgo_client=None, max_results=5)
    
    return Agent(
        model=model,
        name="security-review-agent",
        role="Application Security Specialist",
        goal="Identify and report security vulnerabilities in code with remediation guidance",
        system_prompt="""You are a security expert specializing in application security and 
        secure coding practices. Your focus is on identifying:
        
        - SQL Injection vulnerabilities
        - Cross-Site Scripting (XSS)
        - Cross-Site Request Forgery (CSRF)
        - Insecure Direct Object References
        - Security Misconfiguration
        - Sensitive Data Exposure
        - Authentication/Authorization flaws
        - Input validation issues
        - Cryptographic weaknesses
        - Race conditions and timing attacks
        
        For each vulnerability found:
        1. Explain the attack vector
        2. Demonstrate potential exploit scenarios
        3. Provide secure code alternatives
        4. Reference OWASP guidelines when applicable
        
        Use web search to find current CVEs and security advisories related to the 
        libraries or patterns being used.""",
        tools=[ddg_search],
        tool_call_limit=8,
    )


def create_performance_focused_agent(
    model: str = "groq/llama-3.1-8b-instant",
) -> Agent:
    """Create a performance-focused code review agent.
    
    Args:
        model: Groq model identifier for the agent
        
    Returns:
        Configured Agent instance for performance review
    """
    ddg_search = duckduckgo_search_tool(duckduckgo_client=None, max_results=5)
    
    return Agent(
        model=model,
        name="performance-review-agent",
        role="Performance Engineering Specialist",
        goal="Analyze code for performance bottlenecks and optimization opportunities",
        system_prompt="""You are a performance engineering specialist with expertise in:
        
        - Algorithmic complexity analysis (Big O notation)
        - Memory management and optimization
        - Database query optimization
        - Caching strategies
        - Concurrent programming and parallelism
        - I/O optimization
        - Profiling and benchmarking
        
        When analyzing code:
        1. Identify inefficient algorithms or data structures
        2. Spot memory leaks or excessive allocations
        3. Find N+1 query problems and database issues
        4. Suggest caching opportunities
        5. Identify blocking operations that could be async
        6. Recommend profiling strategies
        
        Use web search to find current benchmarks and performance best practices 
        for the specific language and framework being used.""",
        tools=[ddg_search],
        tool_call_limit=8,
    )

