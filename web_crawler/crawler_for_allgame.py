#-*- coding: UTF-8 -*- 
#爬取bangumi上所有游戏的信息
import single_item_frame as sif
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import time 

basement = r'https://bangumi.tv'#单款产品基础网址
start_page = r'https://bangumi.tv/game/browser'#单页面基础网址
present_page = r'https://bangumi.tv/game/browser?page=1'#当前地址


#数据读取
try:
    raw_data_total_left = pd.read_csv('raw_data_total_left.csv',encoding='utf-8')
except:
    raw_data_total_left = pd.DataFrame(columns=['game_id','attr','thing'])#游戏信息初始化,id，属性，内容
    print('left文件不存在，创建一个')

try:
    raw_data_total_mid = pd.read_csv('raw_data_total_mid.csv',encoding='utf-8')
except:
    raw_data_total_mid = pd.DataFrame(columns=['game_id','tag_name','tag_num'])
    print('mid文件不存在，创建一个')

try:
    raw_data_total_right = pd.read_csv('raw_data_total_right.csv',encoding='utf-8')
except:
    raw_data_total_right = pd.DataFrame(columns=['game_id','score','rank'])
    print('right文件不存在，创建一个')
    
try:
    raw_data_characters = pd.read_csv('raw_data_characters.csv',encoding='utf-8')
except:
    raw_data_characters = pd.DataFrame(columns=['game_id','cv_id','charcter_type','name','other_name'])#角色信息初始化,声优id，角色类型，声优原名，别名
    print('characters文件不存在，创建一个')
    
try:
    raw_data_persons = pd.read_csv('raw_data_persons.csv',encoding='utf-8')
except:
    raw_data_persons = pd.DataFrame(columns=['game_id','person_id','work','name','other_name'])#制作人员信息初始化，职务、名字、别名
    print('persons文件不存在，创建一个')

try:
    raw_data_comments = pd.read_csv('raw_data_comments.csv',encoding='utf-8')
except:
    raw_data_comments = pd.DataFrame(columns=['game_id','user_id','issue_time','user_score','content'])#存储数据的dataframe#评论信息初始化
    print('comments文件不存在，创建一个')

#记录已经获取的gameid
id_list_left = list(set(raw_data_total_left['game_id']))
id_list_mid = list(set(raw_data_total_mid['game_id']))
id_list_right = list(set(raw_data_total_right['game_id']))
id_list_characters = list(set(raw_data_characters['game_id']))
id_list_persons = list(set(raw_data_persons['game_id']))
id_list_comments = list(set(raw_data_comments['game_id']))

#读取已有数据
# raw_data_total_left = pd.read_csv('raw_data_total_left.csv',encoding='utf-8')
# raw_data_total_mid = pd.read_csv('raw_data_total_mid.csv',encoding='utf-8')
# raw_data_total_right = pd.read_csv('raw_data_total_right.csv',encoding='utf-8')
# raw_data_characters = pd.read_csv('raw_data_characters.csv',encoding='utf-8')
# raw_data_persons = pd.read_csv('raw_data_persons.csv',encoding='utf-8')
# raw_data_comments = pd.read_csv('raw_data_comments.csv',encoding='utf-8')

# #数据结构
# raw_data_total_left = pd.DataFrame(columns=['game_id','attr','thing'])#游戏信息初始化,id，属性，内容
# raw_data_total_mid = pd.DataFrame(columns=['game_id','tag_name','tag_num'])
# raw_data_total_right = pd.DataFrame(columns=['game_id','score','rank'])
# raw_data_characters = pd.DataFrame(columns=['game_id','cv_id','charcter_type','name','other_name'])#角色信息初始化,声优id，角色类型，声优原名，别名
# raw_data_persons = pd.DataFrame(columns=['game_id','person_id','work','name','other_name'])#制作人员信息初始化，职务、名字、别名
# raw_data_comments = pd.DataFrame(columns=['game_id','user_id','issue_time','user_score','content'])#存储数据的dataframe#评论信息初始化


#累计爬取产品数
n = 0

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
        #先查看是否可爬
        browse_page = basement + each_item['href']
        temp = sif.one_item(browse_page)
        if temp.is_crawlable():
            #total信息有一列不存在就得加
            if (fi_id in id_list_left) + (fi_id in id_list_mid) + (fi_id in id_list_right) < 3:
                temp.info_total()
                if fi_id not in id_list_left:
                    raw_data_total_left = pd.concat([raw_data_total_left,temp.total_left])
                    print(str(fi_id)+'left数据不存在，故加入')
                if fi_id not in id_list_mid:
                    raw_data_total_mid = pd.concat([raw_data_total_mid,temp.total_mid])
                    print(str(fi_id)+'mid数据不存在，故加入')
                if fi_id not in id_list_right:
                    raw_data_total_right = pd.concat([raw_data_total_right,temp.total_right])
                    print(str(fi_id)+'right数据不存在，故加入')
            if fi_id not in id_list_characters:
                raw_data_characters = pd.concat([raw_data_characters,temp.characters])
                print(str(fi_id)+'characters数据不存在，故加入')
            if fi_id not in id_list_persons:
                raw_data_persons = pd.concat([raw_data_persons,temp.persons])
                print(str(fi_id)+'persons数据不存在，故加入')
            if fi_id not in id_list_comments:
                raw_data_comments = pd.concat([raw_data_comments,temp.comments])
                print(str(fi_id)+'comments数据不存在，故加入')
        
            n += 1
            if (n % 5 == 0):#每满五条输出一次
                print('已获取' + str(n) + '个产品，输出一次')#输出日志
                print("当前时间： ",time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())))
                raw_data_total_left.to_csv('raw_data_total_left.csv',index = False, encoding = 'utf-8')#原始爬取数据输出
                raw_data_total_mid.to_csv('raw_data_total_mid.csv',index = False, encoding = 'utf-8')#原始爬取数据输出
                raw_data_total_right.to_csv('raw_data_total_right.csv',index = False, encoding = 'utf-8')#原始爬取数据输出
                raw_data_characters.to_csv('raw_data_characters.csv',index = False, encoding = 'utf-8')
                raw_data_persons.to_csv('raw_data_persons.csv',index = False, encoding = 'utf-8')
                raw_data_comments.to_csv('raw_data_comments.csv',index = False, encoding = 'utf-8')
        else:
            print(str(fi_id) + '不可爬，故跳过')
    #判断是否为最后一页
    is_last_page = present_bs0bj.find('div',{'class':'page_inner'})
    if '››' in is_last_page.get_text():#说明还有下一页
        next_page = is_last_page.findAll('a')
        for x in next_page:
            if x.get_text() == '››':#有"››"即为下一页连接
                present_page = start_page + x['href']
    else:#说明没有下一页
        break
raw_data_total_left.to_csv('raw_data_total_left.csv',index = False, encoding = 'utf-8')#原始爬取数据输出
raw_data_total_mid.to_csv('raw_data_total_mid.csv',index = False, encoding = 'utf-8')#原始爬取数据输出
raw_data_total_right.to_csv('raw_data_total_right.csv',index = False, encoding = 'utf-8')#原始爬取数据输出
raw_data_characters.to_csv('raw_data_characters.csv',index = False, encoding = 'utf-8')
raw_data_persons.to_csv('raw_data_persons.csv',index = False, encoding = 'utf-8')
raw_data_comments.to_csv('raw_data_comments.csv',index = False, encoding = 'utf-8')
