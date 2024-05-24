from __future__ import absolute_import
import json
import logging
from typing import Iterable

from scrapy.loader import ItemLoader
from scrapy import Spider, Request
from requests import request

from ..items import FoodDotComItem

logger = logging.getLogger(__name__)
logging.basicConfig(filename="cookbooks_logs.txt", encoding="utf-8", level=logging.WARNING)


class ScrapecookbooksdotcomSpider(Spider):
    name = "scrape_food_dot_com"
    allowed_domains = ["food.com"]
    start_urls = ["https://api.food.com/services/mobile/fdc/search/sectionfront?pn={}&recordType=Recipe&collectionId=17"]

    max_recipes = 0

    def open_spider(self, spider):
        initial_data = request("get", self.start_urls[0].format(1))

        json_data = json.loads(initial_data.text)
        self.max_recipes = int(json_data["response"]["totalResultsCount"])

        return spider

    def start_requests(self) -> Iterable[Request]:
        index = 1
        while True:
            data = request("get", self.start_urls[0].format(index))

            if data.status_code != 200:
                logger.warning(f"Request failed with status code {data.status_code} for url {data.url}")
                continue

            json_data = json.loads(data.text)

            if int(json_data["response"]["parameters"]["offset"]) >= self.max_recipes - 10:
                self.close(self, reason="Finished!")

            index += 1
            print(index)
            for result in json_data["response"]["results"]:
                yield Request(result["record_url"], callback=self.parse, meta={"data": result})

    def parse(self, response):

        meta_data = response.meta

        if response.status != 200:
            match response.status:
                case 401:
                    logger.warning(f"This page was not accessed due to not beeing authorizde: {response.url}")
                    return
                case 404:
                    logger.warning(f"This page is not available: {response.url}")
                    return
                case 408:
                    logger.warning(f"Timeout while trying to parse: {response.url}")
                    return
                case 500:
                    logger.warning(f"Server error while trying to parse: {response.url}")
                    return
                case _:
                    logger.warning(f"Unknown error while trying to parse: {response.url}")

        item = ItemLoader(item=FoodDotComItem(), response=response)
        item.add_value("title", meta_data["data"]["main_title"])
        item.add_value("main_rating_mapping", meta_data["data"]["main_rating_mapping"])
        item.add_value("main_rating", meta_data["data"]["main_rating"])
        item.add_value("main_num_ratings", meta_data["data"]["main_num_ratings"])
        item.add_value("url", meta_data["data"]["record_url"])
        item.add_value("topic_name", meta_data["data"]["topic_name"])
        item.add_value("number_of_steps", meta_data["data"]["num_steps"])
        item.add_value("recipe_preptime", meta_data["data"]["recipe_preptime"])
        item.add_value("recipe_cooktime", meta_data["data"]["recipe_cooktime"])
        item.add_value("recipe_total_time", meta_data["data"]["recipe_totaltime"])

        item.add_xpath("total_number_of_ingredients", '//div[@class="facts__item svelte-1dqq0pw"]')
        item.add_xpath("servings", '//div[@class="facts__item svelte-1dqq0pw"]')
        item.add_xpath("directions", '//section[@class="layout__item directions svelte-1dqq0pw"]')
        item.add_xpath("ingredients", '//ul[@class="ingredient-list svelte-1dqq0pw"]')

        return item.load_item()



