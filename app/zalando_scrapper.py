import requests
from bs4 import BeautifulSoup


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
                    return span.text
    else:
        return None


def test_scraper(url):
    return fetch_price_span(url)
