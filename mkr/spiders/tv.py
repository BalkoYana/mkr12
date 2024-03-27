import scrapy
from bs4 import BeautifulSoup
from mkr.items import MkrItem,ShopItem

class TvSpider(scrapy.Spider):
    name = "tv"
    allowed_domains = ["hotline.ua"]
    start_urls = [f"https://hotline.ua/ua/av/televizory/?p={page}" for page in range(1, 5)]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        main_container = soup.find(name="div", class_="list-body__content")
        if main_container:
            items = main_container.find_all(class_="list-item")
            for item in items:
                # Знаходимо назву
                a = item.find("a")
                name = a.find(string=True, recursive=False)

                # url
                url = f"https://hotline.ua{a.get('href')}"
                price_element = item.find(class_="list-item__value-price")
                price = price_element.text.strip() if price_element else "Ціна недоступна"

                image_url = item.find(name="img").get("src")

                yield MkrItem(
                    name=name,
                    price=price,
                    url=url,
                    image_urls=[f"https://hotline.ua{image_url}"]
                )
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_shop,
                    meta={
                        "nameshop": name,
                    }

                )

    def parse_shop(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        shop_items = soup.select(".list > a")[:5]  # Отримуємо лише перші 5 елементів
        for shop in shop_items:
            shop_name = shop.find(string=True, recursive=False)
            print(f"7777777777777777777777777777777777777777777777777777777777777{shop_name}")
            yield ShopItem(name=shop_name)


        pass
