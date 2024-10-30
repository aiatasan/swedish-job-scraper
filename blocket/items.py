# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BlocketItem(scrapy.Item):
    # define the fields for your item here like:

    url = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    date_added = scrapy.Field()
    date_expires = scrapy.Field()
    location = scrapy.Field()
    category = scrapy.Field()
    type = scrapy.Field()
    description = scrapy.Field()
