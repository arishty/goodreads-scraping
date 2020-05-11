# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoodreadsItem(scrapy.Item):
    genre = scrapy.Field()
    book_title = scrapy.Field()
    author = scrapy.Field()
    rating_avg = scrapy.Field()
    ratings_amt = scrapy.Field()
    reviews_amt = scrapy.Field()
    price = scrapy.Field()
    pages_amt = scrapy.Field()
    publish_date = scrapy.Field()



