# Contributing to BLIP

Thanks for your interest in contributing to **BLIP – Business Licensing Intelligence Platform**!

Whether you're a developer, legal researcher, data contributor, or just curious — we welcome your input. Together, we can make regulatory compliance accessible and open for everyone.

---

## What You Can Help With

### Developers
- Improve or extend the LangChain + Gemini pipeline
- Add new endpoints (e.g., document summarization, citation)
- Refactor or clean up backend logic
- Add Docker or deployment scripts
- Write unit tests

### Regulatory/Data Contributors
- Upload official business permit or tax PDFs to `compliance_docs/`
- Organize and name files clearly (e.g., `kenya_trading_license.pdf`)
- Optionally, summarize documents in Markdown under `docs/`
- Validate document sources (only public or licensed materials)

---

## Local Setup Instructions

```bash
# Clone the repo
git clone https://github.com/mburu72/BLIP-LangChain.git
cd BLIP-LangChain

# Set up environment
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload