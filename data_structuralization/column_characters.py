#-*- coding: UTF-8 -*- 
import pandas as pd
from ast import literal_eval
import re
path = r'D:\pycode\ACGN\raw_data.txt'

raw_data = pd.read_csv(path, encoding='utf-8',index_col=0)

#处理raw_data_characters

raw_data_characters = raw_data.loc[:,['id','characters']]#先把characters信息取出
#print(raw_data_characters)
n = 0#计数器

characters_voice = pd.DataFrame(columns=['id','声优','角色类型'])#建立空表

for row_num in range(raw_data_characters.shape[0]):
    temp_id = str(raw_data_characters.loc[row_num,'id'])#先取出id
    if temp_id in characters_voice['id']:#查重
        print("id" + temp_id + "\t已在数据集characters_voice中，故省略")
    else:
        temp_characters = raw_data_characters.loc[row_num,'characters']
        temp_characters = literal_eval(temp_characters)#信息转化为list
        if len(temp_characters) == 0:#如果没有内容
            characters_voice.loc[characters_voice.shape[0]] = [temp_id,'','']#只填入id
            #print('id' + temp_id + '无具体信息，故跳过')
        else:#说明有内容
            for each_character in temp_characters:#遍历
                CV_name = each_character.split("|-*-|")[1].strip()#声优名
                if CV_name != '-':#说明CV名非空
                    characters_type = each_character.split("|-*-|")[0].strip()#所配音角色类型
                    characters_voice.loc[characters_voice.shape[0]] = [temp_id,CV_name,characters_type]#填入信息
    n += 1#处理完一款产品数据
    if n % 1000 == 0:#每处理完1000款产品进行报告
        print('已处理\t' + str(n) + '款产品') 
        
characters_voice = characters_voice.drop_duplicates()#去重
#characters_voice.to_excel('characters_voice.xlsx',index=False)#输出
characters_voice.to_csv('characters_voice.csv',encoding = 'utf-8', index=False)#输出
