import json
import requests
import os

LISTING_FILE = ".github/scripts/listing.json"
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "internship-alerts")  # Replace if not using env vars
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

def load_listings():
    """Load JSON data from listing.json"""
    try:
        with open(LISTING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def send_notification(title, link):
    """Send a notification via ntfy.sh"""
    requests.post(NTFY_URL, data=title.encode(), headers={"Click": link})

def main():
    listings = load_listings()
    for listing in listings:
        title = listing.get("title", "").lower()
        sponsorship = listing.get("sponsorship", "").lower()
        active = listing.get("active", False)
        url = listing.get("url", "")

        if active and "software" in title and "intern" in title and "u.s. citizenship is required" not in sponsorship:
            send_notification(f"New Internship: {listing['title']}", url)

if __name__ == "__main__":
    main()
