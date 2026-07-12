from playwright.sync_api import sync_playwright
import time

class AmazonSellerParce:
    def __init__(self, keyword: str):
        self.keyword = keyword
        self.list_seller_name = []

    def __get_links(self):
        self.page.wait_for_selector(
            'div[data-component-type="s-search-result"]'
        )

        cards = self.page.query_selector_all(
            'div[data-component-type="s-search-result"]'
        )

        for card in cards:
            link = card.query_selector("a.s-line-clamp-4")

            if link:
                href = link.get_attribute("href")

                if href:
                    url = "https://www.amazon.pl" + href

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