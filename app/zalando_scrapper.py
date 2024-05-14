import requests
from bs4 import BeautifulSoup
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)

def fetch_price_span(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        main_content = soup.find(id="main-content")
        if main_content:
            price_spans = main_content.find_all('span')
            for span in price_spans:
                if "€" in span.text:
                    price = span.text.split()[0].replace(',', '.')
                    logger.info(f'Price found: {price}')
                    return price
    return None

async def test_scraper(url, user_id):
    from app.models import Product

    price = fetch_price_span(url)
    
    if price is not None:
        logger.info("Price is not None")
        try:
            # Log the parameters before creating the Product
            logger.info(f"Creating product with user_id: {user_id}, last_price: {price}")
            await sync_to_async(Product.objects.filter(link=url, user_id=user_id).update)(last_price=price, name="PRODUCT NAME")
            logger.info("Product created successfully")
        except Exception as e:
            # Log any exceptions that occur during the creation
            logger.error(f"Error creating product: {e}")
    else:
        logger.info("Price is None")
    
    return price
