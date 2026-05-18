import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchResults
from dotenv import load_dotenv
import time
import os

load_dotenv()

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS — premium minimal design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    #MainMenu, footer, header {visibility: hidden;}

    .stApp {
        background-color: #0a0a0a;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
        color: #e5e5e5;
    }

    /* Header with gradient */
    .main-header {
        background: linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%);
        padding: 2rem 0 1.5rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid #222;
    }

    .logo-text {
        font-size: 2.5rem;
        font-weight: 600;
        background: linear-gradient(135deg, #ffffff 0%, #888888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -2px;
        margin: 0;
    }

    .logo-subtitle {
        color: #666;
        font-size: 0.95rem;
        font-weight: 400;
        margin-top: 0.5rem;
        letter-spacing: 0.3px;
    }

    .badge {
        display: inline-block;
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 100px;
        padding: 4px 12px;
        font-size: 0.7rem;
        color: #888;
        margin-right: 8px;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .badge-active {
        background: #ffffff;
        color: #000000;
        border-color: #ffffff;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f0f0f;
        border-right: 1px solid #1f1f1f;
    }

    [data-testid="stSidebar"] h3 {
        color: #ffffff;
        font-weight: 500;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 1rem;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: #111111;
        border: 1px solid #1f1f1f;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }

    [data-testid="stChatMessage"]:hover {
        border-color: #2a2a2a;
    }

    /* Input */
    [data-testid="stChatInput"] {
        background-color: #141414;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
    }

    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        font-size: 0.95rem;
    }

    /* Buttons */
    .stButton button {
        background-color: #ffffff;
        color: #000000;
        border: none;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.85rem;
        padding: 0.5rem 1.2rem;
        transition: all 0.2s;
    }

    .stButton button:hover {
        background-color: #e0e0e0;
        transform: translateY(-1px);
    }

    /* Example question cards */
    .example-card {
        background: #111111;
        border: 1px solid #1f1f1f;
        border-radius: 8px;
        padding: 1rem;
        cursor: pointer;
        transition: all 0.2s;
        height: 100%;
    }

    .example-card:hover {
        background: #161616;
        border-color: #333;
    }

    .example-icon {
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }

    .example-text {
        color: #aaa;
        font-size: 0.85rem;
        line-height: 1.4;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.4rem;
        font-weight: 400;
        color: #ffffff;
    }

    [data-testid="stMetricLabel"] {
        color: #666;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 500;
    }

    /* Code */
    code {
        background-color: #1a1a1a !important;
        color: #e5e5e5 !important;
        border: 1px solid #2a2a2a;
        border-radius: 4px;
        padding: 2px 6px;
        font-size: 0.85rem;
    }

    /* Status */
    [data-testid="stStatus"] {
        background-color: #111111;
        border: 1px solid #1f1f1f;
        border-radius: 6px;
    }

    /* Welcome screen */
    .welcome-title {
        font-size: 1.3rem;
        color: #ffffff;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    .welcome-subtitle {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #444;
        font-size: 0.75rem;
        padding: 2rem 0 1rem 0;
        margin-top: 3rem;
        border-top: 1px solid #1a1a1a;
        letter-spacing: 0.5px;
    }

    /* Response time pill */
    .time-pill {
        display: inline-block;
        background: #1a1a1a;
        color: #888;
        font-size: 0.7rem;
        padding: 2px 8px;
        border-radius: 100px;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* Hide chat input label */
    [data-testid="stChatInput"] label {display: none;}

    /* Divider */
    hr {
        border-color: #1f1f1f !important;
        margin: 1.5rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Settings")
    show_thinking = st.checkbox("Show agent reasoning", value=True)
    max_sources = st.slider("Sources per query", 1, 5, 3)

    st.markdown("---")

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### Statistics")

    if "total_queries" not in st.session_state:
        st.session_state.total_queries = 0
    if "total_time" not in st.session_state:
        st.session_state.total_time = 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Queries", st.session_state.total_queries)
    with col2:
        st.metric("Avg time", f"{st.session_state.total_time:.1f}s")

    st.markdown("---")
    st.markdown("### Tech stack")
    st.markdown(
        '<span class="badge badge-active">LangChain</span>'
        '<span class="badge badge-active">Groq</span><br><br>'
        '<span class="badge">Streamlit</span>'
        '<span class="badge">DuckDuckGo</span>',
        unsafe_allow_html=True
    )

# Header
st.markdown("""
<div class="main-header">
    <h1 class="logo-text">◆ AI Research Agent</h1>
    <p class="logo-subtitle">Autonomous agent with web search capabilities — built on Llama 3.3 70B</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_tools():
    search = DuckDuckGoSearchResults(num_results=5)
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1
    )
    return search, llm


search, llm = load_tools()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome screen with examples — only when chat is empty
if len(st.session_state.messages) == 0:
    st.markdown('<p class="welcome-title">Start with a question</p>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-subtitle">Or try one of these examples</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    examples = [
        ("◇", "What are the latest developments in AI this month?", col1),
        ("○", "Compare Python and Rust for backend development", col2),
        ("△", "What is the population of Berlin in 2026?", col3),
    ]

    for icon, text, col in examples:
        with col:
            if st.button(f"{icon}  {text}", key=text, use_container_width=True):
                st.session_state.pending_question = text
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle pending question from example buttons
question = None
if "pending_question" in st.session_state:
    question = st.session_state.pending_question
    del st.session_state.pending_question

# Chat input
chat_input = st.chat_input("Ask anything...")
if chat_input:
    question = chat_input

if question:
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        start_time = time.time()

        with st.status("Analyzing question...", expanded=show_thinking) as status:

            decision_prompt = f"""You are an AI agent. Decide if you need to search the web.
Answer ONLY with YES or NO.

Search if: question is about current events, facts, people, places, recent info.
Don't search if: it's a simple greeting, opinion, or general knowledge.

Question: {question}
Decision:"""

            decision = llm.invoke(decision_prompt).content.strip().upper()

            if show_thinking:
                st.markdown(f"**Search needed:** `{decision}`")

            if "YES" in decision:
                status.update(label="Searching the web...")
                search_results = search.run(question)

                if show_thinking:
                    st.markdown(f"**Retrieved sources:** `{max_sources}`")

                status.update(label="Synthesizing answer...")

                answer_prompt = f"""You are a research assistant. Answer the question 
based on search results below. Be concise — max 4 sentences.
Include 1-2 source links at the end in this format:

**Sources:**
- [Title](url)

Search results: {search_results}

Question: {question}
Answer:"""

                response = llm.invoke(answer_prompt)
                answer = response.content
            else:
                status.update(label="Generating answer...")
                response = llm.invoke(question)
                answer = response.content

            status.update(label="Complete", state="complete")

        elapsed = time.time() - start_time
        st.markdown(answer)
        st.markdown(f'<span class="time-pill">⌛ {elapsed:.2f}s</span>', unsafe_allow_html=True)

        st.session_state.total_queries += 1
        st.session_state.total_time = (
                (st.session_state.total_time * (st.session_state.total_queries - 1) + elapsed)
                / st.session_state.total_queries
        )

    st.session_state.messages.append({"role": "assistant", "content": answer})

# Footer
st.markdown("""
<div class="footer">
    Created by Musa Jabbarli
</div>
""", unsafe_allow_html=True)