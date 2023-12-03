# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NofluffItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()

    must_have_graphical = scrapy.Field()
    nice_to_haves_graphical = scrapy.Field()

    requirements_list = scrapy.Field()
    nice_tohaves_list = scrapy.Field()


