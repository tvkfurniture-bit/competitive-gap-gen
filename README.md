# 💰 Competitive Revenue Gap Generator (CRGG)

### **The Python Engine that Closes High-Ticket Agency Deals**

The **CRGG** is a proprietary Python solution designed to overcome the 2026 market challenge: **lead saturation**. We do not sell lists; we sell the **irrefutable pitch** by quantifying the revenue loss a target business experiences when compared to its top local competitors.

---

## 1. Project Overview & Value Proposition

**Problem Solved:** SEO agencies' primary bottleneck is not lead generation, but converting warm leads into high-paying retainer clients.
**Our Solution:** The CRGG generates a detailed, proprietary report that models the **financial cost of digital flaws**. This empowers sales teams to pivot the conversation from technical fixes (SSL, speed) to hard revenue loss (e.g., "$15,000 in lost patient volume").

**Value Delivered:**
1.  **Undeniable Justification:** Provides hard data points to justify a 4-figure monthly retainer.
2.  **Competitive Edge:** Focuses on the target's Top 5 local competitors, showing where the client is losing revenue.
3.  **Automation:** Automates the most complex, time-consuming part of the sales cycle (Competitive Financial Analysis).

---

## 2. Technical Architecture (Powered by Python)

The CRGG executes a four-phase, zero-investment pipeline:

1.  **Acquisition (`requests`, Google Places API):** Pulls GMB profiles and website URLs for the target and its competitors in a specific geography/niche (e.g., Dentists in Chicago).
2.  **Auditing (`BeautifulSoup`, `requests`):** Performs foundational checks (SSL, Mobile tags, CTAs).
3.  **Competitive Modeling (`Pandas`, NLP/SpaCy):** Analyzes GMB review keywords, review velocity, and rank placement of competitors to build a weighted "Competitive Dominance Score."
4.  **Revenue Gap Calculation:** Applies a proprietary formula to the dominance score to estimate the target's current monthly revenue loss (the **Revenue Gap**).

---

## 3. Setup and Deployment

### A. Environment Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/tvkfurniture-bit/competitive-gap-gen.git
    cd competitive-gap-gen
    ```
2.  **Create Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Use `venv\Scripts\activate` on Windows
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Remember to also run `python -m spacy download en_core_web_sm` if using Spacy for NLP.*

### B. API Configuration (SECURE)

The project requires the following environment variable for core functionality:

1.  Create a file named `.env` in the root directory (this file is excluded by `.gitignore`).
2.  Add your API key:
    ```
    # Obtain a key from Google Cloud Console
    GOOGLE_MAPS_API_KEY="YOUR_SECRET_API_KEY_HERE"
    ```

### C. Execution

Run the primary script:
```bash
python main.py
