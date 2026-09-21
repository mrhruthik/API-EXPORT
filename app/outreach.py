from datetime import datetime, timedelta

from .database import SessionLocal
from . import models


def create_outreach_message(lead):
    """
    Creates a professional export buyer outreach email
    using the information already stored for the lead.
    """

    company_name = lead.company_name or "your company"
    product = lead.product_category or "our products"
    country = lead.country or "your market"

    subject = (
        f"Business Opportunity – {product.title()} "
        f"for {company_name}"
    )

    greeting = (
        f"Dear {lead.contact_name},"
        if lead.contact_name
        else f"Dear {company_name} Team,"
    )

    body = f"""Hello,

I am reaching out regarding a potential business opportunity
for {product} in {country}.

We are currently looking to connect with established companies
in the {lead.industry or "food and beverage"} sector that may be
interested in sourcing reliable products for their market.

We would be happy to share:

• Product details
• Product specifications
• Pricing information
• Minimum order quantities
• Export and shipping details
• Company information

If {company_name} is currently sourcing or importing
{product}, we would be glad to discuss a potential
business relationship.

Please let us know if this would be relevant to your
purchasing or procurement team.

Best regards,
API EXPORT
International Business Development
"""

    return subject, body


def prepare_outreach_for_lead(lead):
    """
    Generates and stores an outreach email for one lead.
    """

    if not lead.email:
        return False, "Lead does not have an email address."

    if lead.outreach_status == "SENT":
        return False, "Outreach has already been sent."

    subject, body = create_outreach_message(lead)

    lead.outreach_subject = subject
    lead.outreach_body = body

    lead.outreach_status = "READY_TO_SEND"

    lead.response_status = "NO_RESPONSE"

    lead.follow_up_at = datetime.utcnow() + timedelta(days=5)

    return True, "Outreach prepared successfully."


def prepare_all_outreach():
    """
    Generates outreach messages for all valid leads
    that have email addresses.
    """

    db = SessionLocal()

    prepared = 0
    skipped = 0

    try:
        leads = (
            db.query(models.Lead)
            .filter(
                models.Lead.validation_status == "VALID",
                models.Lead.email.isnot(None),
                models.Lead.outreach_status == "NOT_CONTACTED"
            )
            .all()
        )

        print(f"\nFound {len(leads)} leads ready for outreach.\n")

        for lead in leads:

            success, message = prepare_outreach_for_lead(lead)

            if success:
                prepared += 1

                print(
                    f"Prepared ID {lead.id}: "
                    f"{lead.company_name}"
                )

            else:
                skipped += 1

                print(
                    f"Skipped ID {lead.id}: "
                    f"{message}"
                )

        db.commit()

        print("\n--------------------------------")
        print("OUTREACH PREPARATION COMPLETE")
        print("--------------------------------")
        print(f"Prepared: {prepared}")
        print(f"Skipped:  {skipped}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    prepare_all_outreach()