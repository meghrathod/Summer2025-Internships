import json
import requests
import os

# Constants
LISTING_FILE = ".github/scripts/listing.json"
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "internship-alerts")  # Default to 'internship-alerts'

def load_listings():
    """Load internship listings from the JSON file."""
    try:
        with open(LISTING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []

def filter_new_internships(listings):
    """Filter internships that match the criteria."""
    matching_internships = []
    
    for listing in listings:
        title = listing.get("title", "").lower()
        sponsorship = listing.get("sponsorship", "").lower()
        active = listing.get("active", False)
        
        if "software" in title and "intern" in title and active and "u.s. citizenship is required" not in sponsorship:
            matching_internships.append(listing)
    
    return matching_internships

def send_ntfy_notification(internship):
    """Send notification via ntfy.sh."""
    title = internship.get("title", "Software Internship")
    company = internship.get("company_name", "Unknown Company")
    url = internship.get("url", "#")
    
    message = f"New Internship: {title} at {company}\n[Apply Here]({url})"
    
    response = requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode("utf-8"),
        headers={"Title": title, "Click": url}
    )
    
    if response.status_code == 200:
        print(f"Notification sent: {title} at {company}")
    else:
        print(f"Failed to send notification: {response.status_code} - {response.text}")

def main():
    listings = load_listings()
    new_internships = filter_new_internships(listings)
    
    if new_internships:
        print(f"Found {len(new_internships)} new internships. Sending notifications...")
        for internship in new_internships:
            send_ntfy_notification(internship)
    else:
        print("No new matching internships found.")

if __name__ == "__main__":
    main()
