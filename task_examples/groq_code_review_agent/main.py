from __future__ import annotations

from typing import Dict, Any

from upsonic import Task

try:
    from .agent import create_code_review_agent
    from .task_builder import build_review_task
    from .schemas import CodeReviewOutput
except ImportError:
    from agent import create_code_review_agent
    from task_builder import build_review_task
    from schemas import CodeReviewOutput


async def main(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for code review and best practices analysis.
    
    Args:
        inputs: Dictionary containing:
            - code: The code snippet to review (required)
            - language: Programming language of the code (required)
            - focus_areas: Optional list of areas to focus on (security, performance, etc.)
            - context: Optional context about the codebase or project
            - model: Optional model identifier (default: "groq/llama-3.3-70b-versatile")
    
    Returns:
        Dictionary containing comprehensive code review
    """
    code = inputs.get("code")
    if not code:
        raise ValueError("code is required in inputs")
    
    language = inputs.get("language")
    if not language:
        raise ValueError("language is required in inputs")
    
    focus_areas = inputs.get("focus_areas", [])
    context = inputs.get("context")
    model = inputs.get("model", "groq/llama-3.3-70b-versatile")
    
    agent = create_code_review_agent(model=model)
    
    task_description = build_review_task(
        code=code,
        language=language,
        focus_areas=focus_areas,
        context=context,
    )
    
    task = Task(task_description, response_format=CodeReviewOutput)
    
    result = await agent.do_async(task)
    
    return {
        "language": language,
        "focus_areas": focus_areas,
        "review_report": result,
        "review_completed": True,
    }



if __name__ == "__main__":
    import asyncio
    import json
    import sys
    
    test_code = '''
def calculate_discount(price, discount_percent):
    if discount_percent > 100:
        discount_percent = 100
    final_price = price - (price * discount_percent / 100)
    return final_price

def process_user_data(user_input):
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return execute_query(query)

class UserManager:
    users = []
    
    def add_user(self, name, email):
        self.users.append({"name": name, "email": email})
    
    def get_user(self, name):
        for user in self.users:
            if user["name"] == name:
                return user
        return None
'''
    
    test_inputs = {
        "code": test_code,
        "language": "python",
        "focus_areas": ["security", "performance", "best_practices"],
        "context": "E-commerce application backend",
        "model": "groq/llama-3.3-70b-versatile",
    }
    
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r") as f:
                test_inputs = json.load(f)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            print("Using default test inputs")
    
    async def run_main():
        try:
            result = await main(test_inputs)
            report: CodeReviewOutput = result.get('review_report')
            
            print("\n" + "=" * 80)
            print("🔍 CODE REVIEW COMPLETED SUCCESSFULLY")
            print("=" * 80)
            
            print(f"\n📋 Language: {result.get('language')}")
            print(f"🎯 Focus Areas: {', '.join(result.get('focus_areas', []))}")
            print(f"⭐ Overall Rating: {report.overall_rating.upper()}")
            
            print("\n" + "-" * 80)
            print("📝 SUMMARY")
            print("-" * 80)
            print(report.summary)
            
            print("\n" + "-" * 80)
            print(f"🚨 ISSUES FOUND ({len(report.issues)})")
            print("-" * 80)
            for i, issue in enumerate(report.issues, 1):
                severity_icons = {
                    "critical": "🔴",
                    "high": "🟠", 
                    "medium": "🟡",
                    "low": "🟢",
                    "info": "🔵"
                }
                icon = severity_icons.get(issue.severity, "⚪")
                print(f"\n{i}. {icon} [{issue.severity.upper()}] {issue.title}")
                print(f"   Category: {issue.category}")
                if issue.line_reference:
                    print(f"   Location: {issue.line_reference}")
                print(f"   Description: {issue.description}")
                print(f"   Suggestion: {issue.suggestion}")
                if issue.code_example:
                    print(f"   Example: {issue.code_example}")
            
            print("\n" + "-" * 80)
            print("🔒 SECURITY ANALYSIS")
            print("-" * 80)
            sec = report.security_analysis
            print(f"   Risk Level: {sec.risk_level.upper()}")
            print(f"   Vulnerabilities Found: {sec.vulnerabilities_found}")
            if sec.owasp_categories:
                print(f"   OWASP Categories: {', '.join(sec.owasp_categories)}")
            if sec.recommendations:
                print("   Recommendations:")
                for rec in sec.recommendations:
                    print(f"     • {rec}")
            
            print("\n" + "-" * 80)
            print("⚡ PERFORMANCE ANALYSIS")
            print("-" * 80)
            perf = report.performance_analysis
            if perf.complexity_issues:
                print("   Complexity Issues:")
                for issue in perf.complexity_issues:
                    print(f"     • {issue}")
            if perf.memory_concerns:
                print("   Memory Concerns:")
                for concern in perf.memory_concerns:
                    print(f"     • {concern}")
            if perf.optimization_opportunities:
                print("   Optimization Opportunities:")
                for opp in perf.optimization_opportunities:
                    print(f"     • {opp}")
            
            print("\n" + "-" * 80)
            print("📊 CODE QUALITY METRICS")
            print("-" * 80)
            quality = report.code_quality
            print(f"   Readability: {quality.readability_score}")
            print(f"   Maintainability: {quality.maintainability_score}")
            print(f"   Documentation: {quality.documentation_quality}")
            print(f"   Test Coverage: {quality.test_coverage_suggestion}")
            
            if report.positive_aspects:
                print("\n" + "-" * 80)
                print("✅ POSITIVE ASPECTS")
                print("-" * 80)
                for aspect in report.positive_aspects:
                    print(f"   • {aspect}")
            
            print("\n" + "-" * 80)
            print("🎯 PRIORITY FIXES")
            print("-" * 80)
            for i, fix in enumerate(report.priority_fixes, 1):
                print(f"   {i}. {fix}")
            
            if report.learning_resources:
                print("\n" + "-" * 80)
                print("📚 LEARNING RESOURCES")
                print("-" * 80)
                for resource in report.learning_resources:
                    print(f"   • {resource}")
            
            print("\n" + "=" * 80)
            
        except Exception as e:
            print(f"\n❌ Error during execution: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    asyncio.run(run_main())

