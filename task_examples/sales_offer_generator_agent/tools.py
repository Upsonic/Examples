from upsonic.tools import tool, ToolKit
from ddgs import DDGS


class SearchTools(ToolKit):
    """
    Toolkit for performing internet searches to gather real-time data
    about products, competitors, and market trends.
    """

    @tool
    def search_internet(self, query: str) -> str:
        """
        Searches the internet for a general query.
        Useful for finding product specs, reviews, or general market info.

        Args:
            query: The search string (e.g., "latest specialized gaming laptops 2024").

        Returns:
            A string summary of the top search results.
        """
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        
        if not results:
            return "No results found."
            
        formatted_results = []
        for r in results:
            formatted_results.append(f"Title: {r['title']}\nLink: {r['href']}\nSnippet: {r['body']}")
            
        return "\n\n".join(formatted_results)

    @tool
    def find_product_prices(self, product_name: str) -> str:
        """
        Specifically searches for pricing information for a given product.

        Args:
            product_name: The specific name of the product (e.g., "MacBook Pro M3 Max").

        Returns:
            A list of found price points and retailers.
        """
        query = f"{product_name} price buy online"
        return self.search_internet(query)
