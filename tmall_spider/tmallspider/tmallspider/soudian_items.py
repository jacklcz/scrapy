#-*- coding: UTF-8 -*- 

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ShopItem(Item):
    u'''
    @summary: 店铺名称及连接
    '''
    # define the fields for your item here like:
    # name = Field()
    id = Field()
    shop_name = Field()
    shop_url = Field()

class ShopDetailItem(ShopItem):
    u'''
    @summary: 店铺名称及连接
    '''
    # define the fields for your item here like:
    # name = Field()
    search_url = Field()






