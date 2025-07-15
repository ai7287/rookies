# modules/nvd_fetcher.py

import requests
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from .translator import translate_text_to_korean

load_dotenv()
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_nvd_cves(keywords, days=7):
    if not keywords:
        return []

    api_key = os.getenv("NVD_KEY")
    headers = {"apiKey": api_key} if api_key else {}

    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)
    keyword_str = " ".join(keywords)

    params = {
        "resultsPerPage": 50,
        "pubStartDate": start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "pubEndDate": end_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "keywordSearch": keyword_str
    }

    processed_cves = []
    try:
        response = requests.get(NVD_API_URL, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        for item in data.get("vulnerabilities", []):
            cve_data = item.get("cve", {})
            cve_id = cve_data.get("id", "N/A")
            description_en = next(
                (d["value"] for d in cve_data.get("descriptions", []) if d["lang"] == "en"), ""
            )
            
            if not description_en or "REJECT" in description_en:
                continue

            description_ko = translate_text_to_korean(description_en)
            
            cvss_score = None
            metrics = cve_data.get("metrics", {})
            if "cvssMetricV31" in metrics:
                cvss_score = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]

            processed_cves.append({
                "source": "NVD",
                "id": cve_id,
                "description_en": description_en,
                "description_ko": description_ko,
                "score": cvss_score,
                "link": f"https://nvd.nist.gov/vuln/detail/{cve_id}"
            })
    except Exception as e:
        print(f"NVD 처리 에러: {e}")

    return processed_cves