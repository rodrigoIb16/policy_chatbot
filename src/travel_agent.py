# src/travel_agent.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.api_key import api_key
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# 🔒 Ensure API key is set
if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please configure it in your .env file.")

# ✅ Load markdown files from knowledge base
loader = DirectoryLoader("knowledge_base", glob="**/*.md", loader_cls=TextLoader)
raw_documents = loader.load()

# ✂️ Split documents into manageable chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
documents = text_splitter.split_documents(raw_documents)

# 🔎 Create vector store for retrieval
embedding = OpenAIEmbeddings(openai_api_key=api_key)
vector_store = Chroma.from_documents(documents=documents, embedding=embedding)
retriever = vector_store.as_retriever()

# 💬 Set up the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, openai_api_key=api_key)

# 🔗 Create the Retrieval-QA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 🧪 CLI interface
print("\n🧳 Travel Chatbot is ready! Ask your travel questions (type 'exit' to quit)\n")

while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    response = qa_chain.run(query)
    print(f"\nAI: {response}\n")
