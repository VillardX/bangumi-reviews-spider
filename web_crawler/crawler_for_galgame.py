#爬取bangumi上所有的galgame信息
import single_item_frame as sif
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re

basement = r'https://bangumi.tv'#基础网址
start_page = r'https://bangumi.tv/game/tag/galgame'#首页网址
present_page = r'https://bangumi.tv/game/tag/galgame'

raw_data = pd.DataFrame(columns=['id','total','characters','persons','comments'])#存储数据的dataframe

#爬该页的所有信息

while True:
    present_html = urlopen(present_page)
    present_bs0bj = BeautifulSoup(present_html)
    #先抓取该页上的所有游戏信息
    items_list = present_bs0bj.find('ul',{'id':"browserItemList",'class':"browserFull"}).findAll('a',{'class':'subjectCover cover ll'})#包含了该页面的所有游戏
    for each_item in items_list:
        browse_page = basement + each_item['href']
        temp = sif.one_item(browse_page)
        if temp.is_crawlable():
            temp.info_total()
            temp.info_characters()
            temp.info_comments()
            temp.info_persons()
            raw_data.loc[raw_data.shape[0]] = temp.info#添加一行
    #判断是否为最后一页
    is_last_page = present_bs0bj.find('div',{'class':'page_inner'})
    if '››' in is_last_page.get_text():#说明还有下一页
        next_page = is_last_page.findAll('a')
        for x in next_page:
            if x.get_text() == '››':#有"››"即为下一页连接
                present_page = start_page + x['href']
    else:#说明没有下一页
        break
raw_data.to_excel('raw_data.xlsx')#原始爬取数据输出