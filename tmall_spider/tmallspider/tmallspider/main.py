#-*- coding: UTF-8 -*- 

u'''
@author: lcz
@date: 2014-3-10
'''
import subprocess

if __name__ == '__main__':
    command = 'scrapy runspider .\\spiders\\tmall_spider.py --logfile=tmall_spider.log'
#    command = 'scrapy runspider .\\spiders\\tmall_spider.py'
    command = 'scrapy runspider .\\spiders\\soudian_spider.py --logfile=tmall_spider.log'
    subprocess.call(command, shell=True)
