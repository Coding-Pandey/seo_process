from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema



prompt_template = """You are an SEO expert helping to organize keyword data into structured pages.

        **Instructions:**
        - Group keywords based on the 'cluster' label.
        - Exclude keywords with less than 50 monthly searches.
        - Generate a structured JSON with:
        - Page Title
        - Keywords (all from the same cluster)
        - Monthly Search Volume (dictionary of keywords and search volume)
        - Intent (Awareness, Interest, Consideration, Conversion)
        - Suggested URL Structure

        Provide only the structured **JSON output** without any explanations or extra text, only retun Page Title,Keywords,Intent and Suggested URL Structure.

        **Keywords JSON:**
        {keywords_json}

"""


prompt = PromptTemplate(
    input_variables=["keywords_json"],
    template=prompt_template
)