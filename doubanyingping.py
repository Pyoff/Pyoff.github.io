#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/2/27 16:18 
# @Author : Pyoff 
# @Site :  
# @File : doubanyingping.py 
# @Software: PyCharm

from urllib import request
from bs4 import BeautifulSoup
import re
import jieba
import pandas as pd
import numpy
import matplotlib.pyplot as plt
#%matplotlib inline
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from wordcloud import WordCloud
#import codecs
import warnings
warnings.filterwarnings("ignore")

#分析网页函数
def getmovie_list():
    movie_url = 'https://movie.douban.com/cinema/nowplaying/guangzhou/'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    req = request.Request(url=movie_url, headers=headers)
    #html_data = req.request.urlopen(req).read()
    resp = request.urlopen(req)
    html_data = resp.read().decode('utf-8')
    #print(html_data)
    soup = BeautifulSoup(html_data, 'html.parser')
    nowplaying_movie = soup.find_all('div', id = 'nowplaying')
    nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_ = 'list-item')
    #print(nowplaying_movie_list[0])
    global nowplaying_list
    nowplaying_list = []
    for item in nowplaying_movie_list:
        nowplaying_dict = {}
        nowplaying_dict['id'] = item['data-subject']
        for tag_img_item in item.find_all('img'):
            nowplaying_dict['name'] = tag_img_item['alt']
            nowplaying_list.append(nowplaying_dict)
    #print(nowplaying_list)
    return nowplaying_list

#获取评论函数
def get_comment(movieId, pageNum):
    global eachcomment
    eachcomment = []
    if pageNum > 0:
        start = (pageNum-1) * 20
    else:
        return False
    comment_url = 'https://movie.douban.com/subject/'+ nowplaying_list[0]['id'] + '/comments' + '?' + 'start=0' + '&limit=20' \
                  + '&sort=new_score' + '&status=P&percent_type='
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    resp = request.Request(url = comment_url,headers  =  headers)
    resp = request.urlopen(resp)
    html_data = resp.read().decode('utf-8')
    soup = BeautifulSoup(html_data, 'html.parser')
    comment_div = soup.find_all('div', class_ = 'comment')
    for item in comment_div:
        if item.find_all('p')[0].string is not None:
            eachcomment.append(item.find_all('p')[0].string)
    #print(eachcomment)
    return eachcomment

def main():
    #循环获取第一个电影的前10页评论
    commentslist = []
    nowplayingmovie_list = getmovie_list()
    for i in range(20):
        num = i+1
        commentlist_temp = get_comment(nowplayingmovie_list[0]['id'],num)
        commentslist.append(commentlist_temp)
        #将列表中的数据转换成字符串
        comments = ''
    for com in range(len(eachcomment)):
        comments = comments + (str(eachcomment[com])).strip()
    #使用正则表达式去除标点符号
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern,comments)
    clean_comments = ''.join(filterdata)
    #print(clean_comments)
    #使用结巴分词进行中文分词
    segment = jieba.lcut(clean_comments)
    words_df = pd.DataFrame({'segment':segment})
    #去掉停用词
    stopwords = pd.read_csv("stopwords.txt", index_col=False, quotechar="3", sep="\t", names = ['stopwords'], encoding='gb2312')
    words_df = words_df[~words_df.segment.isin(stopwords)]
    #统计词频
    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
    words_stat = words_stat.reset_index().sort_values(by = ["计数"], ascending=False)
    #用词云进行显示
    wordcloud = WordCloud(font_path="C:/windows/fonts/simhei.ttf", background_color="white", max_font_size=80)
    word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}
    word_frequence_list = []
    for key in word_frequence:
        temp = (key,word_frequence[key])
        word_frequence_list.append(temp)
    wordcloud = wordcloud.fit_words(dict(word_frequence_list))
    plt.imshow(wordcloud)
    #plt.savefig("result.jpg")
    plt.axis('off')
    plt.show()

main()