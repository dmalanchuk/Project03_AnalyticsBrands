import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

urls = [
    "https://www.nike.com/w/mens-clothing-6ymx6znik1", 
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

data = []

page_limit = 3
current_page = 0

def parse_main_page(url):
    global current_page
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f'Loading page {url} successful')
        soup = bs(response.text, "html.parser")

        product_links = soup.select("a.product-card__link-overlay")

        if not product_links:
            print("No product links found. Check the CSS selector for product links.")
        
        for link in product_links:
            if current_page >= page_limit:
                print(f"Reached page limit of {page_limit} products.")
                return
            product_url = link['href']
            print(f"Parsing product page: {product_url}")
            parse_product_page(product_url)
            current_page += 1
            time.sleep(2)

def parse_product_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = bs(response.text, "html.parser")

        title_element = soup.find("h1", class_="product-title")
        title = title_element.text.strip() if title_element else "No title"
        print(f"Product title: {title}")

        star_elements = soup.find_all("svg", class_="star-icon--full")
        star_count = len(star_elements)
        print(f"Rating: {star_count} stars")

        reviews_count_element = soup.find("div", class_="reviews-count")
        reviews_count = 0
        if reviews_count_element:
            reviews_count = 1  
        print(f"Reviews count: {reviews_count}")

        data.append({
            'title': title,
            'star_count': star_count,
            'reviews_count': reviews_count
        })

if __name__ == "__main__":
    for url in urls:
        parse_main_page(url)

    if data:
        df = pd.DataFrame(data)
        df.to_excel("brands_reviews.xlsx", index=False)
        print("Дані збережено в brands_reviews.xlsx")
    else:
        print("No data collected.")
