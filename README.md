# 🔍 AI Research Agent

An autonomous AI agent that searches the web and synthesizes answers with sources.

Built as a portfolio project to demonstrate AI Engineering skills with autonomous agents.

🔗 **Live Demo:** [Try it on HuggingFace Spaces](https://huggingface.co/spaces/mjebb21/ai-research-agent)

---

## 🧠 How it works

1. User asks a question
2. Agent decides if web search is needed (ReAct pattern)
3. If yes — searches the web via DuckDuckGo
4. Synthesizes answer from search results with source citations
5. If no — answers from LLM knowledge directly

This is a real autonomous agent — it decides itself when to use tools.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Llama 3.3 70B via Groq API |
| Framework | LangChain |
| Web Search | DuckDuckGo |
| UI | Streamlit (custom CSS) |
| Hosting | HuggingFace Spaces |

---

## 🚀 Run locally

```bash
git clone https://github.com/mjebb/ai-research-agent.git
cd ai-research-agent
pip install -r requirements.txt
cp .env.example .env
# Add your GROQ_API_KEY to .env
streamlit run app.py
```

---

## 💡 Key Concepts Demonstrated

- **Autonomous agents** with decision-making logic
- **ReAct pattern** (Reason → Act → Observe)
- **Tool use** — agent decides when to call search tool
- **LLM integration** via LangChain and Groq
- **Custom UI/UX** with Streamlit

---

*Created by Musa Jabbarli*