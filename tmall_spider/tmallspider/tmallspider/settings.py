#-*-coding:utf-8-*-
# Scrapy settings for tmallspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import os
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

BOT_NAME = 'tmallspiderspider'

SPIDER_MODULES = ['tmallspider.spiders']
NEWSPIDER_MODULE = 'tmallspider.spiders'

ITEM_PIPELINES = [
                'tmallspider.pipelines.CleanGoodsItemPipeline',
                'tmallspider.pipelines.CleanShopsItemPipeline',
                'tmallspider.pipelines.DuplicatesPipeline',
                'tmallspider.pipelines.FilePipeline',
#                'tmallspider.pipelines.SingleMongodbPipeline',
                ]


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tmallspider (+http://www.yourdomain.com)'

