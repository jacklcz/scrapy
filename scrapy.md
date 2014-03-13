## python 爬虫框架 scrapy ##

**介绍**

Scrapy是用Python开发的一个快速,高层次的web抓取框架，用于抓取web站点并从页面中提取结构化的数据。Scrapy用途广泛，可以用于数据挖掘、监测和自动化测试。

</br></br>
**概述及其组件**

<img src="http://jbcdn1.b0.upaiyun.com/2014/03/scrapy.png" alt="">

</br></br>
**start**
<li>http://scrapy.org/download/python</li>
<li>easy_install Scrapy</li>
<li>pip install Scrapy</li>
 

</br></br>
```
**Command**
  **fetch**           Fetch a URL using the Scrapy downloader 
  **runspider**     Run a self-contained spider (without creating a project)
  **settings**       Get settings values
  **shell**            Interactive scraping console
  **startproject**  Create new project
  **version**        Print Scrapy version
  **view**          Open URL in browser, as seen by Scrapy
```
</br></br>
**scrapy shell 工具使用**
<li> scrapy shell url</li>

```
[s] Available Scrapy objects
[s]   item       {}
s]   request    <GET http://www.jyeoo.com/math/ques/search>
[s]   response   <200 http://www.jyeoo.com/math/ques/search>
[s]   sel        <Selector xpath=None data=u'<html lang="zh-cn"><head><meta http-equi'>
[s]   settings   <CrawlerSettings module=None>
[s]   spider     <BaseSpider 'default' at 0x2d1ebd0>
[s] Useful shortcuts:
[s]   shelp()           Shell help (print this help)
[s]   fetch(req_or_url) Fetch request (or URL) and update local objects
[s]   view(response)    View response in a browser
fetch:
scrapy.http import Request(url)
view(response)
```


</br></br>
**spiders**
<li>spiders定义从哪个网站,包括如何执行(即爬行)、以及如何从页面中提取结构化数据。</li>

<li>我们的spiders首先继承BaseSpider，然后定义爬虫标识(即name)、start_urls[] ，
start_urls是定义最开始需要爬取的页面。</li>

<li>通过Request(url)后的回调函数，来处理、解析响应。</li>

<li>结构化数据，通过pipelines处理。(保存)</li>

<li>常用的spiders(CSVFeedSpider SitemapSpider  XMLFeedSpider)</li>



</br></br>
**xpath**
<li>提供xpath的方式比较强大。</li>

<li>提供两个XPath选择器,HtmlXPathSelector和XmlXPathSelector，提供如下方法：</li>

<li>select(xpath): 返回一个相对于当前选中节点的选择器列表（一个XPath可能选到多个节点）</li>

<li>extract(): 返回选择器（列表）对应的节点的字符串（列表）</li>

<li>re(regex): 返回正则表达式匹配的字符串（分组匹配）列表</li>


</br></br>

**Define the data you want**</br></br>
```
from scrapy.item import Item, Field
class TorrentItem(Item):
url = Field()
name = Field()
description = Field()
size = Field()
```

**Downloader Middlewares**    http://doc.scrapy.org/en/latest/topics/downloader-middleware.html

```
CookiesMiddleware：是否向web server发送cookie
DefaultHeadersMiddleware：将所有request的头设置为默认模式
DownloadTimeoutMiddleware：设置request的timeout
HttpAuthMiddleware：对来自特定spider的request授权
HttpCacheMiddleware：给request&response设置缓存策略
HttpProxyMiddleware：给所有request设置http代理
RedirectMiddleware：处理request的重定向
MetaRefreshMiddleware：根据meta-refresh html tag处理重定向
RetryMiddleware：失败重试策略
RobotsTxtMiddleware：robots封禁处理
UserAgentMiddleware：支持user agent重写
```

**Logging**
```
CRITICAL - for critical errors
ERROR - for regular errors
WARNING - for warning messages
INFO - for informational messages
DEBUG - for debugging messages
 self.log('msg',level=log.INFO)
```      


**如何增量**</br>
目前没有官方方案，介绍两个非官方的方法:</br>
(1). 在pipeline的open_spider时读取所有item里面的url，做成一个parsed_urls的list，在rule的process_link中过滤掉这些已经下载的url。

(2)在item中增加Url字段。item['Url'] = response.url,然后在数据端把储存url的column设置成unique。之后在python代码中捕获数据库commit时返回的异常，忽略掉或者转入log中都可以。(适合小规模的爬虫)



**note**</br>


https://github.com/jacklcz/scrapy

```
scrapy crawl myspider -a category=electronics
Spiders receive arguments in their constructors:

class MySpider(Spider):
    name = 'myspider'
    def __init__(self, category=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.example.com/categories/%s' % category]

```

python -m SimpleHTTPServer 8787

http://doc.scrapy.org/en/latest/topics/images.html 图片下载管道


