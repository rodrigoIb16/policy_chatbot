from langchain.tools import Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from retrieval import hybrid_retriever
import logging

logger = logging.getLogger(__name__)

# Query Rewriting Prompt
rewriter_prompt = PromptTemplate.from_template(
    "Rewrite this query to retrieve the most relevant company policy documents: {query}"
)
rewriter_chain = LLMChain(llm=ChatOpenAI(temperature=0.0), prompt=rewriter_prompt)

def rewrite_query(raw_query: str) -> str:
    return rewriter_chain.invoke({"query": raw_query})["text"].strip()

# Follow-up Clarification Prompt
clarification_prompt = PromptTemplate.from_template(
    "Conversation so far:\n{history}\n\nUser's follow-up question:\n{question}\n\nRephrase the question so it’s fully self-contained and clear:"
)
clarifier_chain = LLMChain(llm=ChatOpenAI(temperature=0.0), prompt=clarification_prompt)

def clarify_followup(question: str, history: str) -> str:
    return clarifier_chain.invoke({"question": question, "history": history})["text"].strip()

# HR & Company Policy QA Tool
def policy_docs_tool(query: str, chat_history: str = "") -> str:
    clarified_query = clarify_followup(query, chat_history) if chat_history else query
    logger.info(f"[Original query]: {query}")
    logger.info(f"[Clarified query]: {clarified_query}")

    clean_query = rewrite_query(clarified_query)
    logger.info(f"[Rewritten query]: {clean_query}")

    docs = hybrid_retriever().invoke(clean_query)
    return "\n\n".join([doc.page_content for doc in docs]) if docs else "Sorry, I couldn’t find any relevant policy documents for that."

tool_list = [
    Tool.from_function(
        func=policy_docs_tool,
        name="PolicyDocs",
        description=(
            "Answer questions using internal company documentation, such as HR policies, "
            "remote work rules, reimbursement procedures, and employee benefits. "
            "Input should be a natural language question like 'What’s our WFH policy?'"
        )
    )
]
