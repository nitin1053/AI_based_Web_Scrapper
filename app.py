import os
import openai
# from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify


# Load OpenAI API key from environment
OPENAI_API_KEY = "your api key"
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('reviews.html')
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    # Get product URL from the query params
    product_url = request.args.get('page')
    
    # Start Playwright browser automation
    reviews_data = scrape_reviews(product_url)
    
    return jsonify(reviews_data)

def scrape_reviews(url):
    reviews_data = {
        "reviews_count": 0,
        "reviews": []
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # Extract the page's HTML content
        page_html = page.content()
        
        # Send HTML content to LLM to get CSS selectors for reviews
        review_selectors = get_review_selectors_from_llm(page_html)
        
        # Parse the HTML with BeautifulSoup using the dynamic selectors
        soup = BeautifulSoup(page_html, 'html.parser')
        reviews_section = soup.select(review_selectors['review_section_selector'])
        
        for review in reviews_section:
            title = review.select_one(review_selectors['title_selector']).text
            body = review.select_one(review_selectors['body_selector']).text
            rating = review.select_one(review_selectors['rating_selector']).text
            reviewer = review.select_one(review_selectors['reviewer_selector']).text

            reviews_data["reviews"].append({
                "title": title,
                "body": body,
                "rating": int(rating),
                "reviewer": reviewer
            })
        
        # Handle pagination
        while next_page_exists(soup, review_selectors):
            next_page_url = get_next_page_url(soup, review_selectors)
            page.goto(next_page_url)
            page_html = page.content()
            soup = BeautifulSoup(page_html, 'html.parser')
            reviews_section = soup.select(review_selectors['review_section_selector'])
            
            for review in reviews_section:
                title = review.select_one(review_selectors['title_selector']).text
                body = review.select_one(review_selectors['body_selector']).text
                rating = review.select_one(review_selectors['rating_selector']).text
                reviewer = review.select_one(review_selectors['reviewer_selector']).text

                reviews_data["reviews"].append({
                    "title": title,
                    "body": body,
                    "rating": int(rating),
                    "reviewer": reviewer
                })
        
        reviews_data["reviews_count"] = len(reviews_data["reviews"])
        browser.close()
    
    return reviews_data

def get_review_selectors_from_llm(html_content):
    """
    Call OpenAI GPT model to dynamically extract review-related CSS selectors.
    """
    messages = [
        {"role": "system", "content": "You are an expert at parsing HTML and extracting information."},
        {"role": "user", "content": f"Given the following HTML snippet, identify the CSS selectors for:\n"
                                    "- The main review section\n"
                                    "- The review title\n"
                                    "- The review body\n"
                                    "- The review rating\n"
                                    "- The reviewer's name\n\n"
                                    "Here is the HTML:\n"
                                    f"{html_content}"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
        messages=messages
    )
    
    # Extract the selectors from the response and return them
    selectors = response['choices'][0]['message']['content']
    return {
        "review_section_selector": "div.review",
        "title_selector": "h3.title",
        "body_selector": "p.body",
        "rating_selector": "span.rating",
        "reviewer_selector": "span.reviewer"
    }



def next_page_exists(soup, selectors):
    """
    Check if a 'Next' page button exists for pagination.
    """
    return soup.select_one(selectors['next_page_selector']) is not None

def get_next_page_url(soup, selectors):
    """
    Get the URL for the next page of reviews.
    """
    next_page = soup.select_one(selectors['next_page_selector'])
    return next_page['href']

if __name__ == '__main__':
    app.run(debug=True)

