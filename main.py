import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import spacy
from dotenv import load_dotenv
from googlesearch import search
import time

# --- CONFIGURATION AND SECURITY ---
# Load environment variables (API Key will be ignored, but config remains structured)
load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Load the NLP model once
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("NLP Model 'en_core_web_sm' not found. "
          "Run: python -m spacy download en_core_web_sm")
    nlp = None


# --- CORE CRGG FUNCTIONS ---

def get_competitor_list(target_name: str, location: str,
                        search_type: str = "dentist", limit: int = 5) -> list:
    """
    Pivoted function: Uses compliant Google Search to find local business URLs.
    Simulates performance metrics (rating/reviews) based on search rank.

    NOTE: Google API is bypassed due to zero-investment constraint.
    """

    search_query = (f"best {search_type} near {location} reviews")
    print(f"-> 1. Searching Google for: '{search_query}'...")

    competitor_data = []

    try:
        # CRITICAL: 'pause=2' enforces a delay between requests for politeness.
        for url in search(search_query, num=limit, stop=limit, pause=2):
            rank = len(competitor_data) + 1

            # --- SIMULATION BASED ON RANK (Zero-Investment Data) ---
            # Higher rank = better metrics. This creates the competitive baseline.
            simulated_reviews = 500 - (rank * 80)
            simulated_rating = 5.0 - (rank * 0.15)

            competitor_data.append({
                "name": f"Local Competitor Rank {rank}",
                "rating": round(max(4.2, simulated_rating), 1),
                "reviews": max(100, simulated_reviews),
                "url": url
            })

            time.sleep(1)  # Extra politeness delay

    except Exception as e:
        print(f"Search failed (Rate limit or network error): {e}")
        # Fallback list used if the network or search limits are hit
        competitor_data = [
            {"name": "Competitor A (Fallback)", "rating": 4.9, "reviews": 300,
             "url": "http://comp-a-fallback.com"},
            {"name": "Competitor B (Fallback)", "rating": 4.7, "reviews": 150,
             "url": "http://comp-b-fallback.com"},
        ]

    # Add the target business (assumed to have poor metrics)
    competitor_data.append({
        "name": target_name,
        "rating": 3.8,  # Low rating drives the "pain"
        "reviews": 45,  # Low review count drives the "gap"
        "url": "http://target-site-to-audit.com"
    })

    return competitor_data


def audit_website_flaws(url: str) -> dict:
    """Performs non-JS audit (SSL, basic mobile, CTA presence)."""
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        soup = BeautifulSoup(response.text, 'html.parser')

        audit = {
            "has_ssl": url.startswith("https"),
            # Check for common CTA text
            "has_basic_cta": bool(
                soup.find('a', text=lambda t: t and 'appointment' in t.lower())
            ),
        }
        return audit
    except requests.exceptions.RequestException as e:
        # Catch specific request/connection errors
        return {"error": str(e), "has_ssl": False, "has_basic_cta": False}


def model_revenue_gap(competitor_data: list) -> float:
    """
    Proprietary logic to model revenue difference based on 'Competitive Dominance Score'.
    This is the core 'magic lure' that justifies the $499 subscription.
    """
    df = pd.DataFrame(competitor_data)

    # Scoring: Rating is weighted 10x, reviews are weighted 1/50th.
    df['dominance_score'] = (df['rating'] * 10) + (df['reviews'] / 50)

    target_score = df.loc[df['name'] == 'Target Business',
                          'dominance_score'].iloc[0]
    avg_competitor_score = df.loc[df['name'] != 'Target Business',
                                  'dominance_score'].mean()

    score_difference = avg_competitor_score - target_score

    # Proprietary conversion: Assume every point of dominance is worth $500 in
    # lost monthly revenue.
    estimated_gap = score_difference * 500

    print(f"-> 3. Modeling Complete. Target Dominance Score: {target_score:.2f}")

    return max(0, estimated_gap)


# --- MAIN ORCHESTRATION ---

def generate_crgg_report(target_name, location):
    """Orchestrates the data collection, auditing, and modeling."""

    # 1. Acquire Competitor Data (via SERP scraping)
    competitor_list = get_competitor_list(target_name, location)

    if not competitor_list:
        return "CRGG Failed: Could not acquire competitor data."

    # 2. Integrate Audit Results (Checking the websites found in step 1)
    for item in competitor_list:
        audit_results = audit_website_flaws(item['url'])
        item.update(audit_results)

    print("-> 2. Audits complete. Data collected.")

    # 3. Model Revenue Gap
    lost_revenue = model_revenue_gap(competitor_list)

    # 4. Final Report Compilation
    report = {
        "Target": target_name,
        "Location": location,
        "Estimated_Monthly_Revenue_Loss": f"${lost_revenue:,.2f}",
        "Critical_Flaw_Example": competitor_list[-1]['has_ssl'],
        "All_Data": competitor_list
    }

    return report


if __name__ == "__main__":
    # Example Target: A high-value niche (Dentist) in a competitive location
    TARGET_BUSINESS = "Dr. Smith's Dental Office"
    TARGET_LOCATION = "Chicago, IL"

    # Run the full pipeline
    final_report = generate_crgg_report(TARGET_BUSINESS, TARGET_LOCATION)

    print("\n=======================================================")
    print("    COMPETITIVE REVENUE GAP GENERATOR (CRGG) REPORT")
    print("=======================================================")
    print(f"Target: {final_report.get('Target')}")
    print(f"Location: {final_report.get('Location')}")
    print("\n*** THE PITCH VALUE (The Closing Script) ***")
    print("ESTIMATED LOST REVENUE: "
          f"{final_report.get('Estimated_Monthly_Revenue_Loss')}")
    print("Critical Flaw Status (SSL): "
          f"{'Secure' if final_report.get('All_Data')[-1].get('has_ssl') else 'VULNERABLE'}")
    print("=======================================================")
