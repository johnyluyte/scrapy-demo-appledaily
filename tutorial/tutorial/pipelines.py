# -*- coding: utf-8 -*-

import re
import MySQLdb

# 1. 請先到 settings.py 將你要用的 pipeline function 加進去 ITEM_PIPELINES = {} 裡面

class AppleDailyPipeline(object):
    def process_item(self, item, spider):
        if(len(item['title'])!=0):
            # 將資料轉為 UTF-8 格式
            # 這裏只是為了讓 demo print 時比較漂亮，實際上不需現在做轉換，要儲存資料時再轉即可
            # http://blog.chunnorris.cc/2015/04/unicode.html
            title =  item['title'][0].encode('UTF-8')
            url =  item['url'][0].encode('UTF-8')
            category = item['category'][0].encode('UTF-8')
            time =  item['time'][0].encode('UTF-8')

# 2. 對資料作處理
            # 蘋果的點閱率記錄在其標題之後用括號內，例如下面這則新聞
            # 拿不到發票存根聯　奧客拍桌摔盤(920)
            # 的點閱率就是 920
            # 我們使用內建的 re 函式庫來處理 Regex
            regex_pattern = r"\((\d+)\)"
            # 這邊使用 regex 的語法，有興趣自己上網查
            clicks = re.findall(regex_pattern, title)
            # 因 re.findall 回傳 strings[]，這裏我們只要第一個 element
            clicks = clicks[0]

            # 接著也將 title 做處理
            title = re.findall(r"(.+)\(", title)[0]
            # 處理 url
            url = "http://www.appledaily.com.tw/realtimenews/section/new" + url

            print "\033[1;33m [AppleDailyPipeline]"
            print title
            print url
            print category
            print time
            print clicks
            print "\033[m"

            self.upload_to_database(title, url, category, time, clicks)

        return item


# 3. 使用 MySQLdb 函式庫上傳至資料庫
# 如果沒有 MySQLdb 的話請先安裝
# http://www.tutorialspoint.com/python/python_database_access.htm
# $ pip install MySQL-python
# 記得使用 virtualenv，如果還沒用的話。雖然現在才講可能有點晚 XD
    def upload_to_database(self, title, url, category, time, clicks):
        conn = MySQLdb.connect(
            # 註：請把這邊的資料改成你的資料庫設定，我的資料庫有擋住外來 IP 所以你會連不上來
            host = "66.147.240.164",
            db = "chunnorr_apple",
            user = "chunnorr_apple",
            passwd = "5566cannotdie",
            charset = "utf8",
            use_unicode = True,
            )
        cursor = conn.cursor()
        cursor.execute(
            # 插入剛剛我們抓取完成並處理過的頻果日報資料
            "INSERT INTO `table_news` VALUES('" + title + "','" + url + "','" + category + "','" + time + "','" + clicks + "');"
            )
        conn.close()

# 以這個例子來講，這個程式效率很差，因為 DB 作 I\O 的 overhead 很大，我們應該盡可能的把所有資料都處理完後，使用一次 DB I/O 全部處理好，而非像這樣一個一個作 DB I/O。
# 但這裏只是展示 scrapy 的 pipeline 及用法，就不深究。

