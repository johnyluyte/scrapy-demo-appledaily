# -*- coding: utf-8 -*-

import scrapy

# 在這邊定義預先設計的 Item 物件來收藏之後 extracted 的 data，確保抓到資料型態都符合預期
# http://doc.scrapy.org/en/latest/topics/items.html

class AppleDailyItem(scrapy.Item):
    # 建立你預期之後會抓到的東西
    title = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    time = scrapy.Field()

