"""
Restaurant Scout Agent — Powered by Upsonic + Apify

Searches Google Maps for restaurants or food spots matching a natural language
query (e.g. "cheap falafel in Kadıköy") and saves the results as a Markdown file.

Usage:
    python main.py
"""

from upsonic import Agent, Task
from upsonic.tools.custom_tools.apify import ApifyTools
from dotenv import load_dotenv
import os

load_dotenv()

# ApifyTools registers the Google Maps crawler as a tool.
# The agent automatically receives the Actor's full input schema,
# so it knows exactly which parameters to pass based on the user's query.
#
# actor_defaults pre-sets config that never needs to change:
#   - maxCrawledPlacesPerSearch: limit results to avoid token overflow
#   - maxImages: skip images (not needed for text output)
#   - outputFormats: return compact markdown instead of verbose JSON
#
# timeout=180.0 overrides the 30s default — the Actor takes ~60-90s to run.
# max_retries=0 prevents parallel duplicate runs on timeout.
agent = Agent(
    "anthropic/claude-sonnet-4-5",
    tools=[
        ApifyTools(
            actors=["compass/crawler-google-places"],
            apify_api_token=os.getenv("APIFY_API_KEY"),
            actor_defaults={
                "compass/crawler-google-places": {
                    "maxCrawledPlacesPerSearch": 10,
                    "maxImages": 0,
                    "outputFormats": ["markdown"],
                }
            },
            timeout=180.0,
            max_retries=0,
        )
    ],
)

task = Task("Tell me cheap and tasty falafel places in Kadıköy, Istanbul")
agent.print_do(task)

with open("results.md", "w") as f:
    f.write(task.response)

print("\n📄 Results saved to results.md")
