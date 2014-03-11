#-*- coding: UTF-8 -*- 

u'''
@author: Administrator
@date: 2013-5-5
'''

import re
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.utils.url import urljoin_rfc
from tmallspider.items import PaginationItem, GoodsItem
from tmallspider.soudian_items import ShopItem, ShopDetailItem
from urllib import quote

SHOP_NAME = u'宁莎'

class SoudianSpider(BaseSpider):
    name = "soudianspider"
#    allowed_domains = ["taobao.com","tmall.com"]
    start_urls = [
        "http://soudian.taobao.com/"
        ]

    def __init__(self):
        BaseSpider.__init__(self)

    def parse(self, response):
        u'''
        @summary: 通过关键字搜索店铺
        '''
#        print dir(response)
#        for attr in dir(response):
#            try:
#                if(attr in ['_body', '_cached_ubody', 'body']):
#                    continue
#                print '------', attr, getattr(response, attr)
#            except:
#                pass

        sname = SHOP_NAME.encode('gbk')
        url = "http://soudian.taobao.com/search.htm?q=" + quote(sname) + "&drt=1&spm=2005.0.0.3"
        yield Request(url, callback=self.parse_shops)

    def parse_shops(self, response):
        u'''
        @summary: 解析搜索出来的店铺
        '''
        hxs = HtmlXPathSelector(response)
        items_obj = hxs.select('//*[@id="J_SelectTag"]/div[1]/div/p/b[2]')
        total_shops = int(''.join(items_obj.select('.//text()').extract()))
        for i in range(1, total_shops + 1):
            try:
                item = ShopItem()
                shopname_path = '''//*[@id="J_Shop%d"]/dt/p/b/a''' % i
                items_obj = hxs.select(shopname_path)
                item['shop_name'] = items_obj.select('.//text()').extract()

                shopurl_path = '''//*[@id="J_ShopMsg%d"]/div[2]/a''' % i
                items_obj = hxs.select(shopurl_path)
                item['shop_url'] = items_obj.select('.//@href').extract()
                shop_url = ''.join(item['shop_url'])

                if(shop_url):
                    item['id'] = re.findall(r"shop_id=(\d+)", shop_url)
                yield Request(shop_url, meta={'item':item}, callback=self.parse_real_shop)
            except:
#                raise
                pass

    def parse_real_shop(self, response):
        u'''
        @summary: 解析真正的店铺名称，及其所有宝贝的首页链接
        '''
        # ------ 解析真正的店铺名称
        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        items_obj = hxs.select('/html/head/title')
        total_shops = ''.join(items_obj.select('.//text()').extract())
        item['shop_name'] = total_shops.replace(' ', '').replace('\n', '')
        item['shop_name'] = re.findall(r"-(.*)-", item['shop_name'])

        detailitem = ShopDetailItem()
        detailitem['id'] = item['id']
        detailitem['shop_name'] = item['shop_name']
        detailitem['shop_url'] = item['shop_url']

        # ------ 解析店铺所有宝贝的链接地址
        search_url_path = '''//a[@href and contains(@href,'search.htm') 
            and contains(text(), %s) and contains(text(),%s)]''' % (u'所有', u'宝贝')
        items_obj = hxs.select(search_url_path)
        search_urls = items_obj.select('.//@href').extract()
        search_urls = list(set(search_urls))
        temp = search_urls[0]
        for search_url in search_urls[1:]:
            if(len(search_url) < len(temp)):
                temp = search_url
        detailitem['search_url'] = temp

        # ------ 返回信息店铺信息
        yield detailitem
        yield item
        # ------ 解析店铺所有宝贝
        yield Request(search_url, meta={'detailitem':detailitem}, callback=self.parse_search_page)

    def parse_search_page(self, response):
        # ------ 将店铺所有宝贝的url放到管道
        yield self.parse_pages(response)

        # ------ 循环迭代各个页面url，获取所有的宝贝信息 
        hxs = HtmlXPathSelector(response)
        # 天猫商城提取所有宝贝页面链接
        urls = hxs.select('//*[@id="J_ShopSearchResult"]/div/div[2]/div[2]/a/@href').extract()
        if(not urls):
            # 天猫商城提取所有宝贝页面链接
            urls = hxs.select('//*[@id="J_ShopSearchResult"]/div/div[2]/div[10]/a/@href').extract()
        urls = list(set(urls))
        urls.append(response.url)
#        detailitem = response.meta['detailitem']
#        print '******', detailitem['search_url'], urls, '******'

        for url in urls:
            yield Request(url, callback=self.parse_goods)

    def parse_pages(self, response):
        u'''
        @summary: 将店铺所有宝贝的连接页面放到管道
        '''
        hxs = HtmlXPathSelector(response)

        items = []
        # 天猫商城提取所有宝贝页面链接
        pagination = hxs.select('//*[@id="J_ShopSearchResult"]/div/div[2]/div[2]/a')
        if(not pagination):
            # 淘宝商店提取所有宝贝页面链接
            pagination = hxs.select('//*[@id="J_ShopSearchResult"]/div/div[2]/div[10]/a')
        for page in pagination:
            try:
                item = PaginationItem()
                item['ns_class'] = page.select('@class').extract()
                item['ns_href'] = page.select('@href').extract()
                item['ns_page'] = page.select('text()').extract()
                if(not item['ns_href'] or 'next' in ''.join(item['ns_class'])):
                    continue
                items.append(item)
            except:
#                raise
                pass

#        detailitem = response.meta['detailitem']
#        print '------', detailitem['search_url'], items, '------'
        return items

    def parse_goods(self, response):
        u'''
        @summary: 获取宝贝信息
        @note: 发现有些店铺的所有宝贝解析不出来，原因是其xpath不太一样，后面修正
        '''
        hxs = HtmlXPathSelector(response)
        items = []
        items_objs = hxs.select('//*[@id="J_ShopSearchResult"]/div/div[2]/ul/li')

        for i, items_obj in enumerate(items_objs):
            try:
                url = "..//li[%d]" % (i + 1) + "/div"

                item = GoodsItem()
                item['pic_href'] = items_obj.select(url + '//div[1]/a/@href').extract()
                item['pic_data_ks_lazyload'] = items_obj.select(url + '//div[1]/a/img/@data-ks-lazyload').extract()
                item['pic_data_cdn_reduce_traffic'] = items_obj.select(url + '//div[1]/a/img/@data-cdn-reduce-traffic').extract()

                item['desc'] = items_obj.select(url + '//div[2]/a/text()').extract()

                item['price_type'] = items_obj.select(url + '//div[3]/span/text()').extract()
                item['price_symbol'] = items_obj.select(url + '//div[3]/s/text()').extract()
                item['price_value'] = items_obj.select(url + '//div[3]/strong/text()').extract()

                item['sales_amount'] = items_obj.select(url + '//div[4]/em/text()').extract()
                item['sales_amount_text'] = items_obj.select(url + '//div[4]/node()').extract()
                item['rating_c_value_no'] = items_obj.select(url + '//div[5]/span[1]/@title').extract()
                item['rating_href'] = items_obj.select(url + '//div[5]/span[2]/a/@href').extract()
                item['rating_title'] = items_obj.select(url + '//div[5]/span[2]/a/@title').extract()
                item['rating_text'] = items_obj.select(url + '//div[5]/span[2]/a/text()').extract()

                if(item['pic_href']):
                    item['id'] = re.findall(r"id=(\d+)&", str(item['pic_href'][0]))

                items.append(item)
            except:
#                raise
                pass
        return items




