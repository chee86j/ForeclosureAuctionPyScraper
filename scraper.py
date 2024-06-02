import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    response = requests.get(url)
    return response.text if response.status_code == 200 else None

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Modify below to match the specific data you need
    auctions = soup.find_all('div', class_='auction')
    data = []
    for auction in auctions:
        title = auction.find('h1').text.strip()
        price = auction.find('span', class_='price').text.strip()
        data.append({'title': title, 'price': price})
    return data

def main(url):
    html = fetch_page(url)
    if html:
        data = parse_page(html)
        # Call your database function to save data
        print(data)

if __name__ == '__main__':
    main('http://example.com/foreclosures')
