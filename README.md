# BLIP - Business Licensing Intelligence Platform

**BLIP** is an open-source AI assistant that helps users understand and stay compliant with licensing, tax and regulatory requirements starting with Kenya.

It uses [LangChain](https://www.langchain.com/) and [Gemini](https://deepmind.google/discover/blog/google-gemini-ai/) to let users query uploaded documents and a growing knowledge base of business laws.

---

## 🚀 Features

- 🧠 AI-powered chat assistant (LangChain + Gemini)
- 📄 Upload and query compliance PDFs
- 🏛️ Local repository of official regulatory documents
- 🔎 RAG-based document retrieval pipeline
- 🌍 Built for expansion across countries and regions

---

## 🛠️ Tech Stack

| Layer        | Tech                         |
|--------------|------------------------------|
| LLM + RAG    | LangChain, Gemini Pro        |
| Backend      | FastAPI                      |
| Parsing      | PyMuPDF / LangChain loaders  |
| Frontend     | NextJS, TailwindCSS          |

---

## 📦 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/mburu72/BLIP-LangChain.git
cd BLIP-LangChain
````

### 2. Set Up Environment

Create a `.env` file:

```bash
cp .env
```

Then add your Gemini API key:

```
GEMINI_API_KEY=your_gemini_key_here
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the App

```bash
uvicorn main:app --reload
```

---

## 📂 Project Structure

```
BLIP-LangChain/
├── BLIP-Pydantic-AI(agent)/ # Agent with pydantic-ai(ignore it if you are not familiar with pydantic-ai or agents)   
├── config/                  # App settings and shared constants
├── docs_processing/         # PDF parsing, chunking, and embedding
├── llm_service/             # LangChain agent and Gemini logic
├── router/                  # FastAPI endpoints (chat, upload, etc.)
├── compliance_docs/         # Business/legal PDFs (core document base)
├── prompt.txt               # System prompt for LLM agent
├── requirements.txt         # Project dependencies
├── README.md                # This file
└── main.py                  # App entry point
```

---
## The live demo can be found [here](https://edwardmn.netlify.app/demo)


## 🗂️ Regulatory Documents

All official compliance PDFs are stored under:

```
compliance_docs/
```

> ✅ Contributors can add documents per country, region or sector.

---

## 🧑‍💻 Contributing

We welcome PRs for:

* Adding new regulatory docs
* Improving parsing or LLM accuracy
* Supporting more countries or sectors
* Fixing bugs or cleaning code

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full guidelines.

---

## 📍 Roadmap

* [x] Kenya MVP (PDF upload + chat)
* [ ] Add summarization and citations
* [ ] Add other countries
* [ ] Dockerized deployment
* [ ] Frontend interface

---

## 🛡️ License

Licensed under the [MIT License](LICENSE).

---

## 👤 Author

Built by [Edward Mburu](https://github.com/mburu72)

> “I built BLIP after struggling to understand what licenses I needed to launch a business in Kenya.”