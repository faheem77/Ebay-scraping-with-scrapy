# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EbayProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title =scrapy.Field()
    Price = scrapy.Field()
    Description = scrapy.Field()
    Images = scrapy.Field()
    Category = scrapy.Field()
    SubCategory= scrapy.Field()
    SellerName= scrapy.Field()
    Product_Page_URL= scrapy.Field()