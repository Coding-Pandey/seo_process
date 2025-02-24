from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

# gemini_model = ChatGoogleGenerativeAI(
#         model='gemini-pro',
#         temperature=0.2,
#         google_api_key=os.getenv("GOOGLE_API_KEY")
#     )
# gpt-4, gpt-3.5-turbo-0125

chatgpt_model = ChatOpenAI(model="gpt-4o-mini",temperature=0.2,api_key=os.getenv("OPENAI_API_KEY"))
# result = chatgpt_model.invoke("hello whatup")
# print(result)