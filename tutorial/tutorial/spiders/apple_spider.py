# -*- coding: utf-8 -*-
# 本範例修改字 Scrapy 官方 Tutorial，更多資訊請參閱
# http://doc.scrapy.org/en/latest/intro/tutorial.html

import scrapy

# 1. 記得 import 進你預先設計的 Item 物件來收藏 extracted 的 data，確保抓到資料型態都符合預期
from tutorial.items import AppleDailyItem

class AppleDailySpider(scrapy.Spider):

# 2. 設定這個 spider 的名稱，必須獨一無二，下指令執行時使用
    # $ scrapy crawl (spider名稱)
    # e.g $ scrapy crawl apple
    name = "apple"

# 3. 指定網域
    allowed_domains = ["appledaily.com.tw"]

# 4. 指定起始的 URL，最先會從這些 URL 開始爬
    start_urls = [
    # 記得加上 http:// 表明要用 http protocol
        "http://www.appledaily.com.tw/realtimenews/section/new"
    # 除了手動加上 URL 之外，也可以用其他方式例如從 Database 中取出 URLs
    # http://stackoverflow.com/questions/20118753/python-scrapy-populate-start-urls-from-mysql
    # 除了起始 URL 外，Scrapy 也可「從目標頁面找出有興趣的連結，並將該連結放入下個目標來爬」，請參見
    # http://doc.scrapy.org/en/latest/intro/tutorial.html#following-links
    ]

# 5. 實作 parse(self, response)
    # 當 scrapy 發出個 request 收到 response 時，就會呼叫這個 callback function，並丟入 response
    # response.body 基本上可以視為 html DOM，但是 scrapy 在 crawl 時不會執行 javascript，
    # 所以 response.body 跟 browser 看到的 DOM 可能會有微妙的不同
    # http://doc.scrapy.org/en/latest/topics/firefox.html
    def parse(self, response):
# 6. 使用 xpath 來描述你想抓的東西(HTML node, DOM)
        # xpath 可做 nested 操作，如下面範例
        for my_trget_dom in response.xpath('//*[@id="maincontent"]//ul[contains(@class,"slvl")]/li'):
        # ul[contains(@class,"slvl")] 是一個不完美的 xpath 比對 class 的 workaround 解法，實際使用上應避免：
        # http://stackoverflow.com/questions/1390568/how-to-match-attributes-that-contain-a-certain-string

# 7. 使用預先設計的 AppleDailyItem 元件來接收資料，確保抓到資料型態都符合預期
            item = AppleDailyItem()

            # 使用 xpath() 抓取想要的資訊，記得使用 extract()
            item['title'] = my_trget_dom.xpath('a/h1/font/text()').extract()
            # 錯誤
            # item['url'] = my_trget_dom.xpath('/a/@href').extract()
            # 正確
            item['url'] = my_trget_dom.xpath('a/@href').extract()
            item['category'] = my_trget_dom.xpath('a/h2/text()').extract()
            item['time'] = my_trget_dom.xpath('a/time/text()').extract()

            # 此時出的字串會是 Unicode 格式，例如：
            # [u'\u570b\u969b']
            # 如需要轉成人類看得懂的格式檢視，可用 encode() 來指定其編碼
            # if(len(item['category'])):
            #     print item['category'][0].encode('UTF-8').rstrip()
            # 就會將上述字串以 UTF-8 編碼，轉成：
            # [國際]
            # 或者其實你可以直接用下面方式輸出到 json，然後用支援 Unicode 的編輯器打開來看
            # 例如 Sublime Text 配合其 pretty json 外掛就還不錯用

# 8. 基本上這樣就抓完 data 了，接下來可以直接對 data 做處理，但是我們通常會將剩下的工作丟給其他程式處理
            # 我們可以將檔案以 json, csv, xml 等方式存進本地端、FTP、cloud 等等，讓其他程式使用
                # http://doc.scrapy.org/en/latest/topics/feed-exports.html
            # 也可以透過 pipeline 方式，將這些 data 丟給其他元件處理
                #

            # 一個最簡單的方式是在這邊使用 yield item，接著在 console 執行時加上 -o output_filename
            # yield item
            # e.g. crapy crawl apple -o myOutput.json

            # 這邊我們示範用 pipeline 丟給 pipeline.py 做處理
            # 接下來請參閱 pipeline.py
            yield item
