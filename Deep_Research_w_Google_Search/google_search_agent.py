import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
from agents import function_tool
from googleapiclient.discovery import build
from pydantic import BaseModel, Field
from typing import Optional, List

load_dotenv(override=True)
API_KEY: Optional[str] = os.environ.get('GOOGLE_SEARCH_API_KEY')
SEARCH_CONTEXT: Optional[str] = os.environ.get('GOOGLE_SEARCH_CONTEXT')


class SearchResult(BaseModel):
    title: str = Field(description="The title of the search result.")
    link: str = Field(description="The URL of the search result.")
    content: str = Field(description="The content snippet of the search result.")


class SearchResults(BaseModel):
    results: List[SearchResult] = Field(description="A list of search results.")


def fetch_page_content(url: str) -> str:
    """
    Fetch a web page and return a small text-only preview of its content.

    Returns the first ~2000 characters of extracted text, or an error description.
    """
    try:
        page = requests.get(url, timeout=10)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.get_text()
        return text[:2000]
    except Exception as exc:
        return f"Error fetching {url}: {str(exc)}"


@function_tool
def run_google_search(query: str) -> List[dict[str, str]]:
    """
    Run a Google Custom Search for the provided query and return a list of result dicts
    including title, link, and a short content preview fetched from each page.
    """
    if not API_KEY or not SEARCH_CONTEXT:
        return []

    search_results = SearchResults(results=[])
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = (
        service.cse()
        .list(
            q=f'{query}',
            cx=f'{SEARCH_CONTEXT}',
        )
        .execute()
    )

    for item in res.get('items', []):
        content = fetch_page_content(item.get('link', ''))
        search_results.results.append(
            SearchResult(
                title=item.get('title', ''),
                link=item.get('link', ''),
                content=content,
            )
        )

    # Convert to primitive dicts for tool friendliness
    return [result.model_dump() for result in search_results.results]
