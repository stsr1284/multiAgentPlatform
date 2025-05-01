from langchain.agents import tool  # test


@tool
def search_urls(urls: list[str], urllens: int):
    """A simple search tool that takes a list of URLs and returns a list of search results."""
    if not isinstance(urls, list):
        raise ValueError("URLs must be a list.")
    if not urls:
        raise ValueError("URLs cannot be empty.")
    if not all(isinstance(url, str) for url in urls):
        raise ValueError("All URLs must be strings.")
    return f"Searching the following URLs: {urls}"


async def register(registry):
    await registry.register(search_urls)


# @tool
# def test_tool2(urls: list[str], urllens: int):
#     """A simple search tool that takes a list of URLs and returns a list of search results."""
#     if not isinstance(urls, list):
#         raise ValueError("URLs must be a list.")
#     if not urls:
#         raise ValueError("URLs cannot be empty.")
#     if not all(isinstance(url, str) for url in urls):
#         raise ValueError("All URLs must be strings.")
#     return f"Searching the following URLs: {urls}"
