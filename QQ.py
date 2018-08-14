import re
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import jieba
import pandas as pd
from wordcloud import WordCloud,STOPWORDS
from scipy.misc import imread

def get_date(data):
    #日期
    dates = re.findall(r'\d{4}-\d{2}-\d{2}',data)
    #天
    days = [date[-2:] for date in dates]
    plt.subplot(221)
    sns.countplot(days)
    plt.title('Days')

    #周几
    weekdays = [datetime.date(int(date[:4]),int(date[5:7]),int(date[-2:])).isocalendar()[-1] for date in dates]
    plt.subplot(222)
    sns.countplot(weekdays)
    plt.title('WeekDays')

def get_time(data):
    times = re.findall(r'\d{2}:\d{2}:\d{2}',data)
    #小时
    hours = [time[:2] for time in times]
    plt.subplot(223)
    sns.countplot(hours,order=['06','07','08','09','10','11','12','13','14','15','16',
                               '17','18','19','20','21','22','23','00','01','02','03','04','05'])
    plt.title('Hours')

def get_wordcloud(text_data):
    world_list = [" ".join(jieba.cut(sentence)) for sentence in text_data]
    new_text = ' '.join(world_list)

    pic_path = 'QQ.jpg'
    # mang_mask = imread(pic_path)
    plt.subplot(224)
    wordcloud = WordCloud(background_color="white",
    font_path = '/home/dream/Downloads/微软vista雅黑.ttf',
    mask = None,stopwords=STOPWORDS).generate(new_text)

    plt.imshow(wordcloud)
    plt.axis("off")

def get_person(data):
    names = re.findall(r'\(\d{6,13}\)',data)
    # print(data)
    # plt.subplot(221)
    # sns.countplot(names)
    # plt.title('Person')
    d = pd.DataFrame(names)
    # print(d)
    counts = d[0].value_counts()
    print(counts)

def get_content(data):
    pa = re.compile(r'\d{4}-\d{2}-\d{2}.*?\(\d+\)\n(.*?[^(\[.*?\])])\n\n',re.DOTALL)
    content = re.findall(pa,data)
    get_wordcloud(content)

def run():
    filename = ''   #自定义
    with open(filename) as f:
        data = f.read()
    get_date(data)
    get_time(data)
    get_content(data)
    # get_person(data)

    plt.show()

if __name__ == '__main__':
    run()
