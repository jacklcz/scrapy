#-*- coding: UTF-8 -*- 

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class TmallspiderItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class PaginationItem(Item):
    # define the fields for your item here like:
    # name = Field()
    ns_class = Field()
    ns_href = Field()
    ns_page = Field()

class Goods(Item):
    u'''
    @summary: 商品数据基类
    '''
    # define the fields for your item here like:
    # name = Field()
    id = Field()
    pic_href = Field()
    pic_data_ks_lazyload = Field()
    pic_data_cdn_reduce_traffic = Field()

    desc = Field()

    price_type = Field()
    price_symbol = Field()
    price_value = Field()

    sales_amount = Field()
    sales_amount_text = Field()

    rating_c_value_no = Field()
    rating_href = Field()
    rating_title = Field()
    rating_text = Field()

class GoodsItem(Goods):
    u'''
    @summary: 商品数据
    '''
    table_name = Field()

    def get_table_name(self):
        return u'goodsitem'

