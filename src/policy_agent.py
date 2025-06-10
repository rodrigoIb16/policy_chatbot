import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI

from tools import tool_list
from prompts import SYSTEM_PROMPT

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
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
    agent_kwargs={
        "system_message": SYSTEM_PROMPT,
        "input_key": "input"
    }
)


print("\nChatbot is ready! Type 'exit' to quit.\n")
while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    chat_history_str = memory.load_memory_variables({}).get("chat_history", "")
    result = agent.invoke({
        "input": query,
        "chat_history": chat_history_str
    })
    print(f"\nAI: {result}\n")