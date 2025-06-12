from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import os
import getpass

# Set up DeepSeek API key
if not os.environ.get("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")

# Initialize DeepSeek chat model
# Replace 'deepseek-model-name' with the actual model name from DeepSeek's documentation
model = init_chat_model(
    model="deepseek-model-name",
    model_provider="deepseek",
    temperature=0.7,
    max_tokens=512
)

# Load and process PDF
def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore.as_retriever()

# Define prompt template
system_template = """You are an AI assistant that answers questions based on the provided PDF content. Use the following context to answer the user's question accurately. If the answer isn't in the context, say so.
Context: {context}"""
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", "{user_input}")
])

# Define LangGraph state
class ChatState:
    def __init__(self):
        self.messages = []
        self.context = ""

# Define node for processing user input
def process_input(state, retriever):
    user_input = state.messages[-1].content
    # Retrieve relevant documents
    docs = retriever.get_relevant_documents(user_input)
    context = "\n".join([doc.page_content for doc in docs])
    # Format prompt with context
    prompt = prompt_template.format(context=context, user_input=user_input)
    # Invoke model
    response = model.invoke(prompt)
    state.messages.append(SystemMessage(content=response.content))
    return state

# Build LangGraph workflow
def build_graph(retriever):
    workflow = StateGraph(ChatState)
    workflow.add_node("process_input", lambda state: process_input(state, retriever))
    workflow.set_entry_point("process_input")
    workflow.add_edge("process_input", END)
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

# Main chat function
def chat_with_pdf_bot(pdf_path):
    retriever = load_pdf(pdf_path)
    graph = build_graph(retriever)
    print("Welcome to the PDF Q&A Chatbot! Type 'quit' to exit.")
    state = ChatState()
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        state.messages.append(HumanMessage(content=user_input))
        state = graph.invoke(state)
        print(f"Bot: {state.messages[-1].content}")

if __name__ == "__main__":
    # Replace with your PDF file path
    pdf_path = "sample.pdf"
    chat_with_pdf_bot(pdf_path)