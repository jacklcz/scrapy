#-*-coding:utf-8-*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

# Standard Python library imports
# 3rd party modules

from custom_settings import *
from items import GoodsItem
from pymongo.connection import MongoClient
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from tmallspider.items import PaginationItem, GoodsItem
from tmallspider.soudian_items import ShopItem, ShopDetailItem
from twisted.enterprise import adbapi
import MySQLdb.cursors
import datetime
import os
import pymongo
import traceback

class SingleMongodbPipeline(object):
    u"""
    @summary: save the data to mongodb.
    """
    MONGODB_SERVER = "localhost"
    MONGODB_PORT = 27017
    MONGODB_DB = "books_fs"

    def __init__(self):
        u"""
        The only async framework that PyMongo fully supports is Gevent.
        
        Currently there is no great way to use PyMongo in conjunction with Tornado or Twisted. 
        PyMongo provides built-in connection pooling, 
        so some of the benefits of those frameworks can be achieved 
        just by writing multi-threaded code that shares a MongoClient.
        """
        self.client = None
        self.db = None

    def open_spider(self, spider):
        u'''
        @summary: spider开启时调用
        '''
        self.MONGODB_SERVER = SingleMONGODB_SERVER
        self.MONGODB_PORT = SingleMONGODB_PORT
        self.MONGODB_DB = SingleMONGODB_DB

        try:
            self.client = MongoClient(self.MONGODB_SERVER, self.MONGODB_PORT)
            self.db = self.client[self.MONGODB_DB]
        except Exception as e:
            print log.ERROR("ERROR(SingleMongodbPipeline): %s" % (str(e),))
            traceback.print_exc()

    def process_item(self, item, spider):
        if(not isinstance(item, GoodsItem)):
            return item

        result = self.db['goodsitems'].insert(dict(item))
#        item["mongodb_id"] = str(result)
#
#        log.msg("Item %s wrote to MongoDB database %s/book_detail" %
#                (result, self.MONGODB_DB), level=log.DEBUG, spider=spider)
        return item


    def close_spider(self, spider):
        u'''
        @summary: spider关闭时调用
        '''
        if(self.client):
            self.client.close()


class TmallSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline(object):
    def __init__(self):
        self.item_ids = set()

    def process_item(self, item, spider):
        if(not isinstance(item, GoodsItem)):
            return item

        id = item.get('id', None)
        if(not id):
            raise DropItem("Not goodsitem: %s" % item)

        if id in self.item_ids:
            raise DropItem("Duplicate item_id found: %s" % item)
        else:
            self.item_ids.add(id)
            return item

class CleanGoodsItemPipeline(object):
    def process_item(self, item, spider):
        u'''
        @summary: 处理物品信息数据，字符串还是保持Unicode编码
        '''

        if(not isinstance(item, GoodsItem)):
            return item

        id = item.get('id', None)
        if(not id):
            raise DropItem("Not goodsitem: %s" % item)
        for key, value in item.items():
            item[key] = ''.join(value).strip()

        item['id'] = int(item['id'])
        item['sales_amount_text'] = item['sales_amount_text']\
            .replace('''<em>''', '').replace('''</em>''', '')
        item['price_value'] = float(item['price_value'])

        item['table_name'] = item.get_table_name()

        return item

class CleanShopsItemPipeline(object):
    def process_item(self, item, spider):
        u'''
        @summary: 处理物品信息数据，字符串还是保持Unicode编码
        '''

        if(not isinstance(item, ShopItem) and not isinstance(item, ShopDetailItem)):
            return item
        item['id'] = int(''.join(item['id']))
        item['shop_name'] = ''.join(item['shop_name']).replace(' ', '').replace('-', '')
        item['shop_url'] = ''.join(item['shop_url'])
        print 'item', item
        return item

class FilePipeline(object):
    def __init__(self):
        if(os.path.exists(FILEPIPELINE_GOODSFILE_PATH)):
            os.remove(FILEPIPELINE_GOODSFILE_PATH)
        if(os.path.exists(FILEPIPELINE_SHOPSFILE_PATH)):
            os.remove(FILEPIPELINE_SHOPSFILE_PATH)
        if(os.path.exists(FILEPIPELINE_SHOPDETAILSFILE_PATH)):
            os.remove(FILEPIPELINE_SHOPDETAILSFILE_PATH)

        self.file_goods = open(FILEPIPELINE_GOODSFILE_PATH, 'a')
        self.file_shops = open(FILEPIPELINE_SHOPSFILE_PATH, 'a')
        self.file_shopdetails = open(FILEPIPELINE_SHOPDETAILSFILE_PATH, 'a')

        self.title_flag = False

    def process_item(self, item, spider):
        if(isinstance(item, GoodsItem)):
            if(not self.title_flag):
                self.file_goods.write('\t'.join(item.keys()) + '\n')
                self.title_flag = True

            for key, value in item.items():
                if(key in ['id', 'price_value' ]):
                    self.file_goods.write(str(key) + '\t' + str(str(value) + '\n'))
                    continue
                self.file_goods.write(str(key) + '\t' + str(value.encode('utf8') + '\n'))

        elif(isinstance(item, ShopDetailItem)):
            for key, value in item.items():
                if(key in ['id']):
                    self.file_shopdetails.write(str(key) + '\t' + str(str(value) + '\n'))
                    continue
                self.file_shopdetails.write(str(key) + '\t' + str(value.encode('utf8') + '\n'))

        elif(isinstance(item, ShopItem)):
            for key, value in item.items():
                if(key in ['id']):
                    self.file_shops.write(str(key) + '\t' + str(str(value) + '\n'))
                    continue
                self.file_shops.write(str(key) + '\t' + str(value.encode('utf8') + '\n'))
        else:
            return item

    def __delete__(self):
        self.file_goods.close()
        self.file_shops.close()
        self.file_shopdetails.close()





