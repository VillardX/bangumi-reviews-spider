import pandas as pd
from ast import literal_eval
import re
path = r'D:\pycode\ACGN\raw_data_all.xlsx'

raw_data = pd.read_excel(path)

#处理total_persons

raw_data_persons = raw_data.loc[:,['id','persons']]#先把persons信息取出
#print(raw_data_persons)
n = 0#计数器

persons_division = pd.DataFrame(columns=['id','原名','中文名','职务1','职务2','职务3','职务4','职务5','职务6','职务7','职务8','职务9'])#建立空表

for row_num in range(raw_data_persons.shape[0]):
    temp_id = str(raw_data_persons.loc[row_num,'id'])#先取出id
    if temp_id in persons_division['id']:#查重
        print('id' + temp_id +'\t已在数据集persons_division中，故省略')
    else:
        temp_persons = raw_data_persons.loc[row_num,'persons']
        temp_persons = literal_eval(temp_persons)#信息转化为list
        if len(temp_persons) == 0:#如果没有内容
            persons_division.loc[persons_division.shape[0]] = [temp_id,'','','','','','','','','','','']#只填入id
        else:
            for each_person in temp_persons:#遍历
                pos = each_person.rfind(':')#找到each_person字符串中最后一次出现:的位置，不用split是为了防止'Mju:z :动画制作||'诸如情况发生
                name = each_person[:pos]#得到名称
                work = each_person[pos + 1:]#得到职务
                #先处理名称
                if r'/' in name:#说明有中文名
                    orignal_name = name.split(r'/')[0].strip()#原始名
                    chinese_name = name.split(r'/')[1].strip()#中文名
                else:#说明没有中文名
                    orignal_name = name.strip()
                    chinese_name = ''  
                #再处理职务
                work_list = work.split("||")            
                work_list.remove('')#去除列表中内容为空得元素
                one_info = [temp_id,orignal_name,chinese_name] + work_list#一条信息，后期还会填入，两个表得合并
                for i in range(9 - len(work_list)):#剩下的职务用空字符串填补
                    one_info.append('')                
                persons_division.loc[persons_division.shape[0]] = one_info
    n += 1#处理完一款产品数据
    if n % 500 == 0:#每处理完500款产品进行报告
        print('已处理\t' + str(n) + '款产品')