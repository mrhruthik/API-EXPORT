# API EXPORT

## Export Buyer Intelligence & Outreach Automation Platform

API EXPORT is an export-sales automation platform designed to help businesses discover potential international buyers, manage buyer leads, validate contact information, automate outreach through Gmail, track follow-ups, monitor responses, and analyze the overall sales pipeline.

The system combines a FastAPI backend, SQLite database, web dashboard, buyer discovery through web search, lead validation, AI-based qualification support, and Gmail API integration into one workflow.

---

## Project Overview

Finding international buyers manually can require significant time spent researching companies, collecting contact information, cleaning lead data, sending emails, and tracking follow-ups.

API EXPORT centralizes these activities into a single workflow:

```text
Market Research
       ↓
Buyer Discovery
       ↓
Lead Collection
       ↓
Duplicate Detection
       ↓
Lead Validation
       ↓
AI Qualification
       ↓
Email Preparation
       ↓
Gmail Outreach
       ↓
Follow-up Tracking
       ↓
Response Tracking
       ↓
Analytics



## Features

- International buyer discovery
- Lead collection and management
- Duplicate detection
- Lead validation
- CSV/Excel lead import
- AI-based buyer qualification support
- Personalized email preparation
- Gmail API integration
- Safe email sending with duplicate-send protection
- Follow-up scheduling and tracking
- Buyer response status tracking
- Sales pipeline analytics
- Web-based dashboard
- REST API with Swagger documentation

---

## Technology Stack

### Backend
- Python 3.13
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

### Database
- SQLite

### Frontend
- HTML
- CSS
- JavaScript

### External Services
- Tavily Web Search API
- OpenAI API
- Gmail API

### Testing
- Pytest

---

## Project Structure

```text
API-EXPORT/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── web.py
│   ├── outreach.py
│   ├── gmail_service.py
│   └── ai_classifier.py
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
│
├── tests/
│   └── test_api.py
│
├── uploads/
├── export.db
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md