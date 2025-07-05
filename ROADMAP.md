# 📍 BLIP Project Roadmap

This document outlines the planned direction of the BLIP platform. If you’d like to help move things forward, check the [CONTRIBUTING.md](./CONTRIBUTING.md) and feel free to open issues or PRs.

---

## ✅ Current Status

- [x] Upload and query local PDFs via API
- [x] Gemini + LangChain powered agent
- [x] Kenya MVP documents manually added

---

## 🛠 Near-Term Goals

### 🗂 1. Document Parsing & QA
- [ ] Add summarization for long documents
- [ ] Add basic citation in LLM answers
- [ ] Support additional formats (Word, HTML)

### 🌍 2. Expand Coverage
- [ ] Rwanda and Nigeria compliance docs
- [ ] Multi-language support (French/Swahili)
- [ ] Community-led country onboarding

---

## 🧱 Mid-Term Architecture

### 🔄 Scraper Integration (Coming Soon)
Manual uploads don’t scale — we plan to:
- [ ] Build a country-specific scraper system
- [ ] Fetch and update government regulations weekly
- [ ] Extract PDFs, notices, and permit pages automatically
- [ ] Store structured data (JSON/YAML) in `data/` folder

Contributors are welcome to help build these modules!

---

## 📊 UI + Dashboard

- [ ] Web frontend for document upload & chat
- [ ] View compliance summaries by country/sector
- [ ] Dashboard to track document freshness

---

## 📦 Packaging + Deployment

- [ ] Dockerized backend
- [ ] Hosted demo on Fly.io, Render, or HuggingFace Spaces
- [ ] CLI interface for querying local docs

---

## 🧠 Long-Term Vision

- A **Pan-African regulatory assistant**
- Open-source **permitting data graph** across countries
- GitHub-first knowledge hub for business compliance

---

## 🙌 Want to Help?

- Pick a feature or goal and open a PR
- Submit new docs, scrapers, or country ideas
- Suggest improvements via [Issues](https://github.com/mburu72/BLIP-LangChain/issues)

Let's simplify business compliance together.