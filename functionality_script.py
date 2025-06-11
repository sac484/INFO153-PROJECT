
import json
import csv
from scraper import get_all_listings, filter_listings

def save_output(listings, format_choice):
    if format_choice == "csv":
        with open("filtered_listings.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=listings[0].keys())
            writer.writeheader()
            writer.writerows(listings)
        print("Saved to filtered_listings.csv")
    elif format_choice == "json":
        with open("filtered_listings.json", "w", encoding="utf-8") as f:
            json.dump(listings, f, indent=2)
        print("Saved to filtered_listings.json")
    else:
        print("Output not saved.")

def get_user_input():
    zip_code = input("Enter ZIP code: ")
    min_price = input("Minimum price (press Enter to skip): ")
    max_price = input("Maximum price (press Enter to skip): ")
    min_beds = input("Minimum number of bedrooms (press Enter to skip): ")
    max_beds = input("Maximum number of bedrooms (press Enter to skip): ")
    min_baths = input("Minimum number of bathrooms (press Enter to skip): ")
    max_baths = input("Maximum number of bathrooms (press Enter to skip): ")
    min_sqft = input("Minimum square footage (press Enter to skip): ")
    max_sqft = input("Maximum square footage (press Enter to skip): ")

    def parse_input(value): return float(value) if value.strip() != "" else None

    return {
        "zip_code": zip_code,
        "min_price": parse_input(min_price),
        "max_price": parse_input(max_price),
        "min_beds": parse_input(min_beds),
        "max_beds": parse_input(max_beds),
        "min_baths": parse_input(min_baths),
        "max_baths": parse_input(max_baths),
        "min_sqft": parse_input(min_sqft),
        "max_sqft": parse_input(max_sqft)
    }

def main():
    filters = get_user_input()
    listings = get_all_listings(filters["zip_code"])
    filtered = filter_listings(listings,
                               min_price=filters["min_price"],
                               max_price=filters["max_price"],
                               min_beds=filters["min_beds"],
                               max_beds=filters["max_beds"],
                               min_baths=filters["min_baths"],
                               max_baths=filters["max_baths"],
                               min_sqft=filters["min_sqft"],
                               max_sqft=filters["max_sqft"])

    print(f"Found {len(filtered)} matching listings.")
    for item in filtered:
        print(item)

    output_format = input("Save results to file? (csv/json/none): ").lower()
    if filtered:
        save_output(filtered, output_format)

if __name__ == "__main__":
    main()
