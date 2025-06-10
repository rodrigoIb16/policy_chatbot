
🧾 HRBot: Internal Policy Chatbot
=================================

HRBot is an internal conversational agent that helps employees get instant answers to HR and operations-related questions. It uses a combination of retrieval-augmented generation (RAG), vector search, and large language models (LLMs) to ground responses in actual company documentation.

📌 Features
-----------
- ✅ Answers questions about remote work, reimbursements, leave policies, and more
- 📄 Supports internal `.md` policy files as the knowledge base
- 🧠 Uses a hybrid retriever (dense + sparse) with compression
- 🤖 Powered by OpenAI’s GPT and LangChain tools
- 🛠️ Easy to extend with more tools

🗂️ Project Structure
--------------------
travel_chatbot/
├── knowledge_base/         # Internal HR policy .md files
├── src/
│   ├── policy_agent.py     # Main entrypoint for the chatbot
│   ├── tools.py            # Defines LangChain tools
│   ├── prompts.py          # Defines system prompt
│   └── retrieval.py        # Implements hybrid retriever logic
└── README.txt              # This file

🚀 Setup Instructions
---------------------

1. Clone the Repository
```bash
git clone https://github.com/yourname/hrbot.git
cd hrbot
```

2. Create and Activate a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

Dependencies include:
- langchain
- langchain-openai
- chromadb
- tiktoken

4. Add Your OpenAI API Key
```bash
export OPENAI_API_KEY=your-key-here
```

Or set it in `.env` and use `dotenv`.

🧠 How It Works
---------------

1. Load Policy Docs: All `.md` files in the `knowledge_base/` folder are loaded, split into chunks, and indexed.

2. Hybrid Retrieval: 
   - Dense retrieval via OpenAI embeddings and Chroma
   - Sparse retrieval via BM25
   - Combined using an EnsembleRetriever

3. Compression: LLM-based extractor summarizes relevant chunks.

4. Tool Use: Agent decides whether to call `PolicyDocs` or respond directly.

5. Answer: LLM responds with helpful, grounded information.

🧪 Run the Agent
----------------
```bash
python src/policy_agent.py
```

You'll enter a chat loop like this:
```
You: What’s the reimbursement policy for home office?
AI: The company reimburses up to $300 annually for...
```

Type `exit` to quit.

🧩 Customization
----------------
- Add `.md` files in `knowledge_base/` to expand the knowledge base.
- Modify `tools.py` to include more tools.
- Adjust the prompt in `prompts.py` for tone/scope.

🔒 Disclaimer
-------------
This tool is for internal informational use only. Always confirm with HR for policy-critical matters.

📬 Contact
----------
Built by Rodrigo García. Questions or ideas? Reach out!
