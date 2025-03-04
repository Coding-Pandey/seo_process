import sys
import os
import json
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model import chatgpt_model
from prompts.cluster_URL_prompt import prompt


# def url_agent(items):
#     try:
#         # Initialize memory
#         memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
#         # Initialize agent
#         agent = initialize_agent(
#             agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
#             llm=chatgpt_model,
#             tools=[],
#             memory=memory,
#             verbose=True,
#             handle_parsing_errors=True
#         )
        
 
#         formatted_prompt = prompt.format(keywords_json=json.dumps(items, indent=4))

#         response = agent.invoke(formatted_prompt)
        
#         output_json = response.get('output', "")
#         print(output_json)
        
#         return output_json
    
#     except Exception as e:
#         print(f"Error in url_agent: {e}")
#         return None



# Define the async URL agent function
async def url_agent(items):
    try:
        # Initialize memory
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Initialize agent
        agent = initialize_agent(
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            llm=chatgpt_model,
            tools=[],
            memory=memory,
            verbose=True,
            handle_parsing_errors=True
        )
        
        formatted_prompt = prompt.format(keywords_json=json.dumps(items, indent=4))
        
        response = await agent.ainvoke(formatted_prompt)
        
        output_json = response.get('output', "")
        print(output_json)
        
        return output_json
    
    except Exception as e:
        print(f"Error in url_agent: {e}")
        return None