"""
Competitor Analysis Agent — Powered by Upsonic + Firecrawl

Automatically researches competitor websites and generates a structured
competitive intelligence report with feature comparisons, pricing analysis,
and strategic insights.

Architecture:
  Phase 1 — Research each competitor in its OWN agent call (keeps context small)
  Phase 2 — Synthesize all profiles into a comparison report (no scraping needed)

Usage:
    python main.py

Customize the competitors, industry, and focus areas in config.py.
"""

import json
from dotenv import load_dotenv

from upsonic import Agent, Task
from upsonic.tools.custom_tools.firecrawl import FirecrawlTools

from config import COMPETITOR_URLS, INDUSTRY, FOCUS_AREAS, MODEL
from schemas import CompetitorProfile, CompetitiveAnalysisReport

load_dotenv()

# ── Firecrawl Setup ──────────────────────────────────────────────
# Two lean tools:
#   • scrape_url  → scrape the homepage (with only_main_content)
#   • search_web  → find pricing, features, and other info via search
#
# map_website is intentionally disabled — it returns too many URLs and
# tempts the agent into scraping heavy doc pages that blow up context.

firecrawl = FirecrawlTools(
    enable_scrape=True,
    enable_crawl=False,
    enable_map=False,
    enable_search=True,
    enable_batch_scrape=False,
    enable_extract=False,
    enable_crawl_management=False,
    enable_batch_management=False,
    enable_extract_management=False,
    default_search_limit=3,
)

# ── Phase 1: Research Agent (one call per competitor) ────────────
research_agent = Agent(
    model=MODEL,
    system_prompt=(
        f"You are a competitive intelligence researcher in the {INDUSTRY} market.\n\n"
        f"Your job is to build a profile of ONE competitor. Follow these rules:\n"
        f"1. Scrape ONLY the competitor's homepage using scrape_url with only_main_content=True.\n"
        f"2. Use search_web to find their pricing info (query: '<company name> pricing plans').\n"
        f"3. Use search_web to find their key features (query: '<company name> features capabilities').\n"
        f"4. Do NOT scrape more than 1 page. Use search for everything else.\n"
        f"5. Extract concrete facts — real prices, real feature names, actual quotes.\n"
    ),
    tools=[firecrawl],
)

# ── Phase 2: Analysis Agent (no tools, just reasoning) ──────────
analysis_agent = Agent(
    model=MODEL,
    system_prompt=(
        f"You are a senior competitive intelligence analyst specializing in the "
        f"{INDUSTRY} market. You receive pre-researched competitor profiles and "
        f"synthesize them into a comprehensive comparison report.\n\n"
        f"Be specific and data-driven. Use the actual data from the profiles — "
        f"do not speculate or add information not present in the profiles."
    ),
)

# ── Build Focus Areas String ─────────────────────────────────────
focus_list = "\n".join(f"  - {area}" for area in FOCUS_AREAS)


def research_competitor(url: str) -> CompetitorProfile:
    """Phase 1: Research a single competitor (own context window)."""
    task = Task(
        description=f"""
Research the competitor at {url} for the {INDUSTRY} market.

Steps:
1. Scrape their homepage ({url}) with only_main_content=True to get an overview.
2. Search the web for "<company name> pricing plans" to find pricing details.
3. Search the web for "<company name> features" to find key capabilities.

Focus areas:
{focus_list}

Build a complete profile based on what you find.
""",
        response_format=CompetitorProfile,
    )
    return research_agent.print_do(task)


def generate_report(profiles: list[CompetitorProfile]) -> CompetitiveAnalysisReport:
    """Phase 2: Compare all profiles and generate the final report."""
    profiles_json = json.dumps(
        [p.model_dump() for p in profiles], indent=2, default=str
    )
    task = Task(
        description=f"""
Generate a competitive analysis report for the {INDUSTRY} market.

Here are the pre-researched competitor profiles:

{profiles_json}

## Requirements
- Include all competitor profiles in the report as-is.
- Create a feature comparison table (Markdown) with rows=features, columns=competitors, cells=✅/❌/partial.
- Create a pricing comparison table (Markdown) comparing plans and prices.
- Identify 5-8 key strategic insights about the competitive landscape.
- Highlight 3-5 market gaps or opportunities.
- Write a 3-5 sentence executive summary.
""",
        response_format=CompetitiveAnalysisReport,
    )
    return analysis_agent.print_do(task)


# ── Run the Analysis ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print(f"🔍 Competitor Analysis Agent — {INDUSTRY}")
    print("=" * 70)
    print()
    print(f"📋 Analyzing {len(COMPETITOR_URLS)} competitors:")
    for url in COMPETITOR_URLS:
        print(f"   → {url}")
    print()

    # Phase 1: Research each competitor individually
    profiles: list[CompetitorProfile] = []
    for i, url in enumerate(COMPETITOR_URLS, 1):
        print(f"🔎 [{i}/{len(COMPETITOR_URLS)}] Researching {url} ...")
        profile = research_competitor(url)
        profiles.append(profile)
        print(f"   ✅ {profile.name} — {profile.tagline[:60]}...")
        print()

    # Phase 2: Generate comparison report
    print("📊 Generating competitive analysis report...")
    print()
    result = generate_report(profiles)

    # ── Display the Report ───────────────────────────────────────
    print()
    print("=" * 70)
    print("📊 COMPETITIVE ANALYSIS REPORT")
    print("=" * 70)

    print(f"\n📌 Industry: {result.industry}")
    print(f"\n📝 Summary:\n{result.analysis_summary}")

    print("\n" + "-" * 70)
    print("🏢 COMPETITOR PROFILES")
    print("-" * 70)

    for i, comp in enumerate(result.competitors, 1):
        print(f"\n{'─' * 50}")
        print(f"  {i}. {comp.name}")
        print(f"     🌐 {comp.website}")
        print(f"     💬 {comp.tagline}")
        print(f"     📖 {comp.description}")
        print(f"     🎯 Target: {comp.target_audience}")
        print(f"     💰 Pricing: {comp.pricing_model}")
        if comp.pricing_tiers:
            for tier in comp.pricing_tiers:
                print(f"        • {tier}")
        print(f"     ✨ Key Features:")
        for feat in comp.key_features:
            print(f"        • {feat}")
        print(f"     🏆 Differentiators:")
        for diff in comp.differentiators:
            print(f"        • {diff}")

    print("\n" + "-" * 70)
    print("📊 FEATURE COMPARISON")
    print("-" * 70)
    print(result.feature_comparison)

    print("\n" + "-" * 70)
    print("💰 PRICING COMPARISON")
    print("-" * 70)
    print(result.pricing_comparison)

    print("\n" + "-" * 70)
    print("💡 KEY INSIGHTS")
    print("-" * 70)
    for insight in result.key_insights:
        print(f"  • {insight}")

    print("\n" + "-" * 70)
    print("🚀 OPPORTUNITIES")
    print("-" * 70)
    for opp in result.opportunities:
        print(f"  • {opp}")

    print("\n" + "=" * 70)
    print("✅ Analysis complete!")
    print("=" * 70)

    # ── Save to JSON ─────────────────────────────────────────────
    output_path = "report.json"
    with open(output_path, "w") as f:
        json.dump(result.model_dump(), f, indent=2, default=str)
    print(f"\n📁 Full report saved to {output_path}")

    # ── Save to Markdown ─────────────────────────────────────────
    md_path = "example_report.md"
    with open(md_path, "w") as f:
        f.write(f"# Competitive Analysis — {result.industry}\n\n")
        f.write(f"> *Auto-generated by the Competitor Analysis Agent (Upsonic + Firecrawl)*\n\n")
        f.write(f"## Executive Summary\n\n{result.analysis_summary}\n\n")
        f.write("---\n\n")
        f.write("## Competitor Profiles\n\n")
        for i, comp in enumerate(result.competitors, 1):
            f.write(f"### {i}. {comp.name}\n\n")
            f.write(f"- **Website:** {comp.website}\n")
            f.write(f"- **Tagline:** {comp.tagline}\n")
            f.write(f"- **Target Audience:** {comp.target_audience}\n")
            f.write(f"- **Pricing:** {comp.pricing_model}\n\n")
            f.write(f"{comp.description}\n\n")
            if comp.pricing_tiers:
                f.write("**Pricing Tiers:**\n\n")
                for tier in comp.pricing_tiers:
                    f.write(f"- {tier}\n")
                f.write("\n")
            f.write("**Key Features:**\n\n")
            for feat in comp.key_features:
                f.write(f"- {feat}\n")
            f.write("\n**Differentiators:**\n\n")
            for diff in comp.differentiators:
                f.write(f"- {diff}\n")
            f.write("\n---\n\n")
        f.write("## Feature Comparison\n\n")
        f.write(result.feature_comparison + "\n\n")
        f.write("## Pricing Comparison\n\n")
        f.write(result.pricing_comparison + "\n\n")
        f.write("## Key Insights\n\n")
        for insight in result.key_insights:
            f.write(f"- {insight}\n")
        f.write("\n## Opportunities\n\n")
        for opp in result.opportunities:
            f.write(f"- {opp}\n")
        f.write("\n---\n\n*Report generated using [Upsonic](https://github.com/upsonic/upsonic) + [Firecrawl](https://firecrawl.dev)*\n")
    print(f"📄 Markdown report saved to {md_path}")
