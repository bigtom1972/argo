from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from langchain_deepseek import ChatDeepSeek
from openai import OpenAI
import os
import getpass

# Set up DeepSeek API key
if not os.environ.get("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")

# Initialize DeepSeek chat model
# Replace 'deepseek-model-name' with the actual model name (e.g., 'DeepSeek-R1') from DeepSeek's documentation
model = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",  # Assuming 'deepseek' is the provider name; verify with DeepSeek's docs
    temperature=0.7,  # Standard parameter for controlling randomness ()[](https://python.langchain.com/docs/concepts/chat_models/)
    max_tokens=512    # Standard parameter for limiting response length ()[](https://python.langchain.com/docs/concepts/chat_models/)
)

llm = ChatDeepSeek(
    model_name="deepseek-chat",  # Use the correct model name as per DeepSeek's documentation
    temperature=0.7,
    max_tokens=512
)

client = OpenAI(
    api_key="3b638f0b-41d5-4a10-90f8-a0c909509dbe",
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    model="doubao-1-5-pro-32k-character-250228"
    
)

# Define prompt template
system_template = "You are a helpful assistant with advanced reasoning capabilities. Respond concisely and accurately to user queries."
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", "{user_input}")
])

# Create chain
# chain = prompt_template | llm


# Function to interact with the chatbot
def chat_with_bot():
    print("Welcome to the DeepSeek Chatbot! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        # Invoke the chain with user input
        response = chain.invoke({"user_input": user_input})
        print(f"Bot: {response.content}")

if __name__ == "__main__":
    chat_with_bot()