from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema



prompt_template = """You are an SEO expert helping to organize keyword data into structured pages.

        **Instructions:**
        - Group keywords based on the 'cluster' label.
        - Exclude keywords with less than 50 monthly searches.
        - Generate a structured JSON with:
            - Page Title : An SEO-optimised, user-friendly Page or Article title for the grouped keywords. max 120 characters
            - Keywords (all from the same cluster): A list of semantically related keywords that belong to the same group. Each keyword should be in a separate row within this column.
            - Monthly Search Volume (dictionary of keywords and search volume)
            - Intent (Awareness, Interest, Consideration, Conversion):Define where a page fits within the conversion funnel and label it accordingly, but only the pge, not all the keywords
                Awareness: The user is discovering and learning about a topic (e.g., informational content).
                Interest: The user is researching possible solutions (e.g., guides, comparisons).
                Consideration: The user is evaluating different products/services (e.g., reviews, case studies).
                Conversion: The user is ready to take action (e.g., purchase pages, consultations).
            - Suggested URL Structure : Propose an SEO-friendly URL that reflects the funnel stage, page hierarchy (pillar pages & child pages), and logical structuring. Ensure parent pages are listed first, followed by their respective child pages.

        Provide only the structured **JSON output** without any explanations or extra text, only retun Page Title,Keywords,Intent and Suggested URL Structure.

        **Keywords JSON:**
        {keywords_json}

"""

# prompt_template = """

# Objective:
#     You are an SEO expert tasked with organizing keyword data into structured pages based on predefined clusters. Your goal is to generate SEO-optimized page titles, categorize keywords by intent, and suggest a logical URL structure.

# Instructions:
#     1.Group Keywords by Cluster:

#         - Process keywords that belong to the same cluster (provided in the input).
#         - Exclude any keyword with a monthly search volume below 50.
        
#     2.Generate a Structured JSON Output (No extra text, only return JSON) with the following fields:

#         - Page Title: An SEO-optimized, user-friendly title for the grouped keywords. (Max: 120 characters)
#         - Keywords: A list of semantically related keywords within the same cluster. Each keyword should be in a separate row.
#         - Monthly Search Volume: A dictionary mapping each keyword to its monthly search volume.
#         - Intent (Awareness, Interest, Consideration, Conversion): Assign a conversion funnel stage only to the page (not individual keywords).
#            - Awareness: Users are discovering and learning (e.g., informational content).
#            - Interest: Users are researching possible solutions (e.g., guides, comparisons).
#            - Consideration: Users are evaluating different options (e.g., reviews, case studies).
#            - Conversion: Users are ready to take action (e.g., purchase pages, consultations).
#         - Suggested URL Structure: Generate an SEO-friendly URL reflecting the funnel stage, logical hierarchy (pillar & child pages), and keyword relevance. Ensure parent pages are listed first, followed by child pages.
# """
    
prompt = PromptTemplate(
    input_variables=["keywords_json"],
    template=prompt_template
)