import os
from typing import Dict
from dotenv import load_dotenv
from firecrawl import FirecrawlApp

def get_website_data(url: str) -> Dict[str, str]:
    """
    Fetch website data using the Firecrawl API.

    :param url: The URL of the website to scrape.
    :return: A dictionary containing the scraped website data.
    """
    load_dotenv()  
    api_key: str = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("API key is required. Set the FIRECRAWL_API_KEY environment variable.")
    app = FirecrawlApp(api_key=api_key)
    scrape_result: Dict[str, str] = app.scrape_url(url=url)
    return scrape_result