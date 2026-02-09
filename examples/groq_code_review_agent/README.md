# Groq Code Review & Best Practices Agent

A fast and comprehensive Code Review Agent built with the **Upsonic AI Agent Framework** using **Groq's ultra-fast inference**. This example demonstrates how to use Groq models for rapid code analysis, security vulnerability detection, and best practices recommendations.

## Features

- ⚡ **Ultra-Fast Reviews**: Leverages Groq's industry-leading inference speed for rapid code analysis
- 🔒 **Security Analysis**: Identifies vulnerabilities like SQL injection, XSS, and insecure patterns
- 🚀 **Performance Review**: Analyzes algorithmic complexity and optimization opportunities
- ✨ **Best Practices**: Compares code against industry standards and suggests improvements
- 📊 **Structured Output**: Returns typed, validated responses using Pydantic schemas
- 🔍 **Web Search Integration**: Uses DuckDuckGo to find current best practices and security advisories
- 🎯 **Focused Analysis**: Supports custom focus areas for targeted reviews

## Prerequisites

- Python 3.10+
- Groq API key (get one at [console.groq.com](https://console.groq.com))

## Installation

1. **Navigate to this directory**:
   ```bash
   cd examples/groq_code_review_agent
   ```

2. **Install dependencies**:
   ```bash
   # Install all dependencies
   upsonic install
   
   # Or install specific sections:
   upsonic install api          # API dependencies only (default)
   upsonic install development  # Development dependencies only
   ```

3. **Set up environment variables**:
   ```bash
   export GROQ_API_KEY="your-groq-api-key"
   ```

## Usage

### Run the API Server

To run the agent as a FastAPI server:

```bash
upsonic run
```

The API will be available at `http://localhost:8000` with automatic OpenAPI documentation at `http://localhost:8000/docs`.

OR

You can run the agent directly:

```bash
uv run main.py
```

**Example API Call:**
```bash
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def process_user(input):\n    query = \"SELECT * FROM users WHERE id = \" + input\n    return db.execute(query)",
    "language": "python",
    "focus_areas": ["security", "best_practices"]
  }'
```

## Project Structure

```
groq_code_review_agent/
├── main.py                    # Entry point with async main() function
├── agent.py                   # Agent creation with Groq model configuration
├── schemas.py                 # Pydantic output schemas for structured responses
├── task_builder.py            # Task description builder
├── upsonic_configs.json       # Upsonic configuration and dependencies
└── README.md                  # This file
```

## How It Works

1. **Groq Model**: Uses Groq's `llama-3.3-70b-versatile` model for fast, high-quality code analysis. The model can also be switched to `llama-3.1-8b-instant` for even faster responses.

2. **Structured Output**: Leverages Pydantic schemas to ensure consistent, typed output including:
   - Severity-rated issues with code examples
   - Security analysis with OWASP category mapping
   - Performance analysis with complexity concerns
   - Code quality metrics and ratings

3. **Web Search Integration**: Uses DuckDuckGo to search for:
   - Current security best practices
   - Language-specific coding standards
   - Recent CVEs and security advisories
   - Performance benchmarks and optimization techniques

4. **Focused Analysis**: Supports optional focus areas to prioritize specific aspects:
   - `security`: Emphasize vulnerability detection
   - `performance`: Focus on optimization opportunities
   - `best_practices`: Concentrate on coding standards
   - `style`: Focus on readability and conventions

## Available Groq Models

| Model | Use Case | Speed |
|-------|----------|-------|
| `groq/llama-3.3-70b-versatile` | Comprehensive analysis | Fast |
| `groq/llama-3.1-8b-instant` | Quick reviews, simpler code | Ultra-fast |
| `groq/gemma2-9b-it` | Balanced performance | Fast |
| `groq/qwen-2.5-coder-32b` | Specialized for code | Fast |

## Example Output

When you run the agent, you'll see a structured output like this:

```
================================================================================
🔍 CODE REVIEW COMPLETED SUCCESSFULLY
================================================================================

📋 Language: python
🎯 Focus Areas: security, performance, best_practices
⭐ Overall Rating: NEEDS_IMPROVEMENT

--------------------------------------------------------------------------------
📝 SUMMARY
--------------------------------------------------------------------------------
The code has several issues, including a critical SQL injection vulnerability,
high-severity input validation issue, and medium-severity performance issue.

--------------------------------------------------------------------------------
🚨 ISSUES FOUND (4)
--------------------------------------------------------------------------------

1. 🔴 [CRITICAL] SQL Injection Vulnerability
   Category: security
   Location: query = "SELECT * FROM users WHERE name = '" + user_input + "'"
   Description: SQL injection vulnerability
   Suggestion: Use parameterized queries
   Example: query = "SELECT * FROM users WHERE name = ?"

2. 🟠 [HIGH] Input Validation
   Category: security
   Description: Lack of input validation
   Suggestion: Validate user input

3. 🟡 [MEDIUM] Inefficient User Lookup
   Category: performance
   Description: Inefficient user lookup
   Suggestion: Use a dictionary for user lookup

--------------------------------------------------------------------------------
🔒 SECURITY ANALYSIS
--------------------------------------------------------------------------------
   Risk Level: HIGH
   Vulnerabilities Found: 1
   OWASP Categories: A03:2021-Injection
   Recommendations:
     • Use parameterized queries
     • Validate user input

--------------------------------------------------------------------------------
⚡ PERFORMANCE ANALYSIS
--------------------------------------------------------------------------------
   Complexity Issues:
     • Inefficient user lookup
   Optimization Opportunities:
     • Use a dictionary for user lookup

--------------------------------------------------------------------------------
📊 CODE QUALITY METRICS
--------------------------------------------------------------------------------
   Readability: good
   Maintainability: fair
   Documentation: fair
   Test Coverage: Write unit tests for each function

--------------------------------------------------------------------------------
✅ POSITIVE ASPECTS
--------------------------------------------------------------------------------
   • Good naming conventions
   • Clear code structure

--------------------------------------------------------------------------------
🎯 PRIORITY FIXES
--------------------------------------------------------------------------------
   1. SQL injection vulnerability
   2. Input validation
   3. Inefficient user lookup

--------------------------------------------------------------------------------
📚 LEARNING RESOURCES
--------------------------------------------------------------------------------
   • https://www.python.org/dev/peps/pep-0008/
   • https://docs.python.org/3/tutorial/errors.html

================================================================================
```

The structured `CodeReviewOutput` schema ensures consistent, typed responses:

```python
CodeReviewOutput(
    summary="...",
    overall_rating="needs_improvement",  # Literal type
    issues=[CodeIssue(severity="critical", category="security", ...)],
    security_analysis=SecurityAnalysis(vulnerabilities_found=1, risk_level="high", ...),
    performance_analysis=PerformanceAnalysis(...),
    code_quality=CodeQualityMetrics(readability_score="good", ...),
    positive_aspects=["Good naming conventions", ...],
    priority_fixes=["SQL injection vulnerability", ...],
    learning_resources=["https://...", ...]
)
```

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `code` | string | ✓ | The code snippet to review |
| `language` | string | ✓ | Programming language (python, javascript, etc.) |
| `focus_areas` | array | ✗ | Areas to prioritize: security, performance, best_practices, style |
| `context` | string | ✗ | Project context for tailored recommendations |
| `model` | string | ✗ | Groq model identifier (default: groq/llama-3.3-70b-versatile) |

## Why Groq?

Groq's custom LPU (Language Processing Unit) hardware provides:
- **Speed**: Up to 10x faster inference than GPU-based solutions
- **Consistency**: Low latency variance for production workloads
- **Cost Efficiency**: Competitive pricing with high throughput
- **Quality**: Access to top-tier open-source models (LLaMA, Gemma, etc.)

This makes Groq ideal for code review workflows where fast feedback loops improve developer productivity.

