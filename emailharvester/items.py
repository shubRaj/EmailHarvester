# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EmailPhoneItem(scrapy.Item):
    """
        Store email and phone
    """
    domain = scrapy.Field()
    emails = scrapy.Field()
    phones = scrapy.Field()

