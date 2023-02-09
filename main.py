from config import DEFAULT_HEADERS
import requests
import time


class BinanceScraper:
    MAIN_URL = "https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=XRPUSDT"

    def __init__(self):
        self.all_prices = []
        self.current_price = ""

    def get_url(self):
        response = requests.get(self.MAIN_URL, headers=DEFAULT_HEADERS)
        return response

    def get_current_price(self, response):
        if response.status_code == 200:
            symbol = response.json().get("symbol")
            self.current_price = response.json().get("lastPrice")
            print(f"Current price of {symbol}: {self.current_price}")

    def get_max_price(self):
        self.all_prices.append(self.current_price)
        max_price = max(self.all_prices)
        for i in self.all_prices:
            if len(self.all_prices) > 2 and i < max_price:
                self.all_prices.remove(i)
            elif len(self.all_prices) > 2 and i == max_price:
                self.all_prices = list(set(self.all_prices))

    def check_price_drop(self):
        max_price = max(self.all_prices)
        if (float(max_price) - float(self.current_price)) >= (float(max_price) / 100):
            print(f"Цена упала на 1% и более ({max_price}-->{self.current_price})")

    def get_price_info(self):
        response = self.get_url()
        self.get_current_price(response)
        self.get_max_price()
        self.check_price_drop()

    def main(self):
        start_time = time.time()
        while True:
            if time.time() - start_time >= 3600:
                start_time = time.time()
                self.all_prices = []
            self.get_price_info()


if __name__ == "__main__":
    scraper = BinanceScraper()
    scraper.main()
