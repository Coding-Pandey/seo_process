import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model import chatgpt_model
# from Tools.keyword_tool import tools
# from prompts.keywords_prompt import prompt
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def query_keyword_suggestion(PROMPT, keywords=None, description=None):
    if not keywords and not description:
        raise ValueError("At least one of 'keywords' or 'description' must be provided.")

    query = f"Keywords: {keywords or ''}\nDescription: {description or ''}"
    messages = [
        {'role' : 'system', 'content' : PROMPT},
        {'role' : 'user', 'content' : query}
        ]
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, response_format={ "type": "json_object" })
    return response.choices[0].message.content


def query_keywords_description(PROMPT, keywords=None, description=None):
    if not keywords and not description:
        raise ValueError("At least one of 'keywords' or 'description' must be provided.")

    query = f"Keywords: {keywords or ''}\nDescription: {description or ''}"
    messages = [
        {'role': 'system', 'content': PROMPT},
        {'role': 'user', 'content': query}
    ]
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_keywords",
                "description": "Returns a list of relevant keywords based on the input query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["keywords"]
                }
            }
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "get_keywords"}}
    )

    tool_calls = response.choices[0].message.tool_calls  
    if tool_calls:
        arguments = tool_calls[0].function.arguments
 
        arguments_dict = eval(arguments)
        print(arguments_dict)


    return arguments_dict