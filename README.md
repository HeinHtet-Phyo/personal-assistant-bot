# 🤖 Personal Assistant Chatbot

A personal assistant chatbot built for Data Science students. Powered by **Llama 3.3 70B** via Groq, with a clean dark-themed UI built in Streamlit.

## What it can do

- **Job applications** — CV writing, cover letters, interview prep
- **Career advice** — DS/ML job market, skills roadmap, portfolio tips
- **Coding help** — Python, SQL, pandas, scikit-learn, PyTorch, debugging
- **Daily planning** — study schedules, task prioritisation, productivity

## Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [Groq API](https://console.groq.com) | Fast AI inference |
| [Llama 3.3 70B](https://ai.meta.com/blog/meta-llama-3/) | Underlying LLM (Meta, open source) |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | API key management |

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/HeinHtet-Phyo/personal-assistant-bot.git
cd personal-assistant-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a free Groq API key
- Go to [console.groq.com](https://console.groq.com)
- Sign up for free (no credit card needed)
- Create an API key

### 4. Set up your `.env` file
```bash
cp .env.example .env
```
Open `.env` and add your key:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

## How it works

Every message you send is prepended with a **system prompt** that tells the AI to act as a Data Science student assistant. The full conversation history is sent with each request so the AI remembers context throughout the session.

```
System prompt (hidden) → "You are a DS student assistant..."
User message          → "Help me write a cover letter"
AI response           → streamed back word by word
```

To customise the assistant for a different domain, just edit the `SYSTEM_PROMPT` variable in `app.py`.

## Project Structure

```
personal-assistant-bot/
├── app.py            # Main app — UI + AI logic
├── requirements.txt  # Python dependencies
├── .env.example      # Template for environment variables
├── .gitignore        # Excludes .env from git
└── README.md         # This file
```
