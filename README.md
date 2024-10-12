# Product Reviews Scraper API

This project is a web application built with Flask that scrapes product reviews from any product page (like Amazon or Shopify) using a browser automation tool (such as Playwright). It also displays these reviews in a beautiful HTML template with dynamic CSS styling.




## Project Overview

The API scrapes reviews from any e-commerce product page, handles pagination, and dynamically identifies CSS selectors for extracting review data. It supports fetching and displaying the following information:
- Review Title
- Review Body
- Rating
- Reviewer Name

The scraped data is served via a RESTful API and can be rendered in an HTML page.

---

## Features

- **Dynamic Review Scraping**: Supports multiple platforms by dynamically detecting the CSS elements for reviews.
- **Pagination Handling**: Automatically navigates through multiple pages to gather all reviews.
- **API with Flask**: Provides a `/api/reviews` endpoint to fetch reviews in JSON format.
- **Frontend Display**: A clean and visually appealing web interface to view the scraped reviews.
- **Browser Automation**: Uses Playwright (or Puppeteer/Selenium) for browser automation.

---

## Prerequisites

Make sure you have the following installed:

- **Python 3.8+**
- **pip** (Python package manager)
- **Git** (optional but recommended)

---

## Installation

Follow these steps to install and run the project locally:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/review-scraper.git
   cd review-scraper

2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   

3.  **Install the Required Dependencies**:
    ```bash
    pip install -r requirements.txt

4.  **Install Playwright and its dependencies**:
    ```bash
    pip install playwright
    playwright install

## Running the Project

1.  **Start the Flask Server**:
    ```bash
    python app.py

2.  **Visit the Web Application**: 
    ```bash
    Open your browser and go to http://127.0.0.1:5000.
 
3.  **Access the API**:
    ```bash
    [text](http://127.0.0.1:5000/api/reviews?page=<YOUR_PRODUCT_PAGE_URL>)

    