from langchain_core.tools import Tool

# Define tool function for getting current time
def Seo_keyword_search(keywords: list ) -> str:
    """Returns the search keyword
    Args:
        keywords: keyword searched by seo google ads client
    Returns:
        list of keywords with Avg. monthly search
    """
    import pandas as pd

    # Load CSV file
    csv_file = r"C:\Users\nickc\OneDrive\Desktop\SEO\data\input test 2 - input test 2.csv"  # Replace with your file path
    df = pd.read_csv(csv_file)

    # Convert DataFrame to JSON
    json_data = df.to_json(orient="records", indent=4)

    # Print or save the JSON data
    # print(json_data)

    return json_data


# Define available tools
tools = [
    Tool(
        name="keywords search",
        func=Seo_keyword_search,
        description="Returns the list of keywords with Avg. monthly search. You have to provide list of keyword from user input, just use this tool directly."
    )
]