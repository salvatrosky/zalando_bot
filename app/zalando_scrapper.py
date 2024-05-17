from decimal import Decimal
import requests
from bs4 import BeautifulSoup
from app.telegram_handler import send_message
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


async def test_scraper(product):
    from app.models import Product

    new_price = fetch_price_span(product.link)
    last_price = product.last_price

    if new_price and new_price != str(product.last_price):
        new_price = Decimal(new_price)
        logger.info(f"Price changed from {product.last_price} to {new_price}")
        try:
            logger.info(
                f"Updating product with user_id: {product.user_id}, last_price: {new_price} link {product.link}")
            await sync_to_async(Product.objects.filter(link=product.link).update)(last_price=new_price, name="PRODUCT NAME")
            logger.info("Product created successfully")
        except Exception as e:
            logger.error(f"Error Updating product: {e}")

        chat_id = await sync_to_async(lambda: product.user.chat_id)()
        message = f'Price updated: {product.link} from €{last_price} to €{new_price}'
        await send_message(chat_id=chat_id, message=message)

    return new_price
