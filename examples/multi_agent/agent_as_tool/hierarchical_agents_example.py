"""
Agent as Tool Demo: Hierarchical AI Agent Architecture
=======================================================

This example demonstrates Upsonic's powerful "Agent as Tool" feature where
specialized agents work together in a hierarchical structure. Perfect for
complex workflows that require different types of expertise.

Use Case: Product Launch Campaign Manager
- Main Coordinator agent delegates to specialized agents
- Each specialist agent has unique expertise
- Agents can be reused across different tasks
"""

from upsonic import Agent, Task

# ============================================
# STEP 1: Create Specialized Agents
# ============================================

# Research Specialist - Gathers market intelligence
research_agent = Agent(
    name="Research Specialist",
    model="openai/gpt-4o-mini",
    role="Market Research Analyst",
    goal="Gather comprehensive market intelligence and competitive analysis",
    system_prompt="""You are an expert market research analyst. When given a topic, 
    you provide detailed research including market trends, competitor analysis, 
    target audience insights, and data-driven recommendations."""
)

# Content Specialist - Creates marketing content
content_agent = Agent(
    name="Content Specialist", 
    model="openai/gpt-4o",
    role="Creative Content Writer",
    goal="Create compelling marketing content and copy",
    system_prompt="""You are a creative content writer specializing in marketing. 
    You create engaging copy, social media posts, email campaigns, and product 
    descriptions that convert. Your writing is persuasive and audience-focused."""
)

# Strategy Specialist - Develops go-to-market strategy
strategy_agent = Agent(
    name="Strategy Specialist",
    model="openai/gpt-4o", 
    role="Strategic Marketing Planner",
    goal="Develop comprehensive go-to-market strategies",
    system_prompt="""You are a strategic marketing planner. You analyze research, 
    define positioning, select channels, set KPIs, and create actionable 
    launch plans. You think holistically about market entry."""
)


# ============================================
# STEP 2: Create Coordinator Agent
# ============================================

# Main Coordinator - Orchestrates specialized agents
coordinator = Agent(
    name="Campaign Coordinator",
    model="openai/gpt-4o",
    role="Product Launch Manager",
    system_prompt="""You are a product launch manager coordinating a team of 
    specialists. You delegate tasks to your team members effectively and 
    synthesize their outputs into a cohesive campaign plan."""
)


# ============================================
# STEP 3: Example 1 - Simple Delegation
# ============================================

def example_simple_delegation():
    """Simple example: Main agent uses research agent as a tool"""
    
    print("=" * 60)
    print("EXAMPLE 1: Simple Delegation")
    print("=" * 60)
    
    task = Task(
        description="""Research the AI agent framework market. 
        Focus on trends, key players, and opportunities.""",
        tools=[research_agent]  # Research agent as a tool
    )
    
    result = coordinator.do(task)
    print("\n📊 Research Results:")
    print(result)
    return result


# ============================================
# STEP 4: Example 2 - Multi-Agent Workflow
# ============================================

def example_multi_agent_workflow():
    """Complex example: Main agent coordinates multiple specialists"""
    
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Multi-Agent Workflow")
    print("=" * 60)
    
    task = Task(
        description="""Create a complete product launch campaign for a new 
        AI-powered customer service chatbot. 
        
        1. First, research the market and competitors
        2. Then, develop a go-to-market strategy
        3. Finally, create compelling marketing content
        
        Provide a comprehensive campaign plan.""",
        tools=[
            research_agent,   # For market research
            strategy_agent,   # For strategy development
            content_agent     # For content creation
        ]
    )
    
    result = coordinator.do(task)
    print("\n🚀 Complete Campaign Plan:")
    print(result)
    return result


# ============================================
# STEP 5: Example 3 - Sequential Expert Consultation
# ============================================

def example_sequential_consultation():
    """Example: Agent consults specialists in sequence"""
    
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Sequential Expert Consultation")
    print("=" * 60)
    
    # Task 1: Research phase
    research_task = Task(
        description="Research top 5 AI agent frameworks and their unique features",
        tools=[research_agent]
    )
    
    research_results = coordinator.do(research_task)
    print("\n📊 Phase 1 - Research Complete")
    
    # Task 2: Strategy phase (uses research results)
    strategy_task = Task(
        description=f"""Based on this research: {research_results}
        
        Develop a competitive positioning strategy for a new AI framework
        focusing on safety-first features.""",
        tools=[strategy_agent]
    )
    
    strategy_results = coordinator.do(strategy_task)
    print("\n🎯 Phase 2 - Strategy Complete")
    
    # Task 3: Content phase (uses strategy)
    content_task = Task(
        description=f"""Based on this strategy: {strategy_results}
        
        Create 5 compelling tweets to announce our framework launch.""",
        tools=[content_agent]
    )
    
    final_content = coordinator.do(content_task)
    print("\n✍️ Phase 3 - Content Complete")
    print(final_content)
    
    return final_content


# ============================================
# STEP 6: Example 4 - Nested Agents
# ============================================

def example_nested_agents():
    """Advanced: Create a meta-coordinator that uses other agents"""
    
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Nested Agent Architecture")
    print("=" * 60)
    
    # Create a specialist coordinator
    campaign_team_agent = Agent(
        name="Campaign Team Lead",
        model="openai/gpt-4o",
        role="Team Coordinator",
        system_prompt="""You coordinate research, strategy, and content teams 
        to deliver comprehensive marketing campaigns."""
    )
    
    # The meta-coordinator uses the team coordinator as a tool!
    meta_coordinator = Agent(
        name="CMO",
        model="openai/gpt-4o",
        role="Chief Marketing Officer"
    )
    
    task = Task(
        description="""Plan a Q2 product launch campaign. 
        Coordinate with your team to deliver a complete plan.""",
        tools=[campaign_team_agent]  # Nested agent as tool
    )
    
    # The campaign_team_agent has access to specialist agents
    campaign_task = Task(
        description="Execute the Q2 campaign planning",
        tools=[research_agent, strategy_agent, content_agent]
    )
    campaign_team_agent.do(campaign_task)
    
    result = meta_coordinator.do(task)
    print("\n👔 CMO's Final Campaign Plan:")
    print(result)
    return result


# ============================================
# Main Execution
# ============================================

if __name__ == "__main__":
    print("""
    Upsonic Agent-as-Tool Demo
    ==============================
    
    This demo shows how to build hierarchical agent architectures
    where specialized agents work together as a coordinated team.
    
    Key Benefits:
    - Separation of concerns: each agent has specific expertise
    - Reusability: agents can be used across different tasks
    - Scalability: add new specialists without changing coordinator
    - Clarity: explicit delegation makes workflows transparent
    """)
    
    # Run examples (comment out what you don't need)
    example_simple_delegation()
    example_multi_agent_workflow()
    example_sequential_consultation()
    example_nested_agents()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
