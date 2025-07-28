import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

def scrape_isro_updates():
    url = "https://www.isro.gov.in/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <a> tags with href inside a 'latest' or 'views-field' container
        news_items = soup.find_all("a")

        updates = []
        for item in news_items:
            text = item.get_text(strip=True)
            if text and len(text) > 40 and "Read More" not in text:
                updates.append(text)

        return updates
    else:
        print("Failed to load ISRO website")
        return []

if __name__ == "__main__":
    updates = scrape_isro_updates()

    for i, item in enumerate(updates[:10], 1):  # Limit to 10 items for now
        print(f"{i}. {item}")

    # Save to data
    Path("data").mkdir(exist_ok=True)
    with open("data/isro_updates.json", "w") as f:
        json.dump(updates, f, indent=2)

    print(f"\n✅ {len(updates)} items saved to data/isro_updates.json")
