from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Body
import pandas as pd
import os
import re
from urllib.parse import urlparse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from tavily import TavilyClient

from .database import Base, engine, SessionLocal
from . import models
from .schemas import LeadCreate, LeadUpdate, BuyerDiscoveryRequest

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
# ---------------------------------------------------------
# Create database tables
# ---------------------------------------------------------

Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="API EXPORT",
    description="Export Buyer Lead Management and Outreach System",
    version="1.0.0"
)


# ---------------------------------------------------------
# Database session dependency
# ---------------------------------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------

def is_valid_email(email: str) -> bool:
    """
    Performs basic email format validation.

    This checks the format only.
    It does NOT verify whether the mailbox actually exists.
    """

    if not email:
        return False

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(pattern, email) is not None


def clean_value(value) -> str:
    """
    Converts empty/NaN spreadsheet values to an empty string
    and removes unnecessary spaces.
    """

    if pd.isna(value):
        return ""

    return str(value).strip()


def normalize_text(value: str) -> str:
    """
    Normalizes text for duplicate checking.

    Example:

        '  GLOBAL   FOODS GmbH '
        'global foods gmbh'

    both become:

        'global foods gmbh'
    """

    value = clean_value(value)

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.lower().strip()


def is_likely_company_website(url: str, title: str) -> bool:
    """
    Filters obvious directories, databases, reports and non-company pages.
    This is intentionally conservative so legitimate company websites are
    not rejected just because their title contains words such as supplier.
    """

    if not url:
        return False

    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower().replace("www.", "")
    path = parsed_url.path.lower()
    title = (title or "").lower().strip()

    blocked_domains = [
        "rocketreach.co", "tracxn.com", "ibisworld.com", "linkedin.com",
        "crunchbase.com", "zoominfo.com", "apollo.io", "dnb.com",
        "kompass.com", "yellowpages.com", "yelp.com", "wikipedia.org",
        "facebook.com", "instagram.com", "youtube.com", "getprospectx.com",
        "business-humanrights.org", "italianfoodnews.com", "foodimporters.org",
        "emneurope.website", "companydata.com", "foodcodirectory.com",
        "business.gov.uk", "usetorg.com", "tradekey.com", "yumda.com",
        "indeed.com", "europages.com", "ecd.eu", "gov.scot",
        "federalregister.gov", "marketsandmarkets.com", "grocerytradenews.com",
        "fas.usda.gov", "tradewithgeorgia.com", "bestfoodimporters.com",
        "foodimportersdirectory.com", "importersdirectory.com",
        "importersearch.com",
        "europages.co.uk", "europages.com", "foodcolors.org",
        "rolandberger.com"
    ]

    if any(blocked in domain for blocked in blocked_domains):
        return False

    blocked_extensions = [
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"
    ]

    if any(path.endswith(ext) for ext in blocked_extensions):
        return False

    blocked_path_terms = [
        "/search", "/directory", "/category/", "/categories/",
        "/article/", "/articles/", "/blog/", "/news/", "/forum/",
        "/marketplace/", "/reports/", "/report/", "/profile/",
        "/profiles/", "/company-profile/", "/trade-show/",
        "/tradefair/", "/events/", "/event/", "/sourcing-guide/", "/importers/",
        "/distributors/", "/wholesalers/"
    ]

    if any(term in path for term in blocked_path_terms):
        return False

    # Strong title indicators of non-company pages only.
    # Do NOT block generic words like "supplier" or "buyer" by themselves.
    blocked_title_phrases = [
        "company profile", "company profiles", "industry report",
        "market report", "market analysis", "market size",
        "trade fair", "trade show", "wholesale guide",
        "b2b sourcing guide", "search results", "list of companies",
        "supplier list", "importer list", "distributor list",
        "companies in germany", "buyers, importers, distributors",
        "jobs, employment", "export plan", "federal register",
        "generally recognized as safe", "private label manufacturers",
        "manufacturers in germany", "industry news", "government report",
        "research report",
        "how to ", "opportunities in ", "food distribution germany",
        "food color importer, buyer", "importer, buyer, pigment dyes",
        "b2b companies and suppliers",
        "food ingredients asia",
        "ingredients asia",
        "food ingredients"
    ]

    if any(term in title for term in blocked_title_phrases):
        return False

    # Titles that clearly describe a generic directory/list page.
    generic_directory_patterns = [
        r"^directory(?:$|[: -])",
        r"^list of ",
        r"^top \d+ ",
        r"^best \d+ ",
        r"^companies in ",
        r"^suppliers in ",
        r"^importers in ",
        r"^distributors in ",
        r"^how to ",
        r"^opportunities in ",
        r"^food distribution .*\|",
        r"^food color importer",
        r"^.* b2b companies and suppliers"
    ]

    if any(re.search(pattern, title) for pattern in generic_directory_patterns):
        return False

    # Supplier-only pages are not buyer leads. A page can still pass if it
    # explicitly presents the company as an importer, distributor, wholesaler,
    # or buyer.
    buyer_terms = [
        "importer", "importers", "distributor", "distributors",
        "wholesaler", "wholesalers", "buyer", "buyers", "purchasing",
        "procurement", "trading company", "food trading"
    ]
    supplier_terms = [
        "supplier", "suppliers", "manufacturer", "manufacturers",
        "producer", "producers"
    ]

    has_buyer_signal = any(term in title for term in buyer_terms)
    has_supplier_signal = any(term in title for term in supplier_terms)

    if has_supplier_signal and not has_buyer_signal:
        return False

    return True


# ---------------------------------------------------------
# Buyer Page Intent Filter
# ---------------------------------------------------------

def is_likely_buyer_page(url: str, title: str, content: str) -> bool:
    """
    Lightweight secondary check. Content can contain incidental words such
    as "trade show" on legitimate company sites, so only reject very strong
    document/list indicators here.
    """

    if not url:
        return False

    title = (title or "").lower()
    content = (content or "").lower()

    strong_content_terms = [
        "federal register",
        "generally recognized as safe",
        "government report",
        "list of companies",
        "directory of companies",
        "job opportunities",
        "jobs, employment",
        "trade show",
        "trade fair",
        "event registration",
        "conference registration"
    ]

    for term in strong_content_terms:
        if term in title or term in content:
            return False

    non_buyer_title_patterns = [
        r"^how to ",
        r"^why ",
        r"^what is ",
        r"^top \d+ ",
        r"^best \d+ ",
        r"^food ingredients",
        r"^.* market \(20\d\d",
        r"^.* insights",
        r"^.* trends",
        r"^.* opportunities",
    ]

    for pattern in non_buyer_title_patterns:
        if re.search(pattern, title):
            return False

    return True

# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "API EXPORT system is running",
        "status": "success"
    }


# ---------------------------------------------------------
# Create Lead
# ---------------------------------------------------------

@app.post("/leads")
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db)
):

    new_lead = models.Lead(
        company_name=lead.company_name,
        contact_name=lead.contact_name,
        designation=lead.designation,
        country=lead.country,
        city=lead.city,
        industry=lead.industry,
        product_category=lead.product_category,
        website=lead.website,
        email=lead.email,
        phone=lead.phone,
        source=lead.source,
        notes=lead.notes
    )

    db.add(new_lead)

    db.commit()

    db.refresh(new_lead)

    return {
        "message": "Lead created successfully",
        "lead_id": new_lead.id,
        "company_name": new_lead.company_name
    }


# ---------------------------------------------------------
# Get All Leads
# ---------------------------------------------------------

@app.get("/leads")
def get_leads(
    db: Session = Depends(get_db)
):

    leads = db.query(models.Lead).all()

    return leads

# ---------------------------------------------------------
# Delete Lead
# ---------------------------------------------------------

@app.delete("/leads/{lead_id}")
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    lead = db.query(
        models.Lead
    ).filter(
        models.Lead.id == lead_id
    ).first()

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    db.delete(lead)
    db.commit()

    return {
        "message": "Lead deleted successfully",
        "lead_id": lead_id
    }

# ---------------------------------------------------------
# Get Lead Source Summary
# ---------------------------------------------------------

@app.get("/leads/sources")
def get_lead_sources(
    db: Session = Depends(get_db)
):

    leads = db.query(models.Lead).all()

    source_counts = {}

    for lead in leads:

        source = lead.source

        if not source:
            source = "UNKNOWN"

        if source not in source_counts:

            source_counts[source] = 0

        source_counts[source] += 1

    return {
        "message": "Lead source summary",
        "total_leads": len(leads),
        "sources": source_counts
    }

# ---------------------------------------------------------
# Buyer Discovery Search
# ---------------------------------------------------------

@app.post("/buyers/discover")
def discover_buyers(
    request: BuyerDiscoveryRequest
):

    if not TAVILY_API_KEY:

        raise HTTPException(
            status_code=500,
            detail="Tavily API key is not configured"
        )

    search_terms = []

    search_terms.append(
        request.product_category
    )

    search_terms.append(
        request.target_country
    )

    if request.industry:

        search_terms.append(
            request.industry
        )

    if request.keywords:

        search_terms.append(
            request.keywords
        )

    search_query = " ".join(
        search_terms
    )

    # -----------------------------------------------------
    # Connect to Tavily
    # -----------------------------------------------------

    tavily_client = TavilyClient(
        api_key=TAVILY_API_KEY
    )

    try:

        response = tavily_client.search(
    search_query + " company importer distributor buyer -directory -wikipedia",
    search_depth="basic",
    max_results=10
)
    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Tavily search failed: {str(e)}"
        )

    # -----------------------------------------------------
    # Return search results
    # -----------------------------------------------------

    return {
        "message": "Buyer discovery completed",
        "search_query": search_query,
        "result_count": len(
            response.get("results", [])
        ),
        "results": response.get(
            "results",
            []
        )
    }
# ---------------------------------------------------------
# Convert Buyer Discovery Results into Lead Candidates
# ---------------------------------------------------------

@app.post("/buyers/discover/import")
def import_discovered_buyers(
    request: BuyerDiscoveryRequest,
    db: Session = Depends(get_db)
):
    if not TAVILY_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Tavily API key is not configured"
        )

    # -----------------------------------------------------
    # Build multiple targeted search queries
    # -----------------------------------------------------

    search_queries = [
        f"{request.product_category} {request.target_country} food importer",
        f"{request.product_category} {request.target_country} food distributor",
        f"{request.product_category} {request.target_country} food wholesaler",
        f"{request.product_category} {request.target_country} food buyer"
    ]

    if request.industry:
        search_queries = [
            f"{query} {request.industry}"
            for query in search_queries
        ]

    if request.keywords:
        search_queries = [
            f"{query} {request.keywords}"
            for query in search_queries
        ]

    tavily_client = TavilyClient(
        api_key=TAVILY_API_KEY
    )

    # -----------------------------------------------------
    # Search Tavily using multiple queries
    # -----------------------------------------------------

    all_results = []
    successful_queries = []
    failed_queries = []

    for search_query in search_queries:

        try:
            response = tavily_client.search(
                search_query + " -directory -wikipedia",
                search_depth="basic",
                max_results=10
            )

            results = response.get(
                "results",
                []
            )

            all_results.extend(results)
            successful_queries.append(search_query)

        except Exception as e:
            failed_queries.append({
                "query": search_query,
                "error": str(e)
            })

    # -----------------------------------------------------
    # Remove duplicate URLs from search results
    # -----------------------------------------------------

    unique_results = []
    seen_urls = set()

    for result in all_results:

        url = result.get(
            "url",
            ""
        )

        if not url:
            continue

        normalized_url = url.rstrip("/").lower()

        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)
        unique_results.append(result)

    # -----------------------------------------------------
    # Process search results
    # -----------------------------------------------------

    candidates = []
    duplicate_count = 0
    filtered_count = 0
    seen_domains_in_run = set()

    for result in unique_results:

        url = result.get(
            "url",
            ""
        )

        title = result.get(
            "title",
            ""
        )

        if not url:
            continue

        # -------------------------------------------------
        # Filter non-company pages
        # -------------------------------------------------

        if not is_likely_company_website(
            url,
            title
        ):
            filtered_count += 1
            continue

        content = result.get(
            "content",
            ""
        )

        if not is_likely_buyer_page(
            url,
            title,
            content
        ):
            filtered_count += 1
            continue

        # -------------------------------------------------
        # Keep only one result per website/domain per run
        # -------------------------------------------------

        parsed_result_url = urlparse(url)
        result_domain = parsed_result_url.netloc.lower().replace("www.", "")

        if result_domain in seen_domains_in_run:
            duplicate_count += 1
            continue

        seen_domains_in_run.add(result_domain)

        # -------------------------------------------------
        # Extract a basic company name
        # -------------------------------------------------

        company_name = title.strip()

        if not company_name:
            continue

        # -------------------------------------------------
        # Check whether website already exists
        # -------------------------------------------------

        existing_lead = db.query(
            models.Lead
        ).filter(
            models.Lead.website == url
        ).first()

        if existing_lead:
            duplicate_count += 1
            continue

        # -------------------------------------------------
        # Create lead candidate
        # -------------------------------------------------

        lead = models.Lead(
            company_name=company_name,
            country=request.target_country,
            industry=request.industry,
            product_category=request.product_category,
            website=url,
            source="Tavily Web Search",
            lead_status="NEW",
            validation_status="PENDING",
            outreach_status="NOT_CONTACTED"
        )

        db.add(lead)

        candidates.append({
            "company_name": company_name,
            "country": request.target_country,
            "industry": request.industry,
            "product_category": request.product_category,
            "website": url,
            "source": "Tavily Web Search"
        })

    # -----------------------------------------------------
    # Save discovered leads
    # -----------------------------------------------------

    try:
        db.commit()

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Could not save discovered leads: {str(e)}"
        )

    # -----------------------------------------------------
    # Return result
    # -----------------------------------------------------

    return {
        "message": "Buyer discovery import completed",
        "search_queries": search_queries,
        "successful_query_count": len(
            successful_queries
        ),
        "failed_queries": failed_queries,
        "raw_result_count": len(all_results),
        "unique_result_count": len(unique_results),
        "filtered_count": filtered_count,
        "discovered_count": len(candidates),
        "duplicate_count": duplicate_count,
        "candidates": candidates
    }


# ---------------------------------------------------------
# Get Single Lead
# ---------------------------------------------------------

@app.get("/leads/{lead_id}")
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):

    lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()

    if lead is None:

        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return lead


# ---------------------------------------------------------
# Update Lead
# ---------------------------------------------------------

@app.put("/leads/{lead_id}")
def update_lead(
    lead_id: int,
    lead_data: LeadUpdate,
    db: Session = Depends(get_db)
):

    lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()

    if lead is None:

        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    update_data = lead_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        setattr(
            lead,
            field,
            value
        )

    db.commit()

    db.refresh(lead)

    return {
        "message": "Lead updated successfully",
        "lead_id": lead.id,
        "company_name": lead.company_name
    }


# ---------------------------------------------------------
# Archive Lead
# ---------------------------------------------------------

@app.patch("/leads/{lead_id}/archive")
def archive_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):

    lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()

    if lead is None:

        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    lead.lead_status = "ARCHIVED"

    db.commit()

    db.refresh(lead)

    return {
        "message": "Lead archived successfully",
        "lead_id": lead.id,
        "company_name": lead.company_name,
        "lead_status": lead.lead_status
    }


# ---------------------------------------------------------
# Validate Lead
# ---------------------------------------------------------

@app.patch("/leads/{lead_id}/validate")
def validate_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):

    lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()

    if lead is None:

        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    validation_errors = []

    # -----------------------------------------------------
    # Check company name
    # -----------------------------------------------------

    if not lead.company_name or not lead.company_name.strip():

        validation_errors.append(
            "Company name is missing"
        )

    # -----------------------------------------------------
    # Check country
    # -----------------------------------------------------

    if not lead.country or not lead.country.strip():

        validation_errors.append(
            "Country is missing"
        )

    # -----------------------------------------------------
    # Check email
    # -----------------------------------------------------

    if not lead.email or not lead.email.strip():

        validation_errors.append(
            "Email is missing"
        )

    elif not is_valid_email(lead.email):

        validation_errors.append(
            "Invalid email format"
        )

    # -----------------------------------------------------
    # Update validation status
    # -----------------------------------------------------

    if validation_errors:

        lead.validation_status = "INVALID"

    else:

        lead.validation_status = "VALID"

    db.commit()

    db.refresh(lead)

    # -----------------------------------------------------
    # Return validation result
    # -----------------------------------------------------

    return {
        "message": "Lead validation completed",
        "lead_id": lead.id,
        "company_name": lead.company_name,
        "validation_status": lead.validation_status,
        "validation_errors": validation_errors
    }


# ---------------------------------------------------------
# Validate All Pending Leads
# ---------------------------------------------------------

@app.post("/leads/validate-all")
def validate_all_leads(
    db: Session = Depends(get_db)
):

    leads = db.query(models.Lead).filter(
        models.Lead.validation_status == "PENDING"
    ).all()

    validated_count = 0
    valid_count = 0
    invalid_count = 0

    results = []

    for lead in leads:

        validation_errors = []

        # -------------------------------------------------
        # Check company name
        # -------------------------------------------------

        if not lead.company_name or not lead.company_name.strip():

            validation_errors.append(
                "Company name is missing"
            )

        # -------------------------------------------------
        # Check country
        # -------------------------------------------------

        if not lead.country or not lead.country.strip():

            validation_errors.append(
                "Country is missing"
            )

        # -------------------------------------------------
        # Check email
        # -------------------------------------------------

        if not lead.email or not lead.email.strip():

            validation_errors.append(
                "Email is missing"
            )

        elif not is_valid_email(lead.email):

            validation_errors.append(
                "Invalid email format"
            )

        # -------------------------------------------------
        # Update validation status
        # -------------------------------------------------

        if validation_errors:

            lead.validation_status = "INVALID"
            invalid_count += 1

        else:

            lead.validation_status = "VALID"
            valid_count += 1

        validated_count += 1

        results.append({
            "lead_id": lead.id,
            "company_name": lead.company_name,
            "validation_status": lead.validation_status,
            "validation_errors": validation_errors
        })

    # -----------------------------------------------------
    # Save all validation results
    # -----------------------------------------------------

    db.commit()

    # -----------------------------------------------------
    # Return bulk validation result
    # -----------------------------------------------------

    return {
        "message": "Bulk validation completed",
        "validated_count": validated_count,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "results": results
    }


# ---------------------------------------------------------
# Import Leads from CSV / Excel
# ---------------------------------------------------------

@app.post("/leads/import")
async def import_leads(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Validate filename
    # -----------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file was provided"
        )

    # Get only the filename.
    # This prevents paths being supplied in the filename.
    original_filename = os.path.basename(
        file.filename
    )

    filename = original_filename.lower()

    allowed_extensions = [
        ".csv",
        ".xlsx"
    ]

    if not any(
        filename.endswith(ext)
        for ext in allowed_extensions
    ):

        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel (.xlsx) files are allowed"
        )

    # -----------------------------------------------------
    # Save uploaded file
    # -----------------------------------------------------

    upload_directory = "uploads"

    os.makedirs(
        upload_directory,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_directory,
        original_filename
    )

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(
                await file.read()
            )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not save uploaded file: {str(e)}"
        )

    # -----------------------------------------------------
    # Read CSV / Excel
    # -----------------------------------------------------

    try:

        if filename.endswith(".csv"):

            dataframe = pd.read_csv(
                file_path
            )

        else:

            dataframe = pd.read_excel(
                file_path
            )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"Could not read file: {str(e)}"
        )

    # -----------------------------------------------------
    # Validate required columns
    # -----------------------------------------------------

    required_columns = [
        "company_name",
        "country"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:

        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {missing_columns}"
        )

    # -----------------------------------------------------
    # Import counters
    # -----------------------------------------------------

    total_rows = len(dataframe)

    imported_count = 0

    duplicate_count = 0

    invalid_count = 0

    invalid_rows = []

    duplicate_rows = []

    # -----------------------------------------------------
    # Track duplicates inside the uploaded file itself
    # -----------------------------------------------------

    processed_company_country = set()

    processed_emails = set()

    # -----------------------------------------------------
    # Process every row
    # -----------------------------------------------------

    for index, row in dataframe.iterrows():

        # Spreadsheet-style row number.
        # Row 1 is the header.
        row_number = index + 2

        # -------------------------------------------------
        # Clean values
        # -------------------------------------------------

        company_name = clean_value(
            row.get(
                "company_name",
                ""
            )
        )

        country = clean_value(
            row.get(
                "country",
                ""
            )
        )

        email = clean_value(
            row.get(
                "email",
                ""
            )
        ).lower()

        contact_name = clean_value(
            row.get(
                "contact_name",
                ""
            )
        )

        designation = clean_value(
            row.get(
                "designation",
                ""
            )
        )

        city = clean_value(
            row.get(
                "city",
                ""
            )
        )

        industry = clean_value(
            row.get(
                "industry",
                ""
            )
        )

        product_category = clean_value(
            row.get(
                "product_category",
                ""
            )
        )

        website = clean_value(
            row.get(
                "website",
                ""
            )
        )

        phone = clean_value(
            row.get(
                "phone",
                ""
            )
        )

        source = clean_value(
            row.get(
                "source",
                ""
            )
        )

        notes = clean_value(
            row.get(
                "notes",
                ""
            )
        )

        # -------------------------------------------------
        # Validate company name
        # -------------------------------------------------

        if not company_name:

            invalid_count += 1

            invalid_rows.append({
                "row": row_number,
                "reason": "Company name is missing"
            })

            continue

        # -------------------------------------------------
        # Validate country
        # -------------------------------------------------

        if not country:

            invalid_count += 1

            invalid_rows.append({
                "row": row_number,
                "company_name": company_name,
                "reason": "Country is missing"
            })

            continue

        # -------------------------------------------------
        # Validate email if supplied
        # -------------------------------------------------

        if email and not is_valid_email(email):

            invalid_count += 1

            invalid_rows.append({
                "row": row_number,
                "company_name": company_name,
                "reason": "Invalid email format"
            })

            continue

        # -------------------------------------------------
        # Normalize values for duplicate detection
        # -------------------------------------------------

        normalized_company = normalize_text(
            company_name
        )

        normalized_country = normalize_text(
            country
        )

        normalized_email = email.lower().strip()

        company_country_key = (
            normalized_company,
            normalized_country
        )

        # -------------------------------------------------
        # Check duplicate inside current file
        # -------------------------------------------------

        if company_country_key in processed_company_country:

            duplicate_count += 1

            duplicate_rows.append({
                "row": row_number,
                "company_name": company_name,
                "reason": "Duplicate within uploaded file"
            })

            continue

        if (
            normalized_email
            and normalized_email in processed_emails
        ):

            duplicate_count += 1

            duplicate_rows.append({
                "row": row_number,
                "company_name": company_name,
                "reason": "Duplicate email within uploaded file"
            })

            continue

        # -------------------------------------------------
        # Check database duplicate
        # -------------------------------------------------

        duplicate = db.query(
            models.Lead
        ).filter(
            models.Lead.company_name.ilike(
                normalized_company
            ),
            models.Lead.country.ilike(
                normalized_country
            )
        ).first()

        # -------------------------------------------------
        # Check database duplicate by email
        # -------------------------------------------------

        if not duplicate and normalized_email:

            duplicate = db.query(
                models.Lead
            ).filter(
                models.Lead.email.ilike(
                    normalized_email
                )
            ).first()

        # -------------------------------------------------
        # Skip duplicate
        # -------------------------------------------------

        if duplicate:

            duplicate_count += 1

            duplicate_rows.append({
                "row": row_number,
                "company_name": company_name,
                "reason": "Lead already exists in database"
            })

            continue

        # -------------------------------------------------
        # Create new lead
        # -------------------------------------------------

        lead = models.Lead(
            company_name=company_name,
            contact_name=contact_name,
            designation=designation,
            country=country,
            city=city,
            industry=industry,
            product_category=product_category,
            website=website,
            email=email,
            phone=phone,
            source=source,
            notes=notes
        )

        db.add(lead)

        # Add to current-file duplicate trackers
        processed_company_country.add(
            company_country_key
        )

        if normalized_email:

            processed_emails.add(
                normalized_email
            )

        imported_count += 1

    # -----------------------------------------------------
    # Save imported leads
    # -----------------------------------------------------

    try:

        db.commit()

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database import failed: {str(e)}"
        )

    # -----------------------------------------------------
    # Import result
    # -----------------------------------------------------

    return {
        "message": "Import completed",
        "filename": original_filename,
        "total_rows": total_rows,
        "imported_count": imported_count,
        "duplicate_count": duplicate_count,
        "invalid_count": invalid_count,
        "invalid_rows": invalid_rows,
        "duplicate_rows": duplicate_rows
    }
# ---------------------------------------------------------
# Outreach Preparation
# ---------------------------------------------------------

from .outreach import prepare_outreach_for_lead
from .gmail_service import send_email
from datetime import datetime, timedelta, timezone


@app.post("/leads/{lead_id}/outreach/prepare")
def prepare_lead_outreach(
    lead_id: int,
    db: Session = Depends(get_db)
):
    lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()

    if lead is None:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    if lead.validation_status != "VALID":
        raise HTTPException(
            status_code=400,
            detail="Lead must have VALID validation status before outreach preparation"
        )

    success, message = prepare_outreach_for_lead(lead)

    if not success:
        raise HTTPException(
            status_code=400,
            detail=message
        )

    db.commit()
    db.refresh(lead)

    return {
        "message": message,
        "lead_id": lead.id,
        "company_name": lead.company_name,
        "email": lead.email,
        "outreach_status": lead.outreach_status,
        "subject": lead.outreach_subject,
        "follow_up_at": lead.follow_up_at
    }


# ---------------------------------------------------------
# Send Prepared Outreach Email
# ---------------------------------------------------------

@app.post("/leads/{lead_id}/outreach/send")
def send_lead_outreach(
    lead_id: int,
    db: Session = Depends(get_db)
):
    lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()

    if lead is None:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    if lead.outreach_status == "SENT":
        raise HTTPException(
            status_code=400,
            detail=f"Lead ID {lead.id} has already been sent an email."
        )

    if not lead.email:
        raise HTTPException(
            status_code=400,
            detail="Lead does not have an email address."
        )

    if lead.outreach_status != "READY_TO_SEND":
        raise HTTPException(
            status_code=400,
            detail="Outreach must be prepared before sending."
        )

    if not lead.outreach_subject or not lead.outreach_body:
        raise HTTPException(
            status_code=400,
            detail="Outreach subject/body is missing. Prepare outreach first."
        )

    try:
        result = send_email(
            lead.email,
            lead.outreach_subject,
            lead.outreach_body
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=502,
                detail=result.get(
                    "message",
                    "Gmail failed to send the email."
                )
            )

        # Store a naive UTC datetime because the existing SQLite
        # model uses SQLAlchemy DateTime without timezone=True.
        now_utc = datetime.now(timezone.utc).replace(tzinfo=None)

        lead.outreach_status = "SENT"
        lead.sent_at = now_utc
        lead.response_status = "NO_RESPONSE"
        lead.follow_up_at = now_utc + timedelta(days=5)

        db.commit()
        db.refresh(lead)

        return {
            "message": "Email sent successfully",
            "lead_id": lead.id,
            "company_name": lead.company_name,
            "recipient": lead.email,
            "outreach_status": lead.outreach_status,
            "sent_at": lead.sent_at,
            "follow_up_at": lead.follow_up_at,
            "response_status": lead.response_status
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Email sending failed: {str(e)}"
        )


# ---------------------------------------------------------
# Get Outreach Status
# ---------------------------------------------------------

@app.get("/leads/{lead_id}/outreach")
def get_lead_outreach(
    lead_id: int,
    db: Session = Depends(get_db)
):
    lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()

    if lead is None:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return {
        "lead_id": lead.id,
        "company_name": lead.company_name,
        "email": lead.email,
        "outreach_status": lead.outreach_status,
        "outreach_subject": lead.outreach_subject,
        "outreach_body": lead.outreach_body,
        "sent_at": lead.sent_at,
        "follow_up_at": lead.follow_up_at,
        "response_status": lead.response_status
    }


# ---------------------------------------------------------
# Outreach Summary
# ---------------------------------------------------------

@app.get("/outreach/summary")
def get_outreach_summary(
    db: Session = Depends(get_db)
):
    leads = db.query(models.Lead).all()

    summary = {
        "total_leads": len(leads),
        "not_contacted": 0,
        "ready_to_send": 0,
        "sent": 0,
        "follow_up_pending": 0,
        "responses_received": 0
    }

    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)

    for lead in leads:
        status = lead.outreach_status or "NOT_CONTACTED"

        if status == "NOT_CONTACTED":
            summary["not_contacted"] += 1
        elif status == "READY_TO_SEND":
            summary["ready_to_send"] += 1
        elif status in {"SENT", "FOLLOW_UP_SENT"}:
            summary["sent"] += 1

        if (
            lead.outreach_status == "SENT"
            and lead.follow_up_at
            and lead.follow_up_at <= now_utc
            and (lead.response_status or "NO_RESPONSE") == "NO_RESPONSE"
        ):
            summary["follow_up_pending"] += 1

        if lead.response_status and lead.response_status != "NO_RESPONSE":
            summary["responses_received"] += 1

    return summary


# ---------------------------------------------------------
# Follow-up Management - Due Follow-ups
# ---------------------------------------------------------

@app.get("/outreach/follow-ups/due")
def get_due_followups(
    db: Session = Depends(get_db)
):
    """
    Returns leads whose scheduled follow-up time has arrived and
    that have not yet received a response.
    """

    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)

    leads = db.query(models.Lead).filter(
        models.Lead.outreach_status == "SENT",
        models.Lead.follow_up_at.isnot(None),
        models.Lead.follow_up_at <= now_utc,
        models.Lead.response_status == "NO_RESPONSE"
    ).order_by(
        models.Lead.follow_up_at.asc()
    ).all()

    return {
        "count": len(leads),
        "follow_ups": [
            {
                "lead_id": lead.id,
                "company_name": lead.company_name,
                "email": lead.email,
                "sent_at": lead.sent_at,
                "follow_up_at": lead.follow_up_at,
                "response_status": lead.response_status
            }
            for lead in leads
        ]
    }


# ---------------------------------------------------------
# Send Follow-up Email
# ---------------------------------------------------------

@app.post("/leads/{lead_id}/outreach/follow-up")
def send_lead_followup(
    lead_id: int,
    db: Session = Depends(get_db)
):
    """
    Sends a follow-up only when the original outreach was sent,
    the scheduled follow-up time has arrived, and no response exists.
    """

    lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()

    if lead is None:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    if lead.outreach_status not in {"SENT", "FOLLOW_UP_SENT"}:
        raise HTTPException(
            status_code=400,
            detail="Original outreach must be sent before a follow-up can be sent."
        )

    if lead.response_status and lead.response_status != "NO_RESPONSE":
        raise HTTPException(
            status_code=400,
            detail=f"Follow-up is not allowed because response status is {lead.response_status}."
        )

    if lead.follow_up_at is None:
        raise HTTPException(
            status_code=400,
            detail="No pending follow-up is scheduled for this lead."
        )

    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)

    if lead.follow_up_at > now_utc:
        raise HTTPException(
            status_code=400,
            detail=f"Follow-up is not due until {lead.follow_up_at.isoformat()} UTC."
        )

    if not lead.email:
        raise HTTPException(
            status_code=400,
            detail="Lead does not have an email address."
        )

    original_subject = lead.outreach_subject or "Business Opportunity"
    followup_subject = (
        original_subject
        if original_subject.lower().startswith("follow-up:")
        else f"Follow-up: {original_subject}"
    )

    company_name = lead.company_name or "your company"
    product = lead.product_category or "our products"

    followup_body = f"""Hello,

I am following up on my previous email regarding a potential business opportunity for {product}.

We would be glad to share product details, specifications, pricing, minimum order quantities, and export/shipping information if {company_name} is currently sourcing or importing these products.

Please let us know if this is relevant to your purchasing or procurement team.

Best regards,
API EXPORT
International Business Development
"""

    try:
        result = send_email(
            lead.email,
            followup_subject,
            followup_body
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=502,
                detail=result.get(
                    "message",
                    "Gmail failed to send the follow-up email."
                )
            )

        lead.outreach_status = "FOLLOW_UP_SENT"
        lead.follow_up_at = None

        existing_notes = lead.notes or ""
        timestamp = now_utc.isoformat()
        lead.notes = (
            existing_notes
            + f"\nFollow-up sent at: {timestamp} UTC"
        )

        db.commit()
        db.refresh(lead)

        return {
            "message": "Follow-up email sent successfully",
            "lead_id": lead.id,
            "company_name": lead.company_name,
            "recipient": lead.email,
            "outreach_status": lead.outreach_status,
            "response_status": lead.response_status,
            "follow_up_sent_at": now_utc
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Follow-up sending failed: {str(e)}"
        )


# ---------------------------------------------------------
# Update Buyer Response Status
# ---------------------------------------------------------

@app.patch("/leads/{lead_id}/outreach/response")
def update_outreach_response(
    lead_id: int,
    payload: dict = Body(...),
    db: Session = Depends(get_db)
):
    """
    Records the current buyer response state.

    Allowed statuses:
    NO_RESPONSE, RESPONDED, INTERESTED, NOT_INTERESTED,
    BOUNCED, FOLLOW_UP_REQUIRED
    """

    lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()

    if lead is None:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    response_status = str(
        payload.get("response_status", "")
    ).strip().upper()

    allowed_statuses = {
        "NO_RESPONSE",
        "RESPONDED",
        "INTERESTED",
        "NOT_INTERESTED",
        "BOUNCED",
        "FOLLOW_UP_REQUIRED"
    }

    if response_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid response status. Allowed values: "
                + ", ".join(sorted(allowed_statuses))
            )
        )

    lead.response_status = response_status

    # A recorded response means the scheduled follow-up should no longer
    # remain pending unless the response explicitly asks for another follow-up.
    if response_status in {
        "RESPONDED",
        "INTERESTED",
        "NOT_INTERESTED",
        "BOUNCED"
    }:
        lead.follow_up_at = None

    db.commit()
    db.refresh(lead)

    return {
        "message": "Response status updated successfully",
        "lead_id": lead.id,
        "company_name": lead.company_name,
        "outreach_status": lead.outreach_status,
        "response_status": lead.response_status,
        "follow_up_at": lead.follow_up_at
    }
