import requests
import json
import pandas as pd
import threading
from lxml import etree
from visualize_data import visualize_data

class DangDang_Spider():

    def __init__(self):
        self.url_model = "http://search.dangdang.com/?key={}&act=input&page_index={}"
        self.headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
        self.items_list = []

    def get_html(self,url):#获取网页html内容
        try:
            response = requests.get(url,headers=self.headers)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text
        except:
            print("There is something wrong!")
            return None

    def get_page_num(self,key):#获取最大页码
        try:
            response = requests.get(self.url_model.format(key,1), headers=self.headers)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            html = etree.HTML(response.text)
        except:
            print("There is something wrong!")
            return None
        page_num = html.xpath("//div[@class='paging']/ul/li/a[@name='bottom-page-turn']/text()")
        return int(page_num[-1])

    def get_url_list(self,key):#构造url列表
        url_list = [self.url_model.format(key,i) for i in range(1,self.get_page_num(key)+1)]
        return url_list

    def get_data(self,url):#获取书名,价格,评论数
        html = etree.HTML(self.get_html(url))
        li_list =html.xpath("//ul[@class='bigimg']//li")        #节点列表

        for li in li_list:
            item = {}
            item['name'] = li.xpath(".//a[@class='pic']//@title")[0]
            item['price'] = float(li.xpath(".//span[@class='search_now_price']/text()")[0][1:])
            item['comments'] = int(li.xpath(".//a[@class='search_comment_num']/text()")[0][:-3])#清洗comments的字符串
            item['publisher'] = str(li.xpath(".//a[@dd_name='单品出版社']/text()"))[2:-2]
            self.items_list.append(item)

    def save_data(self,name,data):			#保存数据
        with open(name+'.csv','a') as f:
            for item in data:
                f.write(json.dumps(item,ensure_ascii=False))
                f.write('\n')

    def Mymultithread(self,url_list,max_threads=50):		#多线程爬取信息
        def urls_process(urls):
            while True:
                try:
                    url =urls.pop()
                except IndexError:
                    break

                self.get_data(url)
                print("页面数据获取成功！")

        threads = []
        while int(len(threads)<max_threads) and len(url_list):
            thread = threading.Thread(target=urls_process,args=[url_list])
            print('创建线程', thread.getName())
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def run(self):#实现主要逻辑
        #0.输入检索关键词
        key = input("Please input the key words you want to search:")
        #1.构造url列表
        url_list = self.get_url_list(key)
        print("构造url列表成功！")
        #2.多线程爬取信息
        self.Mymultithread(url_list)
        #3.保存原始数据
        self.save_data('item_list', self.items_list)
        print("原始数据保存成功！")
        #4.数据处理
        d = pd.DataFrame(self.items_list)

        d = d.reindex(columns=['name','price','publisher','comments'])  #排序 列索引
        comments_rank = d.sort_values('comments',ascending=False)       #评论数排行
        top_20_of_cm = comments_rank.head(20).sort_index()              #评论数前十名

        comment = top_20_of_cm['comments'].tolist()                     #转化为列表以便可视化数据
        name_in_cm = top_20_of_cm['name'].tolist()                      #转化为列表

        price_rank = d.sort_values('price',ascending=False)             #价格排行
        top_20_of_pr = price_rank.head(20).sort_index()                 #价格排行前十名
        price = top_20_of_pr['price'].tolist()                          #转化为列表
        name_in_pr = top_20_of_pr['name'].tolist()                      #转化为列表

        counts = d['publisher'].value_counts()                          #各出版社出现次数
        counts = counts.to_dict()                                       #转化为字典
        #5.数据可视化
        visualization = visualize_data()                                #调用可视化的类
        visualization.bar(name_in_cm,comment,'comments top10')
        visualization.bar(name_in_pr,price,'price top10')
        visualization.pie(list(counts.keys())[:10],list(counts.values())[:10],'publisher top10')
        print("可视化完成,请登录查看！")

Spider = DangDang_Spider()
Spider.run()