# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TheprotocolItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    salary_range = scrapy.Field()
    must_have_main = scrapy.Field()
    nice_tohave_main = scrapy.Field()

    # detailed_list = JobHarvester.Field()
