import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from .database import SessionLocal
from . import models


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is missing from the .env file."
    )

client = OpenAI(api_key=OPENAI_API_KEY)


def classify_lead(lead):
    prompt = f"""
You are an international export lead qualification assistant.

Analyze the following company lead.

Company:
{lead.company_name}

Country:
{lead.country}

Industry:
{lead.industry}

Product category:
{lead.product_category}

Website:
{lead.website}

Determine whether this company is a relevant potential BUYER,
IMPORTER, DISTRIBUTOR, WHOLESALER, or TRADING COMPANY for the
specified product category.

Reject:
- directories
- marketplaces
- news websites
- reports
- events
- consulting companies
- government pages
- manufacturers that clearly do not buy/import/distribute
- supplier-only pages
- irrelevant companies

Return ONLY valid JSON:

{{
    "classification": "BUYER" or "NOT_BUYER",
    "buyer_type": "IMPORTER" or "DISTRIBUTOR" or "WHOLESALER" or "TRADING_COMPANY" or "BUYER" or "UNKNOWN",
    "relevance": "HIGH" or "MEDIUM" or "LOW",
    "reason": "short explanation"
}}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    text = response.output_text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "classification": "NOT_BUYER",
            "buyer_type": "UNKNOWN",
            "relevance": "LOW",
            "reason": "AI returned an invalid classification response."
        }


def main():
    db = SessionLocal()

    try:
        leads = (
            db.query(models.Lead)
            .filter(
                models.Lead.validation_status == "PENDING"
            )
            .all()
        )

        print(f"\nFound {len(leads)} leads to classify.\n")

        for lead in leads:

            print(
                f"Analyzing ID {lead.id}: "
                f"{lead.company_name}"
            )

            try:
                result = classify_lead(lead)

                print(
                    f"Result: "
                    f"{result['classification']} | "
                    f"{result['buyer_type']} | "
                    f"{result['relevance']}"
                )

                print(
                    f"Reason: {result['reason']}\n"
                )

                if result["classification"] == "BUYER":
                    lead.lead_status = "QUALIFIED"
                    lead.validation_status = "VALID"

                    existing_notes = lead.notes or ""

                    lead.notes = (
                        existing_notes
                        + "\nAI Classification: BUYER"
                        + f"\nBuyer Type: {result['buyer_type']}"
                        + f"\nRelevance: {result['relevance']}"
                        + f"\nReason: {result['reason']}"
                    )

                else:
                    lead.lead_status = "REJECTED"
                    lead.validation_status = "INVALID"

                    existing_notes = lead.notes or ""

                    lead.notes = (
                        existing_notes
                        + "\nAI Classification: NOT_BUYER"
                        + f"\nReason: {result['reason']}"
                    )

                db.commit()

            except Exception as e:
                print(
                    f"ERROR for lead {lead.id}: {e}\n"
                )
                db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    main()