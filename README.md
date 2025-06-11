# Real Estate Listing Scraper by ZIP Code

## Team Members
- Zhixi Lin (zl536)  
- Seth Coward (sac484)  
- Maryam Nasralla (mn688)  
- Andrew Stevens (aes464)

## Project Overview
This project facilitates users to search for real estate properties in any U.S. ZIP code by pulling live data from Redfin. The intention here is to make real estate information simpler to query, filter, and bookmark — particularly because Redfin does not offer an open API.

The results can be filtered by cost, bedrooms, bathroom numbers, and square feet. The tool offers an interactive interface and can export results in CSV or in JSON format. Web scraping in Python via the requests and BeautifulSoup libraries collects data.

## Source and Collection of Data
We scrape data from Redfin.com via ZIP code searches. Listings from multiple pages are parsed for address, price, number of bedrooms/baths, and square feet.

## Files Included
| File Name                      | Description                                           |
|-------------------------------|-------------------------------------------------------|
| real_estate_interactive1.ipynb | Final interactive notebook created by Zhixi Lin       |
| scraper.py                    | Modular scraper and filter functions by Zhixi Lin     |
| INFO153-PROJECT-G3.ipynb      | Seth Coward’s original version                        |
| INFO153-PROJECT-G3_v2.ipynb   | Andrew Stevens’ updated version                       |


## How to Use
1. Open `real_estate_interactive1.ipynb` in Jupyter Notebook.
2. Run each cell in order.
3. Enter a ZIP code and any filters when prompted.
4. View results and choose to save as CSV or JSON.

## Notes
- Requires internet connection to access Redfin.
- Make sure to install the required packages before running.

## Requirements
Install the following packages before running:
```bash
pip install requests beautifulsoup4
