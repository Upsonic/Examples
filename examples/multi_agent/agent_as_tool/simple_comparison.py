"""
Simple Comparison: Single Agent vs Agent-as-Tool
=================================================

This script demonstrates the difference between using a single agent
vs using specialized agents as tools.
"""

from upsonic import Agent, Task
import time


def print_section(title):
    """Pretty print section headers"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def single_agent_approach():
    """Traditional approach: One agent does everything"""
    
    print_section("TRADITIONAL APPROACH: Single Agent")
    
    print("Creating a single agent to handle all tasks...")
    
    # One agent trying to do everything
    generalist = Agent(
        name="Generalist",
        model="openai/gpt-4o-mini",
        system_prompt="You are a helpful assistant."
    )
    
    task = Task(
        description="""
        Create a product launch campaign for an AI-powered code editor:
        
        1. Research the market and competitors
        2. Develop a positioning strategy  
        3. Write compelling marketing copy
        
        Provide a comprehensive campaign plan.
        """
    )
    
    print("Starting execution...\n")
    start_time = time.time()
    
    result = generalist.print_do(task)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nResult:\n{result}\n")
    print(f"Time taken: {duration:.2f} seconds")
    print(f"Approach: Single generalist agent")
    
    return result, duration


def hierarchical_agent_approach():
    """Modern approach: Specialized agents as tools"""
    
    print_section("UPSONIC APPROACH: Agent-as-Tool")
    
    print("Creating specialized agents...\n")
    
    # Specialist 1: Market Research
    research_agent = Agent(
        name="Market Research Specialist",
        model="openai/gpt-4o",
        role="Senior Market Research Analyst",
        goal="Provide deep market insights and competitive intelligence",
        system_prompt="""You are a senior market research analyst specializing 
        in technology products. You provide comprehensive market analysis, 
        competitor research, trend identification, and strategic insights."""
    )
    print("  Created: Market Research Specialist")
    
    # Specialist 2: Strategy
    strategy_agent = Agent(
        name="Strategy Specialist",
        model="openai/gpt-4o",
        role="Strategic Marketing Planner",
        goal="Develop winning go-to-market strategies",
        system_prompt="""You are a strategic marketing planner with expertise 
        in positioning, messaging, and go-to-market strategy. You create 
        actionable strategies that drive market success."""
    )
    print("  Created: Strategy Specialist")
    
    # Specialist 3: Content Creation
    content_agent = Agent(
        name="Content Specialist",
        model="openai/gpt-4o-mini",
        role="Creative Marketing Writer",
        goal="Create compelling marketing content",
        system_prompt="""You are a creative marketing writer. You write 
        persuasive copy that converts, engaging social media posts, and 
        compelling product descriptions. Your writing is clear and impactful."""
    )
    print("  Created: Content Specialist")
    
    # Coordinator
    print("\nCreating coordinator agent...")
    coordinator = Agent(
        name="Campaign Director",
        model="openai/gpt-4o",
        role="Product Launch Director",
        system_prompt="""You are a product launch director managing a team 
        of specialists. You effectively delegate tasks to your team members 
        and synthesize their outputs into cohesive campaign plans.""",
        tools=[
            research_agent,
            strategy_agent, 
            content_agent
        ]
    )
    print("  Created: Campaign Director (with 3 specialist tools)\n")
    
    task = Task(
        description="""
        Create a product launch campaign for an AI-powered code editor:
        
        1. Research the market and competitors
        2. Develop a positioning strategy
        3. Write compelling marketing copy
        
        Provide a comprehensive campaign plan.
        """
    )
    
    print("Starting execution...\n")
    start_time = time.time()
    
    result = coordinator.print_do(task)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nResult:\n{result}\n")
    print(f"Time taken: {duration:.2f} seconds")
    print(f"Approach: Hierarchical specialists")
    print(f"Cost: Optimized (mix of GPT-4o and GPT-4o-mini)")
    
    return result, duration


def run_comparison():
    """Run both approaches and compare"""
    
    print("""
    AGENT-AS-TOOL COMPARISON DEMO
    =============================
    Comparing traditional single agent vs hierarchical specialists
    """)
    
    # Run single agent approach
    single_result, single_time = single_agent_approach()
    
    # Run hierarchical approach
    hierarchical_result, hierarchical_time = hierarchical_agent_approach()
    
    # Final comparison
    print_section("FINAL COMPARISON")
    
    print(f"  Single Agent Time:        {single_time:>6.2f}s")
    print(f"  Hierarchical Agent Time:  {hierarchical_time:>6.2f}s")
    print()
    print("  Single Agent:")
    print("    - Generalist approach")
    print("    - Mixed expertise in one agent")
    print("    - Harder to debug")
    print()
    print("  Hierarchical Agents:")
    print("    - Specialist expertise per task")
    print("    - Clear separation of concerns")
    print("    - Easy to test independently")
    print("    - Reusable across projects")
    print("    - Cost-optimized (right model for each task)")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--single":
        single_agent_approach()
    elif len(sys.argv) > 1 and sys.argv[1] == "--hierarchical":
        hierarchical_agent_approach()
    else:
        run_comparison()
