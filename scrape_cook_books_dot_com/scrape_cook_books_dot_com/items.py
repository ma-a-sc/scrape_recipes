# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from itemloaders.processors import TakeFirst
from scrapy import Item, Field
from bs4 import BeautifulSoup


def get_title(title_section) -> str:
    cleaned_title = title_section[0].split('<font size="5">')[1].split('</font>')[0]
    cleaned_sub_title = title_section[0].split('<font size="4">')[1].split('</font>')[0].split("<i>")[0]
    return cleaned_title + "-" + cleaned_sub_title if cleaned_sub_title else cleaned_title


def get_ingredients(ingredients_and_directions_selector) -> str:
    bs = BeautifulSoup(ingredients_and_directions_selector[0], 'html.parser')
    return bs.find('p', {'class': 'H1'}).text


def get_stars(rating_section) -> int:
    if "No votes have been cast!" in rating_section[0]:
        return 0
    star_rating = rating_section[0].split("</strong>")[0].split("<strong>")[1]
    return int(star_rating)


def get_votes(rating_section_selector) -> int:
    if "No votes have been cast!" in rating_section_selector[0]:
        return 0

    votes = rating_section_selector[0].split("</strong>/5 stars")[1].split("</div>")[0].strip()
    votes = votes[1:len(votes)-1]

    votes = votes.strip("votes casted").strip()
    return int(votes)


def get_directions(directions_and_directions_selector) -> str:
    directions = directions_and_directions_selector[1]
    bs = BeautifulSoup(directions, 'html.parser')
    result = bs.find_all('p', {'class': 'H1'})

    return result[0].text.strip()


class ScrapeCookBooksDotComItem(Item):
    url = Field(serializer=str, output_processor=TakeFirst())
    title = Field(serializer=str, input_processor=get_title, output_processor=TakeFirst())
    ingredients = Field(serializer=str, input_processor=get_ingredients, output_processor=TakeFirst())
    directions = Field(serializer=str, input_processor=get_directions, output_processor=TakeFirst())
    # always out of five
    star_rating = Field(serializer=int, input_processor=get_stars, output_processor=TakeFirst())
    total_votes = Field(serializer=int, input_processor=get_votes, output_processor=TakeFirst())
