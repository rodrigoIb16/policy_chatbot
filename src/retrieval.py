import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever, EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers.document_compressors import LLMChainExtractor

PERSIST_DIR = "chroma_store"

def hybrid_retriever():
    # Load markdown files from the knowledge base
    loader = DirectoryLoader("knowledge_base", glob="**/*.md", loader_cls=TextLoader)
    raw_docs = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    documents = splitter.split_documents(raw_docs)

    # Dense retriever
    embeddings = OpenAIEmbeddings()

    # Check if vectorstore already exists
    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        # Load existing persisted vectorstore
        vectorstore = Chroma(embedding_function=embeddings, persist_directory=PERSIST_DIR)
    else:
        # Create and persist new vectorstore
        vectorstore = Chroma.from_documents(documents, embeddings, persist_directory=PERSIST_DIR)
        vectorstore.persist()  # Only call persist when building for the first time

    dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Sparse retriever (BM25)
    sparse_retriever = BM25Retriever.from_documents(documents)
    sparse_retriever.k = 5

    # Combine both retrievers
    hybrid = EnsembleRetriever(
        retrievers=[dense_retriever, sparse_retriever],
        weights=[0.5, 0.5]
    )

    # LLM-based compressor
    compressor = LLMChainExtractor.from_llm(ChatOpenAI(temperature=0.0))

    return ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=hybrid
    )
