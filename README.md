API EXPORT — AI-Powered Export Outreach Automation

API EXPORT is an international export buyer lead-generation and outreach system built with FastAPI, SQLAlchemy, SQLite, Tavily, Gmail API/Google Apps Script integration, and a browser dashboard.

Workflow

Buyer discovery → lead collection → cleaning/duplicate detection → validation → qualification → outreach preparation → Gmail sending → follow-up tracking → response tracking → analytics.

Main Features

Lead CRUD management

CSV/Excel lead import

Duplicate detection

Email-format validation

Bulk validation

Web buyer discovery using Tavily

Lead qualification workflow

Outreach message generation

Gmail email sending

Duplicate-send protection

Follow-up scheduling/tracking

Response status tracking

Outreach summary/analytics

Responsive web dashboard

Swagger/OpenAPI documentation

Project Structure

API-EXPORT/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── outreach.py
│   ├── gmail_service.py
│   ├── ai_classifier.py
│   └── web.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── tests/
├── uploads/
├── export.db
├── .env
├── .env.example
├── .gitignore
└── requirements.txt

Requirements

Python 3.13

Gmail account for email sending

Tavily API key for buyer discovery

OpenAI API key if live AI classification is enabled

Google Apps Script deployment if using the configured Apps Script integration

Installation

Create and activate a virtual environment:

python -m venv venv
.env\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Environment Variables

Create .env locally. Never commit it.

Example:

TAVILY_API_KEY=your_tavily_key
OPENAI_API_KEY=your_openai_key
APPS_SCRIPT_URL=your_apps_script_url
APPS_SCRIPT_TOKEN=your_apps_script_token

Use .env.example as the safe template.

Start the API

From the project root:

uvicorn app.main:app --reload

Swagger:

http://127.0.0.1:8000/docs

Start the Web Dashboard

The dashboard is exposed through app.web:

uvicorn app.web:app --reload

Open:

http://127.0.0.1:8000/dashboard/

The dashboard consumes the existing FastAPI backend and displays live lead/outreach information from SQLite.

Gmail

Gmail sending is authenticated separately and should be tested with a controlled recipient before production outreach. The application records outreach status and prevents a lead from being sent again when its status is already SENT.

Testing

Run:

pytest -q

The included tests cover basic API availability, lead retrieval, outreach summary availability, and Swagger availability.

AI Classification Limitation

The AI classifier implementation is included in the project. During development, live classification testing was limited by the configured OpenAI account returning an insufficient-quota response. The implementation should therefore be described as implemented but not fully live-tested with paid API quota.

Security

Never commit:

.env

OAuth credentials

Gmail tokens

API keys

deployment secrets

local database files containing private data

The repository should contain .env.example instead of real secrets.

Evidence for Evaluation

Recommended evidence:

Dashboard screenshot

Lead management screenshot

Buyer discovery screenshot

Validation/import screenshot

Outreach preparation screenshot

Successful Gmail send screenshot

Follow-up/response tracking screenshot

Analytics screenshot

Swagger API screenshot

GitHub repository link

Project Status

Core backend, database workflow, outreach workflow, Gmail integration, API documentation, and web dashboard are implemented. Remaining evaluation work should focus on automated test coverage, evidence organization, data cleanup, and deployment/submission requirements.