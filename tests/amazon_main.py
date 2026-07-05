from playwright.sync_api import sync_playwright
import time

class AmazonSellerParce:
    def __init__(self, keyword: str):
        self.keyword = keyword
        self.list_seller_name = []

    def __page_down(self):
        self.page.evaluate('''
                                const scrollStep = 200;
                                const scrollInterval = 100;
                                const scrollHeight = document.documentElement.scrollHeight;
                                let currentPosition = 0;
                                const interval = setInterval(() => {
                                    window.scrollBy(0, scrollStep);
                                    currentPosition += scrollStep;
                                
                                    if(currentPosition >= scrollHeight) {
                                        clearInterval(interval);
                                    }
                                }, scrollInterval);
                            ''')

    def __get_links(self):
        self.page.wait_for_selector(".rush-component")
        self.__page_down()
        self.page.wait_for_selector(f':text("Dalej")')

        links = self.page.query_selector_all(
            'div[data-component-type="s-search-result"]'
        )
        print(len(links))


    def parce(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless = False)
            self.context = browser.new_context()
            self.page = self.context.new_page()
            self.page.goto("https://www.amazon.pl/")
            self.page.get_by_placeholder("Szukaj na Amazon.pl").type(self.keyword, delay=0.3)
            self.page.query_selector("input[type='submit']").click()
            self.__get_links()
            time.sleep(10)

if __name__ == "__main__":
    AmazonSellerParce("Bóbr").parce()
    time.sleep(10)