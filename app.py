import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

SYSTEM_PROMPT = """You are a smart, friendly personal assistant for a Data Science student. You help with:

- **Job applications**: Writing CVs, cover letters, LinkedIn profiles, interview prep, and salary negotiation advice
- **Career advice**: Navigating the DS/ML job market, skill development, portfolio building, networking strategies
- **Coding help**: Python, SQL, pandas, scikit-learn, PyTorch, data wrangling, debugging, code reviews
- **Daily planning**: Task prioritisation, time management, study schedules, productivity techniques

Be concise but thorough. Use markdown formatting when helpful (code blocks, bullet points, headers).
When helping with code, always include working examples. When giving career advice, be specific and actionable.
Adapt your tone to be encouraging and practical — like a knowledgeable friend who happens to be a senior data scientist."""

st.set_page_config(
    page_title="Personal Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    .app-header {
        padding: 1rem 0 0.5rem 0;
        border-bottom: 1px solid #1e2530;
        margin-bottom: 1.5rem;
    }
    .app-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #00d4d4;
        letter-spacing: 0.5px;
    }
    .app-subtitle {
        font-size: 0.8rem;
        color: #6b7280;
        margin-top: 2px;
    }

    .message-row {
        display: flex;
        width: 100%;
        margin-bottom: 0.75rem;
    }
    .message-row.user { justify-content: flex-end; }
    .message-row.assistant { justify-content: flex-start; }

    .bubble {
        max-width: 75%;
        padding: 0.75rem 1rem;
        border-radius: 18px;
        font-size: 0.92rem;
        line-height: 1.55;
        word-wrap: break-word;
    }
    .bubble.user {
        background-color: #00d4d4;
        color: #0e1117;
        border-bottom-right-radius: 4px;
        font-weight: 500;
    }
    .bubble.assistant {
        background-color: #1a2030;
        color: #e0e0e0;
        border: 1px solid #1e2d3d;
        border-bottom-left-radius: 4px;
    }

    .role-label {
        font-size: 0.7rem;
        color: #6b7280;
        margin-bottom: 3px;
    }
    .role-label.user { text-align: right; }
    .role-label.assistant { text-align: left; }

    .stTextArea textarea {
        background-color: #1a2030 !important;
        border: 1px solid #1e2d3d !important;
        border-radius: 12px !important;
        color: #e0e0e0 !important;
        font-size: 0.92rem !important;
        resize: none !important;
    }
    .stTextArea textarea:focus {
        border-color: #00d4d4 !important;
        box-shadow: 0 0 0 1px #00d4d490 !important;
    }

    .stButton > button {
        background-color: #00d4d4 !important;
        color: #0e1117 !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: opacity 0.15s ease !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    .welcome-card {
        background: linear-gradient(135deg, #0d1f2d, #0e1117);
        border: 1px solid #1e2d3d;
        border-left: 3px solid #00d4d4;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
        color: #9ca3af;
        font-size: 0.88rem;
        line-height: 1.6;
    }
    .welcome-card strong { color: #00d4d4; }

    .bubble pre {
        background-color: #0a0f18 !important;
        border-radius: 8px;
        padding: 0.75rem;
        overflow-x: auto;
        font-size: 0.82rem;
    }
    .bubble code {
        background-color: #0a0f18 !important;
        padding: 1px 4px;
        border-radius: 4px;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


def get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not found. Add it to your .env file.")
        st.stop()
    return Groq(api_key=api_key)


def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []


def render_message(role: str, content: str):
    label = "You" if role == "user" else "Assistant"
    st.markdown(f"""
    <div class="role-label {role}">{label}</div>
    <div class="message-row {role}">
        <div class="bubble {role}">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def main():
    init_session()

    st.markdown("""
    <div class="app-header">
        <div class="app-title">🤖 Personal Assistant</div>
        <div class="app-subtitle">Powered by Llama 3 · Data Science Edition</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-card">
            Hi! I'm your personal assistant. I can help you with:<br>
            <strong>Job applications</strong> · <strong>Career advice</strong> ·
            <strong>Coding</strong> · <strong>Daily planning</strong><br><br>
            What's on your mind today?
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        render_message(msg["role"], msg["content"])

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_area(
            "Message",
            key="input_box",
            placeholder="Ask me anything — coding, career, planning…",
            height=80,
            label_visibility="collapsed",
        )
    with col2:
        send_clicked = st.button("Send", use_container_width=True)
        clear_clicked = st.button("Clear", use_container_width=True)

    if clear_clicked:
        st.session_state.messages = []
        st.rerun()

    if send_clicked and user_input.strip():
        user_text = user_input.strip()
        st.session_state.messages.append({"role": "user", "content": user_text})
        render_message("user", user_text)

        client = get_client()

        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        st.markdown('<div class="role-label assistant">Assistant</div>', unsafe_allow_html=True)
        response_placeholder = st.empty()

        with st.spinner("Thinking…"):
            accumulated = ""
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=api_messages,
                stream=True,
                max_tokens=2048,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                if delta:
                    accumulated += delta
                    response_placeholder.markdown(
                        f'<div class="message-row assistant"><div class="bubble assistant">{accumulated}▌</div></div>',
                        unsafe_allow_html=True,
                    )

        response_placeholder.markdown(
            f'<div class="message-row assistant"><div class="bubble assistant">{accumulated}</div></div>',
            unsafe_allow_html=True,
        )

        st.session_state.messages.append({"role": "assistant", "content": accumulated})
        st.rerun()


if __name__ == "__main__":
    main()
