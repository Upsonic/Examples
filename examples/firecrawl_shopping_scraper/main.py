import os
from dotenv import load_dotenv
from upsonic import Agent, Task
from upsonic.tools.custom_tools.firecrawl import FirecrawlTools

load_dotenv()

# Only enable scrape_url — the agent does not need crawling or search for this task
firecrawl = FirecrawlTools(
    enable_scrape=True,
    enable_crawl=False,
    enable_map=False,
    enable_search=False,
    enable_batch_scrape=False,
    enable_extract=False,
    enable_crawl_management=False,
    enable_batch_management=False,
    enable_extract_management=False,
)

task = Task(
    description="""
    Scrape the homepage of http://books.toscrape.com and extract ALL
    products visible on the page.

    For each product return:
      - Name  (full book title)
      - Price (as shown, e.g. '£51.77')
      - Rating (word form, e.g. 'Three')

    Format the output as a Markdown table:

    | # | Book Title | Price | Rating |
    |---|-----------|-------|--------|

    Sort by price descending. Add a one-line summary at the top
    with the total number of products found and the price range.
    """
)

agent = Agent(
    model="anthropic/claude-sonnet-4-6",
    tools=[firecrawl],
)

result = agent.do(task)
print(result)
