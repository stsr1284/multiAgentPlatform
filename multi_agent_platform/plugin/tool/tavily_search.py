from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langgraph.types import interrupt
from utils.config import settings


@tool
def tavily_search(
    query: str,
):
    """A search engine optimized for comprehensive, accurate, and trusted results.
    Useful for when you need to answer questions about current events.
    Input should be a search query."""

    response = interrupt(
        "travily_search는 웹 검색을 위한 도구입니다.\n과금이 발생합니다. yes or no?"
    )
    if response == "no":
        return "검색을 취소했습니다."
    elif response == "yes":
        return TavilySearchResults(
            k=6, tavily_api_key=settings.TAVILY_API_KEY, name="tavily_search"
        )._run(query)


async def register(registry):
    await registry.register(tavily_search)
