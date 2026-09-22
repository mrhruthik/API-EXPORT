# API EXPORT

## Export Buyer Intelligence & Outreach Automation Platform

---

# 1. Project Abstract

API EXPORT is a web-based export-sales automation platform designed to streamline the process of discovering and managing potential international buyers.

The platform provides a centralized workflow for buyer discovery, lead collection, duplicate detection, contact validation, AI-assisted qualification, outreach preparation, Gmail-based communication, follow-up tracking, response monitoring, and sales pipeline analysis.

The application is developed using Python and FastAPI for the backend, SQLite for data storage, SQLAlchemy for database interaction, and HTML, CSS, and JavaScript for the web dashboard. External services such as the Tavily Web Search API, OpenAI API, and Gmail API are integrated to extend the functionality of the platform.

The main objective of API EXPORT is to reduce repetitive manual work involved in export buyer research and outreach while maintaining a structured and centralized lead management process.

---

# 2. Problem Statement

International export businesses often rely on manual methods to identify potential buyers, collect company and contact information, validate leads, communicate with prospects, and monitor follow-up activities. These processes can require significant time and may result in duplicated records, incomplete contact information, inconsistent lead management, and difficulty tracking the progress of buyer outreach.

Traditional workflows may involve searching multiple websites, maintaining lead information in separate spreadsheets, manually preparing emails, and tracking responses and follow-ups independently. As the number of potential buyers increases, managing these activities manually becomes more difficult and less organized.

There is therefore a need for a centralized platform that can organize the export buyer acquisition process into a structured workflow. The system should support buyer discovery, lead collection, duplicate detection, contact validation, buyer qualification, email preparation, Gmail-based outreach, follow-up tracking, response monitoring, and sales pipeline analysis.

API EXPORT addresses this problem by integrating these activities into a single web-based platform. The system provides a centralized database and dashboard through which export leads can be collected, managed, validated, contacted, and monitored throughout the outreach process.

---

# 3. Objectives

The main objective of API EXPORT is to develop a centralized export-sales automation platform that simplifies and organizes the process of discovering potential international buyers and managing the buyer outreach lifecycle.

The specific objectives of the project are:

1. **Buyer Discovery**

   To provide a structured mechanism for discovering potential international buyers, importers, distributors, wholesalers, and trading companies through web-based research.

2. **Lead Collection and Management**

   To collect and maintain important buyer information such as company name, contact details, country, industry, product category, website, email, phone number, and source.

3. **Duplicate Detection**

   To identify duplicate buyer records and reduce repeated entries in the lead database.

4. **Lead Validation**

   To validate available contact information and maintain a clear validation status for each lead.

5. **AI-Based Buyer Qualification**

   To provide AI-assisted qualification of leads by analyzing available company information and identifying whether a lead may be relevant as a potential buyer, importer, distributor, wholesaler, or trading company.

6. **Email Preparation**

   To automatically prepare structured and personalized outreach messages based on the information available for each lead.

7. **Gmail Integration**

   To integrate Gmail API functionality for controlled business email outreach and maintain the status of sent communications.

8. **Duplicate-Send Prevention**

   To prevent the same lead from being unintentionally contacted multiple times through the platform.

9. **Follow-up Management**

   To schedule and track follow-up activities for leads that have been contacted.

10. **Response Tracking**

    To maintain buyer response statuses and provide visibility into buyer engagement.

11. **Sales Pipeline Monitoring**

    To provide a centralized dashboard for monitoring lead status, outreach activity, follow-ups, and responses.

12. **Analytics and Reporting**

    To provide basic analytics that help users understand the current state of the export-sales pipeline.

13. **REST API Development**

    To provide backend REST APIs using FastAPI for managing leads and supporting the different operations of the platform.

14. **Testing and Reliability**

    To test the core backend functionality using automated tests and ensure that important API operations work as expected.

---

# 4. System Architecture

API EXPORT follows a modular web application architecture in which the frontend dashboard communicates with a FastAPI backend. The backend manages lead operations, buyer discovery, validation, outreach preparation, Gmail communication, follow-up tracking, and analytics. The application also integrates external services for web search, AI-based qualification, and email communication.

## 4.1 High-Level Architecture

The overall architecture of API EXPORT is:

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │  Web Dashboard  │
                  │   HTML/CSS/JS   │
                  └────────┬────────┘
                           │
                      HTTP / JSON
                           │
                           ▼
                  ┌─────────────────┐
                  │     FastAPI     │
                  │     Backend     │
                  └────────┬────────┘
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
   Lead Management   Buyer Discovery    Outreach System
          │                │                 │
          │                ▼                 ▼
          │          Tavily Web Search    Gmail API
          │
          ▼
   ┌─────────────────┐
   │ SQLite Database │
   │    export.db    │
   └────────┬────────┘
            │
            ├── Leads
            ├── Validation
            ├── Outreach
            ├── Follow-ups
            └── Responses

                           │
                           ▼
                    Analytics Dashboard
4.2 Frontend Layer

The frontend provides the user interface for interacting with the platform.

The frontend is implemented using:

HTML
CSS
JavaScript

The dashboard provides different sections for managing the export-sales workflow:

Dashboard
    │
    ├── Leads
    │
    ├── Buyer Discovery
    │
    ├── Outreach
    │
    ├── Follow-ups
    │
    └── Analytics

JavaScript communicates with the FastAPI backend using HTTP requests and processes the returned JSON data to update the dashboard.

4.3 Backend Layer

The backend is developed using Python and FastAPI.

The backend provides REST API endpoints for:

Creating leads
Retrieving leads
Updating leads
Deleting leads
Importing leads
Validating leads
Discovering potential buyers
Preparing outreach
Sending outreach
Tracking follow-ups
Monitoring response status
Providing analytics data

The main backend components are organized into separate Python modules.

app/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── web.py
├── outreach.py
├── gmail_service.py
└── ai_classifier.py

This modular structure separates different responsibilities of the application.

4.4 Database Layer

API EXPORT uses SQLite as the database and SQLAlchemy as the ORM.

The database is stored locally in:

export.db

The primary entity is the Lead table.

The database stores:

Company Information
        │
        ├── Company Name
        ├── Contact Name
        ├── Designation
        ├── Country
        └── City

Business Information
        │
        ├── Industry
        ├── Product Category
        ├── Website
        ├── Email
        ├── Phone
        └── Source

Lead Management
        │
        ├── Lead Status
        └── Validation Status

Outreach Management
        │
        ├── Outreach Status
        ├── Outreach Subject
        ├── Outreach Body
        ├── Sent Time
        ├── Follow-up Time
        └── Response Status
4.5 Buyer Discovery Integration

The Buyer Discovery module uses the Tavily Web Search API to perform web-based research.

The general process is:

Product Category
       │
       ▼
Target Market
       │
       ▼
Tavily Web Search
       │
       ▼
Search Results
       │
       ▼
Filtering
       │
       ▼
Duplicate Detection
       │
       ▼
Lead Database

The discovery module is intended to identify potential companies that may be relevant to the selected export product and market.

4.6 AI Qualification Integration

The project includes an AI qualification module using the OpenAI API.

The intended workflow is:

Lead Information
       │
       ▼
AI Classification
       │
       ▼
Buyer / Not Buyer
       │
       ▼
Buyer Type
       │
       ▼
Relevance
       │
       ▼
Lead Qualification

The AI qualification module considers available company information such as industry, product category, country, website, and company name.

The AI component is designed as qualification support and does not replace human verification of potential buyers.

4.7 Gmail Integration

The Outreach module integrates with the Gmail API to send business emails.

The workflow is:

Validated Lead
       │
       ▼
Prepare Email
       │
       ▼
Subject + Email Body
       │
       ▼
Gmail Authentication
       │
       ▼
Gmail API
       │
       ▼
Email Sent
       │
       ▼
Update Lead Status

The system maintains outreach information in the database so that the application can determine whether a lead has already been contacted.

This provides duplicate-send protection.

4.8 Follow-up and Response Tracking

After outreach, the system maintains follow-up information for the lead.

Email Sent
    │
    ▼
Follow-up Date
    │
    ▼
Follow-up Monitoring
    │
    ▼
Response Status

This allows the platform to track the progress of buyer communication after the initial email.

4.9 Analytics Layer

The Analytics section retrieves information from the lead database and presents the current state of the export-sales pipeline.

The dashboard can display metrics such as:

Total Leads
     │
     ├── Not Contacted
     │
     ├── Ready to Send
     │
     ├── Emails Sent
     │
     ├── Follow-ups
     │
     └── Responses

This provides a centralized overview of the current outreach pipeline.

4.10 Complete Application Flow

The complete API EXPORT workflow can be represented as:

                    START
                      │
                      ▼
                Market Research
                      │
                      ▼
                Buyer Discovery
                      │
                      ▼
                Lead Collection
                      │
                      ▼
               Duplicate Detection
                      │
                      ▼
                 Lead Validation
                      │
                      ▼
                AI Qualification
                      │
                      ▼
                Email Preparation
                      │
                      ▼
                 Gmail Outreach
                      │
                      ▼
              Outreach Status Update
                      │
                      ▼
                Follow-up Tracking
                      │
                      ▼
                Response Tracking
                      │
                      ▼
                    Analytics
                      │
                      ▼
                     END
4.11 Architectural Benefits

The architecture provides several benefits:

Separation of frontend and backend responsibilities.
Modular Python backend structure.
Centralized lead and outreach data management.
Integration with external services through APIs.
REST-based communication between frontend and backend.
Easier testing and maintenance.
Ability to replace or extend individual modules independently.
Foundation for future cloud deployment and database scaling.
5. System Modules

API EXPORT is divided into multiple functional modules. Each module is responsible for a specific part of the export buyer discovery and outreach workflow.

5.1 Lead Management Module

The Lead Management module is responsible for storing and managing potential international buyer information.

The module manages information such as:

Company name
Contact name
Designation
Country
City
Industry
Product category
Website
Email
Phone
Source
Lead status
Validation status
Outreach status
Notes

Users can create, view, update, archive, and delete lead records through the application.

5.2 Buyer Discovery Module

The Buyer Discovery module helps identify potential international buyers based on user-provided search criteria.

The user can provide:

Product category
Target country
Industry
Keywords

The system uses web search to collect potential company results and processes the results before they are imported into the lead database.

The general workflow is:

Search Criteria
      ↓
Web Search
      ↓
Potential Results
      ↓
Filtering
      ↓
Duplicate Detection
      ↓
Discovery Results
      ↓
Lead Database
5.3 Lead Import Module

The Lead Import module allows users to add existing buyer information to the platform using structured files such as CSV files and Excel files.

The import process helps transfer external lead lists into the centralized database.

The system processes the imported records and checks for duplicate entries before storing them.

5.4 Duplicate Detection Module

The Duplicate Detection module helps prevent repeated lead records from being unnecessarily stored in the database.

Duplicate detection is used during lead discovery and lead import operations.

The general process is:

New Lead
   ↓
Compare with Existing Records
   ↓
Duplicate?
 ┌───────┴───────┐
 │               │
YES              NO
 │               │
Skip          Store Lead

This helps maintain a cleaner lead database.

5.5 Lead Validation Module

The Lead Validation module checks the available lead information and maintains a validation status.

The platform uses statuses such as:

PENDING
VALID
INVALID

Validation can be performed for individual leads or multiple leads.

This helps identify records that are ready for further processing.

5.6 AI Qualification Module

The AI Qualification module is designed to provide AI-assisted analysis of potential buyer companies.

The module can analyze information such as:

Company name
Country
Industry
Product category
Website

The intended classification includes:

BUYER
NOT_BUYER

Potential buyer types include:

IMPORTER
DISTRIBUTOR
WHOLESALER
TRADING_COMPANY
BUYER
UNKNOWN

The module is intended to support lead qualification and does not replace human verification.

5.7 Outreach Preparation Module

The Outreach Preparation module generates an email subject and message body using available lead information.

The generated outreach can include information such as:

Company name
Contact name
Product category
Country
Industry
Business opportunity
Product information
Pricing information
Minimum order quantities
Export and shipping information

The prepared message is stored with the lead and can be marked as ready for sending.

5.8 Gmail Outreach Module

The Gmail Outreach module integrates the platform with Gmail through the Gmail API.

The general workflow is:

Qualified / Valid Lead
        ↓
Prepare Email
        ↓
Review Email
        ↓
Gmail Authentication
        ↓
Send Email
        ↓
Update Outreach Status

The platform records outreach information such as:

Outreach status
Email subject
Email body
Sent time
Follow-up date
Response status

The system also includes protection against sending the same lead's outreach email twice.

5.9 Follow-up Module

The Follow-up module manages follow-up information for leads that have already been contacted.

The platform stores a follow-up date and provides an endpoint for identifying follow-ups that are due.

The workflow is:

Email Sent
    ↓
Follow-up Date
    ↓
Follow-up Monitoring
    ↓
Follow-up Due
5.10 Response Tracking Module

The Response Tracking module stores the response status associated with an outreach record.

For example:

NO_RESPONSE

The response-tracking functionality provides a foundation for monitoring buyer engagement.

5.11 Analytics Module

The Analytics module provides an overview of the current export-sales pipeline.

The dashboard can display:

Total leads
Not contacted
Ready to send
Emails sent
Follow-ups
Responses

The analytics information is retrieved from the backend and displayed through the web dashboard.

5.12 Web Dashboard Module

The Web Dashboard provides the main user interface for interacting with API EXPORT.

The dashboard contains:

Dashboard
    ↓
Leads
    ↓
Buyer Discovery
    ↓
Outreach
    ↓
Follow-ups
    ↓
Analytics

The dashboard communicates with the FastAPI backend using HTTP requests and displays the returned data to the user.

5.13 API Documentation Module

FastAPI provides interactive API documentation through Swagger UI.

The documentation allows developers to:

View available API endpoints
View request parameters
View response structures
Test API endpoints

The documentation is available locally at:

http://127.0.0.1:8000/docs
5.14 Testing Module

The project includes automated backend testing using Pytest.

The test suite is executed using:

python -m pytest -q

The current verified test result is:

4 passed
6. Technology Stack

API EXPORT is developed using a combination of backend, frontend, database, API integration, automation, and testing technologies. The technology stack was selected to support modular development, REST API communication, data management, buyer discovery, email outreach, and future scalability.

6.1 Programming Language
Python 3.13

Python is the primary programming language used for backend development.

It is used for:

Developing the FastAPI backend
Implementing lead management operations
Processing CSV and Excel files
Implementing buyer discovery logic
Lead validation and duplicate detection
AI-based lead qualification
Email outreach processing
Follow-up management
Database interaction
Automated testing
6.2 Backend Framework
FastAPI

FastAPI is used to develop the RESTful backend of the application.

It provides API endpoints for:

Lead creation and management
Lead import
Lead validation
Buyer discovery
Outreach preparation
Gmail outreach
Follow-up management
Response tracking
Analytics

FastAPI also provides automatic API documentation through Swagger UI.

6.3 ASGI Server
Uvicorn

Uvicorn is used as the ASGI server for running the FastAPI application.

It provides the development server required to run API EXPORT locally and handle HTTP requests from the web dashboard and API clients.

6.4 Database
SQLite

SQLite is used as the database for API EXPORT.

The database stores information related to:

International buyer leads
Company and contact information
Lead status
Validation status
Outreach status
Email subject and body
Sending timestamps
Follow-up information
Response status
Notes

The database is stored locally in the export.db file during development.

6.5 Database ORM
SQLAlchemy

SQLAlchemy is used as the Object-Relational Mapping (ORM) framework.

It provides a structured way to:

Define database models
Create and query records
Update lead information
Delete and archive leads
Manage database sessions
Interact with the SQLite database

The main database model used by the application is the Lead model.

6.6 Data Validation
Pydantic

Pydantic is used for request and response data validation.

It helps ensure that API requests contain valid and correctly structured data before the information is processed by the backend.

Pydantic schemas are used for operations such as:

Creating leads
Updating leads
Returning lead information
Validating API data
6.7 Frontend Technologies
HTML5

HTML is used to create the structure of the web dashboard and user interface.

It defines elements such as:

Navigation
Forms
Tables
Dashboard sections
Buttons
Lead management interfaces
Analytics sections
CSS3

CSS is used for styling the dashboard.

It controls:

Layout
Colors
Typography
Tables
Cards
Forms
Buttons
Responsive interface elements
JavaScript

JavaScript is used to provide dynamic functionality in the dashboard.

It communicates with the FastAPI backend using HTTP requests and updates the user interface based on API responses.

JavaScript is used for operations such as:

Loading leads
Adding and updating leads
Importing data
Running discovery
Preparing outreach
Sending emails
Displaying analytics
Updating dashboard information
6.8 Buyer Discovery API
Tavily Web Search API

Tavily is integrated into API EXPORT to support web-based buyer discovery.

The service is used to search the web for potential international buyers based on search criteria such as:

Product category
Industry
Country
Buyer-related keywords

The search results are processed by the backend and can be converted into lead records.

6.9 AI Integration
OpenAI API

The OpenAI API is integrated into the project to support AI-based lead qualification.

The AI classification module analyzes lead information and helps classify potential leads into categories such as:

Buyer
Not Buyer

It can also identify buyer types based on the available lead information.

The AI functionality is implemented as a separate module so that it can be used independently from the main lead management system.

6.10 Email Communication
Gmail API

The Gmail API is integrated into API EXPORT for email outreach.

It allows the application to:

Connect to a Gmail account
Send outreach emails
Track sent email information
Support follow-up communication

The Gmail integration uses Google's OAuth authentication mechanism.

6.11 CSV and Excel Processing
Pandas

Pandas is used for processing structured lead data and supporting file-based lead imports.

It helps process tabular data before it is inserted into the database.

OpenPyXL

OpenPyXL is used to support Excel workbook processing.

Together, Pandas and OpenPyXL allow API EXPORT to work with CSV and Excel-based lead data.

6.12 Testing
Pytest

Pytest is used for automated testing of the backend application.

The project includes tests for important API functionality such as:

Creating leads
Retrieving leads
Updating lead information
Validating API behavior

The current automated test suite successfully executes with all implemented tests passing.

6.13 Development Environment
Visual Studio Code

Visual Studio Code is used as the primary development environment.

It is used for:

Writing Python code
Developing frontend files
Managing project files
Running the FastAPI server
Running automated tests
Managing the Git repository
Python Virtual Environment

A Python virtual environment is used to isolate the project's dependencies from the system-wide Python installation.

This helps maintain a consistent development environment for API EXPORT.

6.14 Version Control
Git

Git is used for source code version control.

It is used to:

Track project changes
Create commits
Manage development history
Maintain project versions
GitHub

GitHub is used as the remote repository for the project.

The source code is maintained in the project's GitHub repository, allowing version control and remote backup of the application source code.

6.15 Technology Stack Summary
Category	Technology	Purpose
Programming Language	Python 3.13	Backend development and application logic
Backend Framework	FastAPI	REST API development
ASGI Server	Uvicorn	Running the FastAPI application
Database	SQLite	Storing application data
ORM	SQLAlchemy	Database interaction
Data Validation	Pydantic	API request and response validation
Frontend	HTML5	Web interface structure
Styling	CSS3	User interface styling
Client-side Logic	JavaScript	Dashboard interaction and API communication
Web Search	Tavily API	International buyer discovery
AI	OpenAI API	AI-based lead qualification
Email	Gmail API	Buyer outreach and email communication
Data Processing	Pandas	Tabular data processing
Excel Processing	OpenPyXL	Excel file handling
Testing	Pytest	Automated backend testing
IDE	Visual Studio Code	Development environment
Version Control	Git	Source code management
Repository	GitHub	Remote source code repository
7. Database Design

API EXPORT uses SQLite as its database and SQLAlchemy as the ORM layer. The database stores international buyer lead information along with validation, outreach, follow-up, and response-tracking information.

The database file used during development is export.db.

7.1 Database Structure

The primary database table in the current implementation is:

leads

The leads table stores the complete lifecycle information of an export buyer lead, from initial discovery or import through validation, outreach, follow-up, and response tracking.

7.2 Leads Table

The leads table contains the following fields:

Field	Data Type	Description
id	Integer	Unique identifier for each lead
company_name	String	Name of the buyer company
contact_name	String	Name of the contact person
designation	String	Designation or job role of the contact
country	String	Country of the buyer
city	String	City of the buyer
industry	String	Industry associated with the buyer
product_category	String	Product category relevant to the lead
website	String	Website of the company
email	String	Email address of the lead
phone	String	Contact phone number
source	String	Source from which the lead was obtained
lead_status	String	Current qualification or lifecycle status of the lead
validation_status	String	Status of email/contact validation
outreach_status	String	Current email outreach status
outreach_subject	String	Generated outreach email subject
outreach_body	Text	Generated outreach email content
sent_at	DateTime	Date and time when an outreach email was sent
follow_up_at	DateTime	Scheduled date and time for follow-up
response_status	String	Status of the buyer response
notes	Text	Additional notes related to the lead
7.3 Primary Key

The id field is the primary key of the leads table.

It uniquely identifies every lead stored in the database.

The primary key allows the application to:

Retrieve an individual lead
Update a specific lead
Delete a lead
Archive a lead
Track outreach activity for a particular lead
Associate actions with the correct lead record
7.4 Lead Information

The database stores basic company and contact information including:

Company name
Contact person
Designation
Country
City
Industry
Product category
Website
Email
Phone number

This information forms the basic buyer profile used throughout the application.

7.5 Lead Status and Validation

The database maintains separate status fields for managing the lead pipeline.

Lead Status

The lead_status field represents the current state of the lead in the application.

Validation Status

The validation_status field records whether the available contact information has been validated.

This separation allows the system to distinguish between the business qualification of a lead and the validation of its contact information.

7.6 Outreach Data

The database also stores information related to buyer outreach.

The following fields are used:

outreach_status
outreach_subject
outreach_body
sent_at

This allows the system to prepare and send personalized outreach emails while maintaining a record of the communication status.

7.7 Follow-up and Response Tracking

API EXPORT stores follow-up and response information directly in the lead record.

The following fields support this functionality:

follow_up_at
response_status

The follow_up_at field stores the scheduled follow-up time, while response_status records the current response state of the lead.

This allows the application to identify leads requiring follow-up and track communication progress.

7.8 Lead Source Tracking

The source field records where a lead originated.

Possible sources can include:

Buyer discovery
CSV import
Excel import
Other lead sources supported by the application

Source tracking helps identify how lead records entered the system.

7.9 Database Operations

SQLAlchemy is used to perform database operations through the FastAPI backend.

The application supports operations such as:

Create lead
Retrieve leads
Retrieve an individual lead
Update lead
Validate lead
Archive lead
Delete lead
Import leads
Update outreach information
Store email sending information
Schedule follow-ups
Track response status
7.10 Database Workflow

The database participates in the complete lead lifecycle:

Buyer Discovery / File Import
            │
            ▼
       Lead Created
            │
            ▼
     Duplicate Detection
            │
            ▼
       Lead Validation
            │
            ▼
      Lead Qualification
            │
            ▼
    Outreach Preparation
            │
            ▼
       Gmail Outreach
            │
            ▼
      Follow-up Tracking
            │
            ▼
     Response Tracking
            │
            ▼
         Analytics
7.11 Database Relationships and Design Characteristics

The current implementation uses a centralized leads table rather than maintaining separate relational tables for each stage of the workflow.

Lead information, validation information, outreach information, follow-up information, and response status are associated with the same lead record.

This design keeps the local development database simple and allows the backend to access the complete lead lifecycle using the lead ID.

The database design is therefore suitable for the current project scope and prototype/internship environment.

7.12 Data Lifecycle

A lead can enter the system through buyer discovery or file import.

The lead then progresses through different processing stages:

Discovery / Import
       ↓
Lead Record
       ↓
Duplicate Check
       ↓
Validation
       ↓
Qualification
       ↓
Outreach Preparation
       ↓
Email Outreach
       ↓
Follow-up
       ↓
Response Tracking

This lifecycle provides a structured method for managing potential buyers from initial collection through communication.

7.13 Database Design Benefits

The database design provides:

Centralized lead storage
Structured lead information
Simple database maintenance
Easy access through SQLAlchemy
Persistent outreach information
Follow-up tracking
Response status storage
Support for dashboard analytics
A foundation for future database migration and scaling
8. API Documentation

API EXPORT provides a RESTful API through the FastAPI backend. The API acts as the main communication layer between the web dashboard, database, and external services.

The API provides functionality for lead management, lead import, validation, buyer discovery, AI qualification, outreach preparation, Gmail communication, follow-up tracking, response tracking, and analytics.

FastAPI also provides automatic interactive API documentation through Swagger UI.

8.1 API Base URL

During local development, the API EXPORT backend runs using Uvicorn at:

http://127.0.0.1:8000

The interactive Swagger UI documentation is available at:

http://127.0.0.1:8000/docs

Swagger UI allows developers to view and test the available API endpoints directly from a web browser.

8.2 Lead Management APIs

Lead management is the core functionality of API EXPORT. These APIs allow the application to create, retrieve, update, archive, and delete buyer lead records.

Create Lead
POST /leads

Creates a new buyer lead in the database.

The API accepts information such as:

Company name
Contact name
Designation
Country
City
Industry
Product category
Website
Email
Phone number
Lead source

The backend processes the request and stores the lead in the SQLite database.

Get Leads
GET /leads

Retrieves the available lead records from the database.

This endpoint is used by the dashboard to display the lead list and provide the user with access to stored buyer information.

Get Individual Lead
GET /leads/{lead_id}

Retrieves information about a specific lead using its unique database ID.

The endpoint is useful when detailed information about a particular buyer is required.

Update Lead
PUT /leads/{lead_id}

Updates information associated with an existing lead.

The endpoint can be used to modify lead information such as contact details, company information, status, or notes.

Archive Lead
PATCH /leads/{lead_id}/archive

Archives a selected lead.

Archiving allows the system to remove a lead from the active workflow without permanently deleting its stored information.

Delete Lead
DELETE /leads/{lead_id}

Permanently deletes a selected lead from the database.

The lead ID is used to identify the record that should be deleted.

8.3 Lead Import API
Import Leads
POST /leads/import

The lead import API allows users to add existing buyer information to API EXPORT from supported structured files.

The system processes imported lead information before storing the records in the database.

The import functionality helps users transfer existing buyer lists into the centralized lead management system.

The imported data can subsequently pass through:

Import
   ↓
Duplicate Detection
   ↓
Validation
   ↓
Qualification
   ↓
Outreach

This allows imported leads to follow the same workflow as leads discovered through the system.

8.4 Lead Validation APIs

Lead validation helps determine whether the available contact information for a lead is usable.

Validate Individual Lead
PATCH /leads/{lead_id}/validate

Validates the available contact information for a specific lead.

The endpoint updates the lead's validation_status based on the validation process.

Validate All Leads
POST /leads/validate-all

Runs the validation process for the available leads.

This endpoint allows multiple leads to be processed without requiring the user to manually validate each lead individually.

The validation functionality helps improve the quality of the lead database before outreach is performed.

8.5 Lead Source API
Get Lead Sources
GET /leads/sources

Retrieves the lead sources recorded in the system.

The source field allows API EXPORT to maintain information about where a lead originated.

Examples of sources may include:

Buyer discovery
CSV import
Excel import
Other configured lead sources

Source information can be used for lead management and analysis.

8.6 Buyer Discovery APIs

The Buyer Discovery module is responsible for finding potential international buyers using web search functionality.

The discovery process can use criteria such as:

Product category
Industry
Target country
Buyer-related keywords

The backend communicates with the configured web-search service and processes the returned information.

The discovered results can then be converted into lead records and added to the lead management workflow.

The general discovery workflow is:

Search Criteria
      ↓
Web Search
      ↓
Search Results
      ↓
Lead Extraction
      ↓
Duplicate Detection
      ↓
Lead Database
8.7 AI Qualification Module

API EXPORT includes an AI qualification module that supports automated classification of potential buyer leads.

The AI module uses the configured OpenAI API integration to analyze available lead information.

The classification process can identify whether a lead appears to be:

Buyer
Not Buyer

It can also identify buyer types based on the information available for the lead.

The general workflow is:

Lead Information
       ↓
AI Classification
       ↓
Buyer / Not Buyer
       ↓
Buyer Type
       ↓
Lead Qualification

The AI qualification functionality is implemented as a separate backend module so that it remains independent from the core lead management operations.

8.8 Outreach Preparation APIs

The Outreach Preparation module generates an email that can be used to contact a selected buyer.

Prepare Outreach
POST /outreach/{lead_id}/prepare

Generates an outreach email for a selected lead.

The generated information includes:

Email subject
Email body
Outreach status
Follow-up information

The prepared email is stored with the corresponding lead and can be reviewed before sending.

The preparation workflow is:

Qualified Lead
      ↓
Outreach Preparation
      ↓
Email Subject
      ↓
Email Body
      ↓
READY_TO_SEND

The system also helps prevent unnecessary duplicate outreach by maintaining the outreach status of each lead.

8.9 Gmail Outreach APIs

The Gmail Outreach module is responsible for sending prepared emails to buyers.

Send Outreach
POST /outreach/{lead_id}/send

Sends the prepared outreach email for the selected lead through the Gmail API.

After a successful send operation, the system records relevant information such as:

Outreach status
Sending time
Email subject
Email body
Follow-up information

The general communication flow is:

Prepared Email
      ↓
Gmail API
      ↓
Buyer Email Address
      ↓
Email Sent
      ↓
Database Updated
Get Outreach Information
GET /outreach/{lead_id}

Retrieves the outreach information associated with a specific lead.

The endpoint can provide information related to the current outreach state and prepared email content.

Outreach Summary
GET /outreach/summary

Returns summary information about the outreach pipeline.

The summary is used by the dashboard to display outreach-related information such as:

Leads ready for outreach
Leads contacted
Sent outreach
Response information
8.10 Follow-up APIs

API EXPORT provides functionality for managing follow-up communication with buyers.

Get Due Follow-ups
GET /follow-ups/due

Retrieves leads for which a follow-up is currently due.

This allows the system to identify leads that require additional communication after the initial outreach.

Send Follow-up
POST /follow-ups/{lead_id}/send

Sends a follow-up email for the selected lead through the Gmail integration.

After the follow-up operation, the relevant lead information is updated in the database.

The follow-up workflow is:

Initial Outreach
       ↓
Follow-up Scheduled
       ↓
Follow-up Becomes Due
       ↓
Due Follow-up Retrieved
       ↓
Follow-up Email Sent
       ↓
Lead Information Updated
8.11 Response Tracking Module

API EXPORT maintains response information for leads that have been contacted.

The response state is stored using the response_status field associated with the lead.

The response tracking functionality allows the system to distinguish between leads that have not responded and leads that have progressed through the communication process.

The general workflow is:

Email Sent
    ↓
Response Status
    ↓
No Response / Response
    ↓
Lead Pipeline Updated

Response information can also be reflected in the analytics dashboard to provide an overview of communication activity.

8.12 Analytics and Dashboard Data

API EXPORT provides analytics information for monitoring the lead and outreach pipeline.

The analytics functionality uses information stored in the database to calculate and display useful statistics.

Examples include:

Total number of leads
Lead status distribution
Validation status
Outreach status
Number of contacted leads
Number of sent emails
Response information
Follow-up information

The analytics workflow is:

SQLite Database
       ↓
Lead and Outreach Data
       ↓
Backend Processing
       ↓
Analytics Information
       ↓
Web Dashboard

The analytics information allows users to monitor the overall progress of the export buyer acquisition workflow.

8.13 Swagger UI and API Testing

FastAPI automatically generates interactive API documentation through Swagger UI.

The Swagger interface is available at:

http://127.0.0.1:8000/docs

Swagger UI provides an interactive interface where developers can:

View available API endpoints
Inspect HTTP methods
View request parameters
View request and response schemas
Send test requests
Inspect API responses
Test backend functionality
Debug API operations

The REST API architecture provides the following benefits:

Clear separation between frontend and backend
Modular backend development
Reusable API functionality
Structured HTTP communication
Easier testing and debugging
Integration with external services
Support for future frontend or client applications

Overall, the FastAPI layer acts as the central communication interface between the API EXPORT dashboard, database, internal application modules, and external services.

9. Application Workflow

API EXPORT follows a structured workflow that manages the complete process from identifying potential international buyers to monitoring outreach activity.

The application workflow is divided into multiple stages.

9.1 Market Research

The process begins with identifying the target export product and market.

The user can define:

Product category
Target country
Industry
Buyer-related keywords

These parameters are used to identify potential buyer companies.

9.2 Buyer Discovery

The Buyer Discovery module uses web search functionality to identify potential companies.

The general process is:

Product / Market Criteria
          ↓
      Web Search
          ↓
    Search Results
          ↓
Potential Buyer Companies

The results are processed before being added to the lead database.

9.3 Lead Collection

Relevant company information is collected and converted into structured lead records.

Typical information includes:

Company name
Contact name
Designation
Country
City
Industry
Product category
Website
Email
Phone
Source

Leads can also be imported from structured files.

9.4 Duplicate Detection

Before storing new leads, the system checks available information against existing lead records.

New Lead
   ↓
Existing Lead Comparison
   ↓
Duplicate?
 ┌───────┴───────┐
 │               │
YES              NO
 │               │
Skip          Store

This helps reduce repeated records.

9.5 Lead Validation

The next stage is validation of available contact information.

The system maintains validation statuses such as:

PENDING
VALID
INVALID

Validation can be performed individually or for multiple leads.

9.6 AI Qualification

Where AI qualification is used, available company information is passed to the AI classification module.

The system can classify leads as:

BUYER
NOT_BUYER

Potential buyer categories can also be identified.

AI qualification is intended as decision support and does not replace human verification.

9.7 Outreach Preparation

For suitable leads, the system prepares an outreach message.

The outreach preparation process uses available lead information to generate:

Email subject
Email body

The prepared message is stored with the lead.

9.8 Gmail Outreach

The prepared email can be sent through the Gmail API.

Prepared Outreach
       ↓
Gmail Authentication
       ↓
Gmail API
       ↓
Email Sent
       ↓
Database Updated

The system records the communication status after sending.

9.9 Duplicate-Send Prevention

The outreach system maintains an outreach status for each lead.

Before sending an email, the application checks the existing outreach state.

This helps prevent a previously contacted lead from unintentionally receiving the same initial outreach again.

9.10 Follow-up Management

After an initial email is sent, a follow-up date can be stored for the lead.

The follow-up system identifies leads for which follow-up activity is due.

Email Sent
    ↓
Follow-up Scheduled
    ↓
Follow-up Due
    ↓
Follow-up Email
9.11 Response Tracking

The system maintains a response status for contacted leads.

This provides a basic mechanism for monitoring whether a lead has progressed beyond the initial outreach stage.

9.12 Analytics

Information stored in the database is used by the analytics dashboard.

The dashboard can provide information such as:

Total leads
Leads not contacted
Leads ready to send
Emails sent
Follow-ups
Responses
9.13 Complete Workflow

The complete workflow is:

                    START
                      │
                      ▼
               Market Research
                      │
                      ▼
                Buyer Discovery
                      │
                      ▼
                Lead Collection
                      │
                      ▼
              Duplicate Detection
                      │
                      ▼
                 Lead Validation
                      │
                      ▼
                AI Qualification
                      │
                      ▼
                Outreach Preparation
                      │
                      ▼
                 Gmail Outreach
                      │
                      ▼
              Outreach Status Update
                      │
                      ▼
                Follow-up Tracking
                      │
                      ▼
                Response Tracking
                      │
                      ▼
                    Analytics
                      │
                      ▼
                     END
9.14 User Interaction Workflow

The web dashboard provides a centralized interface through which the user can operate the application.

The typical user interaction is:

Open Dashboard
      ↓
View Lead Pipeline
      ↓
Discover / Import Leads
      ↓
Review Leads
      ↓
Validate Leads
      ↓
Prepare Outreach
      ↓
Send Email
      ↓
Monitor Follow-ups
      ↓
Review Analytics
10. Testing

Testing was performed to verify that the core functionality of API EXPORT works correctly.

The project uses Pytest for automated backend testing.

10.1 Testing Objectives

The main testing objectives are:

Verify API functionality.
Verify lead creation.
Verify lead retrieval.
Verify lead update operations.
Verify validation-related behavior.
Identify backend errors.
Ensure that important application operations return expected results.
10.2 Testing Framework

The project uses:

Pytest

The test suite can be executed using:

python -m pytest -q
10.3 Test Environment

Testing was performed in the local development environment using:

Python 3.13
FastAPI
Uvicorn
SQLite
SQLAlchemy
Pydantic
Pytest
10.4 Automated Test Cases

The project includes automated tests for core API behavior.

The tested functionality includes:

Test Area	Purpose
Lead Creation	Verify that a new lead can be created
Lead Retrieval	Verify that lead information can be retrieved
Lead Update	Verify that existing lead information can be updated
API Validation	Verify expected API behavior and validation
10.5 Test Execution

The command used to execute the tests is:

python -m pytest -q
10.6 Test Result

The current verified test result is:

4 passed

This indicates that the implemented automated test cases completed successfully.

10.7 Manual Testing

In addition to automated testing, the application was manually tested through:

Web dashboard
Swagger UI
Buyer Discovery interface
Lead management interface
Outreach interface
Follow-up interface
Analytics dashboard

The Gmail integration was also tested through the configured Gmail account, and the outreach workflow successfully demonstrated email sending.

10.8 API Testing

The FastAPI Swagger UI was used to inspect and test backend endpoints.

The Swagger interface allows individual API requests to be executed and their responses to be inspected.

This was useful for verifying:

Request formats
Response formats
Status codes
Backend behavior
Error handling
10.9 Integration Testing

Several application components were tested together as part of the complete workflow.

For example:

Lead
 ↓
Validation
 ↓
Outreach Preparation
 ↓
Gmail
 ↓
Database Update
 ↓
Follow-up
 ↓
Analytics

This helped verify that information was correctly transferred between the different application modules.

10.10 Testing Outcome

Testing confirmed that the core backend functionality is operational in the local development environment.

The automated test suite currently reports:

4 passed

The dashboard, API documentation, lead management, discovery workflow, outreach functionality, and analytics were also tested during development.

11. Limitations

Although API EXPORT provides an integrated export buyer discovery and outreach workflow, the current implementation has several limitations.

11.1 Local Database

The application currently uses SQLite as the primary database.

SQLite is suitable for local development and prototype usage but may not be the ideal choice for a large multi-user production system with high concurrent database activity.

11.2 Web Search Result Quality

Buyer discovery depends on external web search results.

Search results may contain:

Incomplete company information
Duplicate information
Directory listings
Outdated information
Companies that may not actually be suitable buyers

Therefore, discovered leads may require manual review.

11.3 Contact Information Availability

Not every discovered company provides a public email address or complete contact information.

As a result, some leads may not be immediately suitable for outreach.

11.4 AI Qualification Dependency

The AI qualification functionality depends on access to the configured OpenAI API service.

AI classification is intended as an assistance mechanism and should not be treated as a guaranteed determination of buyer status.

Human verification remains important.

11.5 Email Sending Dependency

Gmail outreach depends on the availability and configuration of Gmail API authentication.

Changes to account permissions, OAuth credentials, API restrictions, or service availability may affect email sending.

11.6 Response Tracking

The current response tracking functionality stores response status information but does not provide a complete automated email inbox intelligence system.

More advanced response detection could be added in a future version.

11.7 Follow-up Automation

The current system supports follow-up scheduling and identification of due follow-ups, but a production system could use a dedicated scheduling service for fully automated recurring follow-up execution.

11.8 Scalability

The current implementation is primarily designed for local development and internship/project demonstration purposes.

A production deployment would require additional infrastructure for:

High availability
Concurrent users
Larger databases
Background processing
Monitoring
Logging
Authentication
Cloud deployment
11.9 Data Verification

Information collected from public web sources should be manually reviewed before important business decisions or outreach.

Automated discovery and qualification can reduce manual work but cannot guarantee that every discovered company is a suitable buyer.

12. Future Enhancements

API EXPORT provides a foundation that can be extended with additional features.

12.1 Production Database

The application can be migrated from SQLite to a production database such as PostgreSQL when larger datasets and concurrent users need to be supported.

12.2 Advanced Authentication

A future version can implement user authentication and role-based access control.

Possible roles include:

Administrator
Sales Manager
Sales Executive
Viewer

Different users could then receive different permissions.

12.3 Advanced Buyer Discovery

Buyer discovery can be enhanced with more advanced search and filtering mechanisms.

Future functionality could include:

Country-specific filtering
Industry-specific filtering
Company-size filtering
Buyer-type filtering
Website quality checks
Domain verification
Better result ranking
12.4 Improved Duplicate Detection

Duplicate detection can be enhanced using more advanced matching techniques.

Future matching could consider:

Company name similarity
Website domain
Email domain
Phone number
Country
Address
Fuzzy matching

This could improve the identification of duplicate companies even when their names are written differently.

12.5 Advanced Email Validation

The validation module could be extended with additional email verification services.

Possible improvements include:

Domain verification
MX record checks
Disposable email detection
Mailbox verification
Email risk scoring
12.6 Improved AI Qualification

The AI module can be extended to provide more detailed lead analysis.

Future outputs could include:

Buyer relevance score
Buyer type
Product relevance
Market relevance
Company size estimation
Qualification explanation
Recommended outreach approach

AI results should continue to be treated as decision-support information rather than guaranteed facts.

12.7 Automated Response Detection

Future versions can integrate Gmail inbox processing to detect buyer responses automatically.

A possible workflow is:

Email Sent
    ↓
Buyer Response
    ↓
Gmail Inbox
    ↓
Response Detection
    ↓
Lead Status Update
    ↓
Dashboard
12.8 Automated Follow-up Scheduling

A background task or scheduling service could automatically send follow-ups when their scheduled time is reached.

This would reduce the need for manual follow-up execution.

12.9 Advanced Analytics

The analytics module could be expanded with additional business metrics such as:

Outreach conversion rate
Response rate
Follow-up conversion
Country-wise lead distribution
Industry-wise lead distribution
Buyer-type distribution
Email performance
Lead-source performance
12.10 Export and Reporting

Future versions could provide downloadable reports in formats such as:

CSV
Excel
PDF

Users could generate reports based on selected countries, industries, lead statuses, or outreach periods.

12.11 Cloud Deployment

The application can be deployed to a cloud environment for remote access.

A future architecture could include:

User
 ↓
Cloud Web Application
 ↓
FastAPI Backend
 ↓
PostgreSQL
 ↓
Background Workers
 ↓
External APIs
12.12 Background Processing

Long-running operations such as large-scale buyer discovery, lead validation, and outreach processing could be moved to background workers.

This would improve responsiveness of the main web application.

12.13 Monitoring and Logging

A production version could implement centralized logging and monitoring.

This could help track:

API errors
Search failures
Email failures
Database errors
Authentication problems
Application performance
12.14 Improved Dashboard

The dashboard could be expanded with:

Interactive charts
Advanced filters
Search
Sorting
Bulk operations
Lead segmentation
Export functionality
Custom reports
12.15 Multi-User Sales Workflow

A future version could support multiple sales users working with the same lead database.

Users could be assigned leads and track responsibility for outreach and follow-up.

13. Conclusion

API EXPORT provides a centralized platform for managing the export buyer discovery and outreach lifecycle.

The project integrates several important activities into a structured workflow, including:

Buyer discovery
Lead collection
Duplicate detection
Lead validation
AI-assisted qualification
Outreach preparation
Gmail communication
Follow-up tracking
Response tracking
Analytics

The FastAPI backend provides a modular REST API architecture, while the SQLite database provides centralized storage for lead and outreach information. The HTML, CSS, and JavaScript dashboard provides an accessible interface for interacting with the system.

The integration of the Tavily Web Search API supports web-based buyer discovery, while the OpenAI API provides AI-assisted lead qualification functionality. Gmail API integration enables business outreach through a configured Gmail account.

The project also includes automated backend testing using Pytest, with the current verified test suite reporting:

4 passed

The current implementation demonstrates how multiple technologies and external APIs can be combined to create a structured export-sales automation platform.

Although the present version is primarily designed for local development and internship/project demonstration, the architecture provides a foundation for future improvements such as production database deployment, advanced authentication, automated response detection, background processing, advanced analytics, cloud deployment, and multi-user sales management.