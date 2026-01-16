 # Ekantipur Scraper

A Python-based web scraper for Ekantipur news articles, built using Playwright.  
This project extracts headlines, article links, and other relevant information from the Ekantipur website for data analysis and research purposes.

---

## Features

- Scrapes news articles and metadata from Ekantipur.
- Supports dynamic content using Playwright.
- Stores results in structured formats (CSV/JSON).
- Easy to configure and extend for additional scraping tasks.

---

## Technologies Used

- Python 3.14+
- Playwright for browser automation
- Pandas (optional, for data processing)

## Installation

1. Clone this repository:

git clone https://github.com/YOUR_USERNAME/ekantipur-scraper.git
cd ekantipur-scraper

2. Install dependencies

pip install -r requirements.txt

3. Install Playwright browsers:

playwright install

## Usage

Run the scraper script:

python scraper.py


The scraped data will be saved to the output folder in CSV/JSON format.

Project Structure
ekantipur-scraper/
│
├── scraper.py          # Main scraper script
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── output/             # Folder for scraped data

