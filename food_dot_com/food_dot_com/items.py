# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst
from bs4 import BeautifulSoup


def get_directions(directions):
    soup = BeautifulSoup(directions[0], 'html.parser')
    directions = [li.get_text(strip=True) for li in soup.select('ul.direction-list.svelte-1dqq0pw li.direction.svelte-1dqq0pw')]
    return "-".join(directions)


def get_ingredients(ingredients):
    soup = BeautifulSoup(ingredients[0], 'html.parser')
    ingredients = [li.get_text(strip=False) for li in
                   soup.select('ul.ingredient-list.svelte-1dqq0pw li[style="display: contents"]')]
    ingredients = [ingredient.strip('\n').replace("\n", "").replace("  ", " ").replace("   ", " ") for ingredient in ingredients]
    return "-".join(ingredients)


def get_servings(servings):
    return int(servings[2].split('<span contenteditable="true" inputmode="numeric" class="value svelte-1o10zxc">')[1].split('</span>')[0])


def get_total_ingredients(total_ingredients):
    return int(total_ingredients[1].split('<dd class="facts__value svelte-1dqq0pw">\n ')[1].split('\n')[0].strip())


class FoodDotComItem(scrapy.Item):
    title = scrapy.Field(serializer=str, output_processor=TakeFirst())
    main_rating_mapping = scrapy.Field(serializer=int, output_processor=TakeFirst())
    main_rating = scrapy.Field(serializer=float, output_processor=TakeFirst())
    main_num_ratings = scrapy.Field(serializer=int, output_processor=TakeFirst())
    url = scrapy.Field(serializer=str, output_processor=TakeFirst())
    topic_name = scrapy.Field(serializer=str, output_processor=TakeFirst())
    number_of_steps = scrapy.Field(serializer=int, output_processor=TakeFirst())
    recipe_preptime = scrapy.Field(serializer=int, output_processor=TakeFirst())
    recipe_cooktime = scrapy.Field(serializer=int, output_processor=TakeFirst())
    recipe_total_time = scrapy.Field(serializer=int, output_processor=TakeFirst())
    servings = scrapy.Field(serializer=int, input_processor=get_servings, output_processor=TakeFirst())
    ingredients = scrapy.Field(serializer=str, input_processor=get_ingredients, output_processor=TakeFirst())
    total_number_of_ingredients = scrapy.Field(serializer=int, input_processor=get_total_ingredients, output_processor=TakeFirst())
    directions = scrapy.Field(serializer=str, input_processor=get_directions, output_processor=TakeFirst())