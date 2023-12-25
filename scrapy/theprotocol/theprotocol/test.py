from playwright.sync_api import sync_playwright
import time

class Offer:
    def __init__(self,id, title, price, link):
        self.id = id
        self.title = title
        self.price = price
        self.link = link

    @staticmethod
    def from_element(element):
        title = element.locator('h6').inner_text()
        price = element.locator('p[data-testid="ad-price"]').inner_text().splitlines()[0]
        link = element.locator('a').get_attribute('href')
        if link.startswith('/'):
            link = 'https://www.olx.pl' + link
        return Offer(title, price, link)


def scrape(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector('#__next > div.MuiBox-root.css-1v89lmg > div.css-c4vap3 > div > div.MuiBox-root.css-1fmajlu > div > div > div:nth-child(2)')

        # __next > div.MuiBox-root.css-1v89lmg > div.css-c4vap3 > div > div.MuiBox-root.css-1fmajlu > div > div
        # __next > div.MuiBox-root.css-1v89lmg > div.css-c4vap3 > div > div.MuiBox-root.css-1fmajlu > div > div > div:nth-child(2)
        time.sleep(20)
        print('elo')

        offers_elements = page.locator('#__next > div.MuiBox-root.css-1v89lmg > div.css-c4vap3 > div > div.MuiBox-root.css-1fmajlu > div > div > div:nth-child(2) > div > div:nth-child(2) > div > div > div > a').all()
        print(f"Number of offers: {len(offers_elements)}")
        # for element in offers_elements:
        #     title = element.locator('#offer-title').inner_text()
        #     print(title)


if __name__ == "__main__":
    # search_value = input("Enter your search: ")
    # url = f"https://www.olx.pl/oferty/q-{search_value}/"
    # offers = scrape_olx(url)
    # display_offers(offers)

    scrape('https://justjoin.it')
