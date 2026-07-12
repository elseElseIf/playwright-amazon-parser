from playwright.sync_api import sync_playwright
import time

class AmazonSellerParce:
    def __init__(self, keyword: str):
        self.keyword = keyword
        self.list_seller_name = []

    def __page_down(self):
        previous_height = 0

        while True:
            self.page.mouse.wheel(0, 5000)
            self.page.wait_for_timeout(2000)
            current_height = self.page.evaluate("document.documentElement.scrollHeight")

            if current_height == previous_height:
                break

            previous_height = current_height

    def __get_seller_name(self, url:str):
        self.page2 = self.context.new_page()
        self.page2.goto(url=url)
        self.page2.wait_for_selector("#productTitle")

        seller = self.page2.query_selector(
            "div.offer-display-feature-text.odf-truncation-popover"
        )

        if seller:
            print("Seller:", seller.inner_text())
        else:
            print("Seller not found")


    def __get_links(self):
        self.page.wait_for_selector('div[data-component-type="s-search-result"]')
        self.__page_down()
        cards = self.page.query_selector_all('div[data-component-type="s-search-result"]')

# 9 - is a 10 sellers cards
        for count, card in enumerate(cards):
            if count > 9: break
            link = card.query_selector("a.s-line-clamp-4")

            if link:
                href = link.get_attribute("href")

                if href:
                    url = "https://www.amazon.pl" + href
                    self.__get_seller_name(url=url)

    def parce(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless = False)
            self.context = browser.new_context()
            self.page = self.context.new_page()
            self.page.goto("https://www.amazon.pl/")
            self.page.get_by_placeholder("Szukaj na Amazon.pl").type(self.keyword, delay=0.3)
            self.page.query_selector("input[type='submit']").click()
            self.__get_links()
            time.sleep(5)

if __name__ == "__main__":
    AmazonSellerParce("Bóbr").parce()
    time.sleep(5)