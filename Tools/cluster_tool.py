from langchain_core.tools import Tool

# Define tool function for getting current time
def Seo_keyword_search(keywords: list ) -> str:
    """Returns the search keyword
    Args:
        keywords: keyword searched by seo google ads client
    Returns:
        list of keywords with Avg. monthly search
    """

    return keywords


# Define available tools
tools = [
    Tool(
        name="keywords search",
        func=Seo_keyword_search,
        description="Returns the list of keywords with Avg. monthly search. You have to provide list of keyword from prompts, just use this tool directly."
    )
]