import pandas as pd
from ast import literal_eval
import re
path = r'D:\pycode\ACGN\raw_data.xlsx'

raw_data = pd.read_excel(path)

#将total列中的左元素、中元素、右元素分出来
raw_data_total = pd.DataFrame(columns=['id', 'left', 'mid', 'right'])#建立空的dataframe，四列分别记录id、左、中、右信息
for num in range(raw_data.shape[0]):
    each_total = {'id':raw_data.ix[num,'id'], 'left':'', 'mid':'', 'right':''}#每款游戏的total信息
    each_total_list = literal_eval(raw_data.ix[num,'total'])#将信息转化为list
    each_total['left'] = each_total_list[0]
    each_total['mid'] = each_total_list[1]
    each_total['right'] = each_total_list[2]
    raw_data_total.loc[raw_data_total.shape[0]] = each_total#添加一行


#对total取三份切片，分别记为total_left、total_mid、total_right
total_left = raw_data_total.ix[:,['id','left']]
total_mid = raw_data_total.ix[:,['id','mid']]
total_right = raw_data_total.ix[:,['id','right']]


#处理total_left
n = 0#计数器

total_brief = pd.DataFrame(columns=['id','基本信息类别','内容'])
for row_num in range(total_left.shape[0]):#遍历total_left的每一行数据
    temp_id = str(total_left.loc[row_num,'id'])#取出该行的id
    if temp_id in total_brief['id']:#查重
        print("id" + temp_id + "已在数据集total_brief中，故省略")
    else:
        temp_left = total_left.loc[row_num,'left']#取出改行属性left的内容（是一个字符串）
        if temp_left =='':#如果是空字符串，说明left中没有信息，那直接跳过\
            total_brief.loc[total_brief.shape[0],'id'] = temp_id#将该产品的id直接加入后结束
            print('id' + temp_id + '无信息，故填入id后跳过')        
        elif temp_left != '':#有信息
            temp_split_list = temp_left.split("||")#以字符"||"分割元素left的内容
            temp_split_list.remove("")#去除没有内容的分割结果
            for temp_each_brief in temp_split_list:#遍历每一种类别的基本信息   
                attr_name = temp_each_brief.split(":",1)[0].strip()#每种类别的基本信息的类别名，如名称、剧本等等，strip函数去除两头空格
                attr_content = temp_each_brief.split(":",1)[1].strip()#该类别基本信息的具体内容
                total_brief.loc[total_brief.shape[0]] = [temp_id,attr_name,attr_content]#将该产品的相关信息加入
    n += 1#处理完一款产品数据
    if n % 100 == 0:#每处理完100款产品进行报告
        print('已处理\t' + str(n) + '款产品')    
total_brief = total_brief.drop_duplicates()#去重
total_brief.to_excel('total_brief.xlsx')#输出        

#处理total_mid
n = 0#计数器

total_tag = pd.DataFrame(columns=['id','标签名称','标记人数'])

for row_num in range(total_mid.shape[0]):#遍历total_mid的每一行数据
    temp_id = str(total_mid.loc[row_num,'id'])#取出该行的id
    if temp_id in total_tag['id']:#查重
        print("id" + temp_id + "已在数据集total_tag中，故省略")
    else:
        temp_mid = total_mid.loc[row_num,'mid']#取出改行属性mid的内容（是一个字符串）
        if temp_mid =='':#如果是空字符串，说明mid中没有信息，那直接跳过
            total_tag.loc[total_tag.shape[0],'id'] = temp_id#将该产品的id直接加入后结束
            print('id' + temp_id + '无信息，故填入id后跳过')     
        elif temp_mid != '':#有信息
            temp_split_list = temp_mid.split("||")#以字符"||"分割元素mid的内容
            temp_split_list.remove("")#去除没有内容的分割结果
            for temp_each_tag in temp_split_list:#遍历每一个tag   
                tag_name = temp_each_tag.split(" ",1)[0].strip()#获取tag名，strip函数去除两头空格
                tag_count = temp_each_tag.split(" ",1)[1].strip()#获取tag标记人数
                total_tag.loc[total_tag.shape[0]] = [temp_id,tag_name,tag_count]#将该产品的相关信息加入
    n += 1#处理完一款产品数据
    if n % 100 == 0:#每处理完100款产品进行报告
        print('已处理\t' + str(n) + '款产品') 
total_tag = total_tag.drop_duplicates()#去重
total_tag.to_excel('total_tag.xlsx')#输出

#处理total_right
n = 0#计数器

total_rank = pd.DataFrame(columns=['id','评分','排名'])

for row_num in range(total_right.shape[0]):#遍历total_right的每一行数据
    temp_id = str(total_right.loc[row_num,'id'])#取出该行的id
    if temp_id in total_rank['id']:#查重
        print("id" + temp_id + "已在数据集total_rank中，故省略")
    else:
        temp_right = total_right.loc[row_num,'right']#取出改行属性right的内容（是一个字符串）
        temp_split_list = temp_right.split("||")#以字符"||"分割元素right的内容，得到一个含有2个元素的list，前为评分，后为排名
        score = temp_split_list[0]#为评分
        rank = temp_split_list[1]#为排名
        if rank =='-':#说明暂无排名
            rank = ''#将排名改为空字符串
        else:#说明有排名
            rank = rank.replace('#','')#将＃替换为空字符串，方便排序
        total_rank.loc[total_rank.shape[0]] = [temp_id,score,rank]#将该产品的相关
    n += 1#处理完一款产品数据
    if n % 100 == 0:#每处理完100款产品进行报告
        print('已处理\t' + str(n) + '款产品')
total_rank = total_rank.drop_duplicates()#去重
total_rank.to_excel('total_rank.xlsx')#输出  
