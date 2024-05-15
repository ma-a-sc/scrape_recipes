import logging
from typing import Iterable

import scrapy
from scrapy import Spider, Request
from scrapy.loader import ItemLoader

from ..items import ScrapeCookBooksDotComItem
logger = logging.getLogger(__name__)
logging.basicConfig(filename="cookbooks_logs.txt", encoding="utf-8", level=logging.WARNING)


class ScrapecookbooksdotcomSpider(Spider):
    name = "scrape_cook_books_dot_com"
    allowed_domains = ["cookbooks.com"]
    start_urls = ["https://cookbooks.com/Recipe-Details.aspx?id=1"]

    def start_requests(self) -> Iterable[Request]:
        #for index in range(1, 1086400):
        for index in range(1, 1000):
            yield scrapy.Request(url="https://cookbooks.com/Recipe-Details.aspx?id={}".format(index), callback=self.parse)

    def parse(self, response):

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

        # this is not working as I expect it
        try:
            problem = response.xpath('//td[@valign="top" and @bgcolor="#FFFFFF"]')[0].get()
            found = "Could NOT Open Recipe Page" in problem
            if found:
                logger.warning(f"No recipe for page found: {response.url}")
                return
        except IndexError:
            pass

        item = ItemLoader(item=ScrapeCookBooksDotComItem(), response=response)
        item.add_value("url", response.url)
        item.add_xpath("title", '//p[@class="H2"]')
        item.add_xpath("ingredients", '//table[@width="100%" and @border="1px" and @cellspacing="0" and @cellpadding="10"]')
        item.add_xpath("directions", '//table[@width="100%" and @border="1px" and @cellspacing="0" and @cellpadding="10"]')
        item.add_xpath("star_rating", '//div[@id="star-rating"]')
        item.add_xpath("total_votes", '//div[@id="star-rating"]')
        return item.load_item()




