#爬取bangumi上所有游戏的信息
import single_item_frame as sif
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import time 

basement = r'https://bangumi.tv'#单款产品基础网址
start_page = r'http://bangumi.tv/game/browser'#单页面基础网址
present_page = r'http://bangumi.tv/game/browser?page=1'#当前地址

#数据结构
raw_data = pd.DataFrame(columns=['id','total','characters','persons','comments'])#存储数据的dataframe

#累计爬取产品数
n = 0

#在爬取过的信息基础上爬新的信息，去重
already_item_path = r'D:\pycode\ACGN\raw_data_already.xlsx'
already_item_data = pd.read_excel(already_item_path)
already_item_id = already_item_data['id']
already_item_id = list(already_item_id)


#爬取该页所有信息
while True:
    print('正在爬' + present_page)

    #设置超时(timeout)重新请求
    for times in range(50):#默认最多重新请求50次，并假定50次内必定请求成功
        try:
            present_html = urlopen(present_page,timeout = 5)#设置timeout
            present_bs0bj = BeautifulSoup(present_html)
            break
        except:
            print('请求页面时，网址:\t'+ present_page + '\t超时\n再尝试一次，已累计尝试' + str(times + 1) + '次')#出错输出

    #先抓取该页上的所有游戏信息
    items_list = present_bs0bj.find('ul',{'id':"browserItemList",'class':"browserFull"}).findAll('a',{'class':'subjectCover cover ll'})#包含了该页面的所有游戏
    for each_item in items_list:
        fi_id = int(re.search(r'[0-9]+',each_item['href']).group(0))
        if fi_id not in already_item_id:#说明没爬过
            browse_page = basement + each_item['href']
            temp = sif.one_item(browse_page)
            if temp.is_crawlable():
                temp.info_total()
                temp.info_characters()
                temp.info_comments()
                temp.info_persons()
                raw_data.loc[raw_data.shape[0]] = temp.info#添加一行
            n += 1
            if (n%5 == 0):#每满五条输出一次
                print('已扫描' + str(n) + '个产品，输出一次')#输出日志
                print("当前时间： ",time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())))
                raw_data.to_excel('raw_data.xlsx')#原始爬取数据输出
        else:
            print(str(fi_id) + '已爬过，故跳过')
    #判断是否为最后一页
    is_last_page = present_bs0bj.find('div',{'class':'page_inner'})
    if '››' in is_last_page.get_text():#说明还有下一页
        next_page = is_last_page.findAll('a')
        for x in next_page:
            if x.get_text() == '››':#有"››"即为下一页连接
                present_page = start_page + x['href']
    else:#说明没有下一页
        break
raw_data.to_excel('raw_data.xlsx')#最后爬取数据再输出一次
