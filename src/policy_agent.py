import sys, os
import json
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI

from tools import tool_list
from prompts import SYSTEM_PROMPT

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2) #temperature=0.2: Makes the output a bit more deterministic
memory = ConversationSummaryBufferMemory(
    llm=ChatOpenAI(temperature=0),
    memory_key="chat_history",
    input_key="input",
    return_messages=True
)

agent = initialize_agent(
    tools=tool_list,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=False,
    memory=memory,
    handle_parsing_errors=True,
    agent_kwargs={
        "system_message": SYSTEM_PROMPT,
        "input_key": "input"
    }
)

query = os.getenv("CHAT_QUERY")
if query:
    chat_history_str = memory.load_memory_variables({}).get("chat_history", "")
    result = agent.invoke({
        "input": query,
        "chat_history": chat_history_str
    })
    print(json.dumps({"output": result["output"]}))
