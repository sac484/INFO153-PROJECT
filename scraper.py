# Import the libraries
import requests
from bs4 import BeautifulSoup
import re
import time

# Define headers
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

# Create session
web_session = requests.Session()
web_session.headers.update(headers)

# Define Queue
class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

# Get all URL for a specific ZIP code given from Redfin
def get_all_page_urls(zip_code):
    url_queue = Queue()
    base_url = f"https://www.redfin.com/zipcode/{zip_code}/"
    page_regex = re.compile("Viewing page \\d+ of (\\d+)")

    # Send initial request
    request = web_session.get(base_url)
    if request.status_code != 200:
        return url_queue
    html_body = request.text
    page = BeautifulSoup(html_body, "html.parser")

    # Element that gives number of pages in total
    element = page.find("span", attrs={"data-rf-test-name": "download-and-save-page-number-text"})
    if element is None:
        return url_queue
    regex_result = page_regex.search(element.get_text())
    if regex_result is None:
        return url_queue
    url_queue.enqueue(base_url)
    max_page = int(regex_result.group(1))
    for i in range(2, max_page + 1):
        url_queue.enqueue(f"{base_url}page-{i}")
    return url_queue

# Gets all property listings for a ZIP code
def get_all_listings(zip_code):
    page_url_queue = get_all_page_urls(zip_code)
    all_listings = []
    while not page_url_queue.is_empty():
        url = page_url_queue.dequeue()
        html_body = web_session.get(url).text
        page = BeautifulSoup(html_body, "html.parser")
        for listing_card in page.find_all("div", class_="HomeCardContainer"):

            # Skips ads
            if listing_card.get("aria-label") == "Advertisement":
                continue
            try:
                # Gets listing details
                listing_href = listing_card.find("a", href=True, class_="bp-InteractiveHomecard")["href"]
                price = listing_card.find("span", class_="bp-Homecard__Price--value").text
                price = float(price[1:].replace(",", ""))
                address = listing_card.find("div", class_="bp-Homecard__Address").string

                # Number of bedrooms
                num_beds = listing_card.find("span", class_="bp-Homecard__Stats--beds").string.split(" ")[0]
                if num_beds == "—":
                    continue
                else:
                    num_beds = float(num_beds)

                # Number of bathrooms
                num_baths = listing_card.find("span", class_="bp-Homecard__Stats--baths").string.split(" ")[0]
                if num_baths == "—":
                    continue
                else:
                    num_baths = float(num_baths)

                # Square footage
                square_footage = listing_card.find("span", class_="bp-Homecard__Stats--sqft").find_all(string=True)[0]
                if square_footage in ["—", "sq ft"]:
                    continue
                else:
                    square_footage = float(square_footage.replace(",", ""))

                # Contact info for agent
                try:
                    contact_info = listing_card.find("div", class_="bp-Homecard__Attribution").string
                except AttributeError:
                    contact_info = "See listing via URL"

                # Dictionary
                listing_info = {
                    "listing_url": f"https://redfin.com{listing_href}",
                    "price": price,
                    "address": address,
                    "num_beds": num_beds,
                    "num_baths": num_baths,
                    "square_footage": square_footage,
                    "contact_info": contact_info
                }
                all_listings.append(listing_info)
            except Exception:
                continue
        time.sleep(1)
    return all_listings

# Apply filters
def filter_listings(all_listings, min_price=None, max_price=None, min_beds=None, max_beds=None,
                    min_baths=None, max_baths=None, min_sqft=None, max_sqft=None):
    filtered_listings = []
    for listing in all_listings:
        # Filter conditions for each listing
        conditions = [
            (min_price is None or listing["price"] >= min_price),
            (max_price is None or listing["price"] <= max_price),
            (min_beds is None or listing["num_beds"] >= min_beds),
            (max_beds is None or listing["num_beds"] <= max_beds),
            (min_baths is None or listing["num_baths"] >= min_baths),
            (max_baths is None or listing["num_baths"] <= max_baths),
            (min_sqft is None or listing["square_footage"] >= min_sqft),
            (max_sqft is None or listing["square_footage"] <= max_sqft)
        ]
        if all(conditions):
            filtered_listings.append(listing)
    return filtered_listings
