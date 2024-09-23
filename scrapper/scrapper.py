import requests
from bs4 import BeautifulSoup
import urllib.parse
import os

# ScrapeOps API Key (should ideally be stored in an environment variable)
SCRAPEOPS_API_KEY = os.getenv('SCRAPEOPS_API_KEY', '6c88b0cd-0edb-4365-bc23-46e6b51b3377')


def scrape_amazon_product(product_name):
    base_url = f'https://www.amazon.com/s?k={urllib.parse.quote_plus(product_name)}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    proxy_url = 'https://proxy.scrapeops.io/v1/'

    try:
        response = requests.get(proxy_url, params={'api_key': SCRAPEOPS_API_KEY, 'url': base_url}, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find product containers (adjust this based on Amazon's HTML structure)
        product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})

        product_details = []
        for container in product_containers:
            # Check if title exists
            title_elem = container.find('span', class_='a-size-medium a-color-base a-text-normal')
            title = title_elem.text.strip() if title_elem else "Title not available"

            # Check if price exists
            price_elem = container.find('span', class_='a-offscreen')
            price = price_elem.text.strip() if price_elem else "Price not available"

            # Check if rating exists
            rating_elem = container.find('span', class_='a-icon-alt')
            rating = rating_elem.text.strip() if rating_elem else "Rating not available"

            # Check if image exists (use 'src' attribute instead of text)
            image_elem = container.find('img', class_='s-image')
            image = image_elem['src'] if image_elem else "Image not available"

            # Check if URL exists
            url_elem = container.find('a', class_='a-link-normal s-no-outline')
            url = 'https://www.amazon.com' + url_elem['href'] if url_elem else "URL not available"

            product_details.append({
                'title': title,
                'price': price,
                'rating': rating,
                'image': image,
                'url': url
            })

        return product_details

    except requests.exceptions.RequestException as e:
        return []  # Return an empty list in case of error


def recommend_best_product(products):
    best_product = None
    best_score = float('-inf')  # Start with a very low score

    for product in products:
        price_str = product['price']
        if price_str.startswith('$'):
            price_str = price_str[1:]  # Remove dollar sign
        price_str = price_str.replace(',', '')  # Remove commas

        # Debug: Print the price string
        print(f"Checking product: {product['title']}, Price String: '{price_str}'")

        if price_str.replace('.', '', 1).isdigit():  # Check if it's a valid number
            price = float(price_str)
        else:
            print(f"Invalid price for {product['title']}: {price_str}")  # Debug: Print the invalid price
            continue  # Skip this product if the price is invalid

        rating_str = product['rating']
        if rating_str.replace('.', '', 1).isdigit():  # Handle missing ratings
            rating = float(rating_str)
        else:
            print(f"Invalid rating for {product['title']}: {rating_str}")  # Debug: Print the invalid rating
            continue  # Skip this product if the rating is invalid

        # Calculate the score
        score = rating / price  # Score based on rating to price ratio
        if score > best_score:  # Find the product with the best score
            best_score = score
            best_product = product

    return best_product
