from pydantic import BaseModel
from typing import Optional


class LeadCreate(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    designation: Optional[str] = None

    country: str
    city: Optional[str] = None

    industry: Optional[str] = None
    product_category: Optional[str] = None

    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    source: Optional[str] = None
    notes: Optional[str] = None

class LeadUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    designation: Optional[str] = None

    country: Optional[str] = None
    city: Optional[str] = None

    industry: Optional[str] = None
    product_category: Optional[str] = None

    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    source: Optional[str] = None

    lead_status: Optional[str] = None
    validation_status: Optional[str] = None
    outreach_status: Optional[str] = None

    notes: Optional[str] = None

    # ---------------------------------------------------------
# Buyer Discovery Schema
# ---------------------------------------------------------

class BuyerDiscoveryRequest(BaseModel):
    product_category: str
    target_country: str
    industry: Optional[str] = None
    keywords: Optional[str] = None