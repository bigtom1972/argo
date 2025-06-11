import os
import json
from langchain import LLM, PromptTemplate
from langchain.llms import DeepSeekChatLLM

llm = DeepSeekChatLLM(api_key=os.environ["DEEPSEEK_API_KEY"])
template = PromptTemplate(input_variables=["user_input"], template="You are an AI chatbot.  You are asked to generate a response to a given user input.  The response should be in the following format: {user_input}: {response}.")

def chatbot(message):
    output = llm.generate(template.format(user_input=message))
    return json.loads(output)["response"]
m