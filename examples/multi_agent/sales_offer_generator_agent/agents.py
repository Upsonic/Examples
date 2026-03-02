from upsonic import Agent
from tools import SearchTools

class SalesAgents:
    """
    Factory class to create specialized agents for the Sales Offer Generator.
    """

    def product_researcher(self) -> Agent:
        return Agent(
            name="Product Researcher",
            role="Search Specialist",
            goal="Identify the best products matching customer needs using real market data.",
            tools=[SearchTools()],
            model="openai/gpt-4o"
        )

    def pricing_strategist(self) -> Agent:
        return Agent(
            name="Pricing Strategist",
            role="Market Analyst",
            goal="Analyze product pricing and determine a competitive offer strategy.",
            tools=[SearchTools()], # Needs search to verify competitor prices if needed
            model="openai/gpt-4o"
        )

    def offer_writer(self) -> Agent:
        return Agent(
            name="Creative Copywriter",
            role="Sales Writer",
            goal="Draft a compelling, personalized sales offer email.",
            model="openai/gpt-4o"
        )
