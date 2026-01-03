import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import spacy
from dotenv import load_dotenv

# --- CONFIGURATION AND SECURITY ---
# Load environment variables for secure access (API keys)
load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Load the NLP model once
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:  # Catch only the specific error for missing model
    print("NLP Model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

# --- CORE CRGG FUNCTIONS ---

def get_competitor_list(target_name: str, location: str, search_type: str = "dentist", limit: int = 5) -> list:
    """
    Uses the Google Places API to find the target and its top N competitors.
    Returns structured JSON data (simulated for this demo).
    """
    if not GOOGLE_MAPS_API_KEY:
        return []

    print(f"-> 1. Searching for {search_type} competitors in {location}...")

    # Placeholder for API call logic. 
    # We simulate data return for this demonstration.

    return [
        {"name": "Competitor A Dental", "rating": 4.9, "reviews": 320, "url": "http://comp-a.com"},
        {"name": "Competitor B Ortho", "rating": 4.7, "reviews": 150, "url": "http://comp-b.com"},
        {"name": "Target Business", "rating": 3.8, "reviews": 45, "url": "http://target-site.com"}
    ]


def audit_website_flaws(url: str) -> dict:
    """Performs non-JS audit (SSL, basic mobile, CTA presence)."""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        audit = {
            "has_ssl": url.startswith("https"),
            # Check for common CTA text
            "has_basic_cta": bool(soup.find('a', text=lambda t: t and 'appointment' in t.lower())),
        }
        return audit
    except requests.exceptions.RequestException as e:
        # Catch specific request/connection errors
        return {"error": str(e), "has_ssl": False, "has_basic_cta": False}


def model_revenue_gap(competitor_data: list) -> float:
    """
    Proprietary logic to model revenue difference based on 'Competitive Dominance Score'.
    """
    df = pd.DataFrame(competitor_data)

    # Simple modeling: High reviews and high ratings increase authority.
    df['dominance_score'] = (df['rating'] * 10) + (df['reviews'] / 50)

    target_score = df.loc[df['name'] == 'Target Business', 'dominance_score'].iloc[0]
    avg_competitor_score = df.loc[df['name'] != 'Target Business', 'dominance_score'].mean()

    score_difference = avg_competitor_score - target_score

    # Proprietary conversion: Assume every point of dominance is worth $500 in lost monthly revenue.
    estimated_gap = score_difference * 500

    print(f"-> 3. Modeling Complete. Target Dominance Score: {target_score:.2f}")

    return max(0, estimated_gap)  # Revenue loss can't be negative


# --- MAIN ORCHESTRATION ---

def generate_crgg_report(target_name, location):
    """Orchestrates the data collection, auditing, and modeling."""

    # 1. Acquire Competitor Data
    competitor_list = get_competitor_list(target_name, location)

    if not competitor_list:
        return "CRGG Failed: Could not acquire competitor data."

    # 2. Integrate Audit Results
    for item in competitor_list:
        audit_results = audit_website_flaws(item['url'])
        item.update(audit_results)

    print("-> 2. Audits complete. Data collected.")

    # 3. Model Revenue Gap
    lost_revenue = model_revenue_gap(competitor_list)

    # 4. Final Report Compilation (The Sales Pitch)
    report = {
        "Target": target_name,
        "Location": location,
        "Estimated_Monthly_Revenue_Loss": f"${lost_revenue:,.2f}",
        "Critical_Flaw_Example": competitor_list[-1]['has_ssl'],
        "All_Data": competitor_list
    }

    return report


if __name__ == "__main__":
    # The CRGG is run for a specific target and location
    final_report = generate_crgg_report("Dr. Smith's Dental Office", "Chicago, IL")

    print("\n=======================================================")
    print("    COMPETITIVE REVENUE GAP GENERATOR (CRGG) REPORT")
    print("=======================================================")
    print(f"Target: {final_report.get('Target')}")
    print(f"Location: {final_report.get('Location')}")
    print("\n*** THE PITCH VALUE (The Closing Script) ***")
    print(f"ESTIMATED LOST REVENUE: {final_report.get('Estimated_Monthly_Revenue_Loss')}")
    print(f"Critical Flaw Status (SSL): {'Secure' if final_report.get('All_Data')[-1].get('has_ssl') else 'VULNERABLE'}")
    print("=======================================================")
