# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobharvesterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NofluffItem(scrapy.Item):
    item_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()

    salary_range = scrapy.Field()
    must_have_main = scrapy.Field()
    nice_tohave_main = scrapy.Field()
    date = scrapy.Field()



class TheprotocolItem(scrapy.Item):
    item_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    salary_range = scrapy.Field()
    must_have_main = scrapy.Field()
    nice_tohave_main = scrapy.Field()
    date = scrapy.Field()


    # detailed_list = scrapy.Field()


class JustjoinitItem(scrapy.Item):
    item_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    salary_range = scrapy.Field()
    date = scrapy.Field()

