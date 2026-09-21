from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    # ---------------------------------------------------------
    # Company / Contact Information
    # ---------------------------------------------------------

    company_name = Column(
        String(200),
        nullable=False
    )

    contact_name = Column(
        String(150),
        nullable=True
    )

    designation = Column(
        String(150),
        nullable=True
    )

    country = Column(
        String(100),
        nullable=False
    )

    city = Column(
        String(100),
        nullable=True
    )

    # ---------------------------------------------------------
    # Business Information
    # ---------------------------------------------------------

    industry = Column(
        String(150),
        nullable=True
    )

    product_category = Column(
        String(150),
        nullable=True
    )

    website = Column(
        String(300),
        nullable=True
    )

    email = Column(
        String(255),
        nullable=True
    )

    phone = Column(
        String(50),
        nullable=True
    )

    source = Column(
        String(150),
        nullable=True
    )

    # ---------------------------------------------------------
    # Lead Management
    # ---------------------------------------------------------

    lead_status = Column(
        String(50),
        nullable=False,
        default="NEW"
    )

    validation_status = Column(
        String(50),
        nullable=False,
        default="PENDING"
    )

    # ---------------------------------------------------------
    # Outreach Management
    # ---------------------------------------------------------

    outreach_status = Column(
        String(50),
        nullable=False,
        default="NOT_CONTACTED"
    )

    outreach_subject = Column(
        String(300),
        nullable=True
    )

    outreach_body = Column(
        Text,
        nullable=True
    )

    sent_at = Column(
        DateTime,
        nullable=True
    )

    follow_up_at = Column(
        DateTime,
        nullable=True
    )

    response_status = Column(
        String(50),
        nullable=True,
        default="NO_RESPONSE"
    )

    # ---------------------------------------------------------
    # Notes
    # ---------------------------------------------------------

    notes = Column(
        Text,
        nullable=True
    )