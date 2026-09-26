# 🌿 MindMate

A warm, always-positive AI wellness companion. Multi-agent RAG system built on
Groq-hosted LLMs, grounded in four therapeutic books (CBT, ACT, Motivational
Interviewing, DSM-5), plus live web search. Helps with everyday mental
discomfort, addictions, and fears — never diagnoses, always has a hard-coded
crisis safety layer in front of everything else.

**Built by: Engr. Mubashir Malik**

> ⚠️ MindMate is a supportive companion, not a licensed therapist. It does not
> replace professional care, diagnosis, or crisis services.

---

## How it works

```
User message
   → Safety Check (crisis detection, always runs first)
   → Router (classifies: mental_discomfort / addiction / fear / general_chat)
   → Specialist agent(s) retrieve from their book's Chroma collection
       + web search if the retrieval is weak
   → Positivity/Persona Rewrite Layer (validates feeling, cuts toxic
     positivity, keeps hope specific)
   → Response shown to user
```

| Agent | Grounded in | Handles |
|---|---|---|
| Mental Discomfort | CBT (Beck) + ACT (Hayes) | uncertainty, dissonance, boredom, rejection, regret, envy, guilt/shame, decision fatigue, FOMO, loneliness |
| Addiction | Motivational Interviewing (Miller & Rollnick) + CBT | alcohol, nicotine, opioids, stimulants, caffeine, gambling, phone/social media, gaming, porn/sex |
| Fear | ACT (Hayes) | death, public speaking, failure, rejection, heights, spiders, the dark, losing control, isolation, the unknown |

---

## 1. Setup

```bash
git clone <your-repo-url>
cd mindmate
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Add your API keys

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` and fill in:
- `GROQ_API_KEY` — get one free at https://console.groq.com
- `TAVILY_API_KEY` — optional; if omitted, web search automatically falls back
  to the free DuckDuckGo search (no key needed)

## 3. Add your source books and build the knowledge base

Place your 4 PDFs in `data/source_pdfs/` renamed exactly as:

```
data/source_pdfs/cbt.pdf     # Cognitive Behavior Therapy: Basics and Beyond — Judith Beck
data/source_pdfs/act.pdf     # Get Out of Your Mind and Into Your Life — Steven Hayes
data/source_pdfs/mi.pdf      # Motivational Interviewing — Miller & Rollnick
data/source_pdfs/dsm5.pdf    # DSM-5 — APA
```

Then run the one-time ingestion script (this builds the local Chroma vector
database — only needs to be re-run if you change the source books):

```bash
python rag/ingest.py
```

This will take a few minutes, especially for the larger PDFs (DSM-5 is big).

## 4. Run locally

```bash
streamlit run app.py
```

The app will be at `http://localhost:8501`.

---

## Deploying to Streamlit Community Cloud

1. Push this repo to GitHub. **Do not commit** `data/source_pdfs/*.pdf`,
   `.streamlit/secrets.toml`, or (unless you've checked the copyright
   implications) `data/chroma_db/` — all three are already in `.gitignore`.
2. If you want the deployed app to have a working knowledge base without
   committing the vector DB, either:
   - Run `rag/ingest.py` locally and manually upload `data/chroma_db/` to the
     deployed instance's persistent storage, or
   - Host the Chroma DB files somewhere private (e.g. a private cloud bucket)
     and adjust `rag/retriever.py`'s `DB_DIR` to download/mount it at startup.
3. Go to https://share.streamlit.io, connect your GitHub repo, and set the
   main file to `app.py`.
4. In the app's **Settings → Secrets**, paste the same keys from your local
   `secrets.toml`:
   ```toml
   GROQ_API_KEY = "..."
   TAVILY_API_KEY = "..."
   ```
5. Deploy.

---

## Project structure

```
mindmate/
├── app.py                      # Streamlit entrypoint
├── requirements.txt
├── .streamlit/
│   ├── config.toml             # theme
│   └── secrets.toml.example
├── agents/
│   ├── graph.py                 # top-level pipeline orchestration
│   ├── router.py
│   ├── safety_check.py
│   ├── base_agent.py            # shared RAG + Groq call logic
│   ├── discomfort_agent.py
│   ├── addiction_agent.py
│   ├── fear_agent.py
│   ├── general_agent.py
│   └── persona_rewrite.py
├── rag/
│   ├── ingest.py                 # one-time: PDFs -> Chroma collections
│   ├── retriever.py
│   └── web_search.py
├── ui/
│   ├── chat_tab.py
│   ├── mood_tab.py
│   ├── addiction_tab.py
│   └── fear_tab.py
├── utils/
│   ├── session_state.py
│   ├── crisis_resources.py
│   └── groq_client.py
└── data/
    ├── source_pdfs/              # your 4 books (gitignored)
    └── chroma_db/                # built by ingest.py (gitignored)
```

## A note on safety

The safety check in `agents/safety_check.py` runs on every single message
before any specialist agent sees it, using both a keyword filter and an LLM
classifier. If either flags crisis-level risk, the app immediately shows real
crisis resources and skips the rest of the pipeline. Please test this file
thoroughly with your own examples before showing this app to anyone in a
vulnerable moment — and please treat it as a supplement to real human and
professional support, never a replacement.
