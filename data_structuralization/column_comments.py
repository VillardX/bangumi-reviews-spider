import pandas as pd
import single_item_frame as sif
from ast import literal_eval
import re
path = r'D:\pycode\ACGN\raw_data_all.xlsx'

raw_data = pd.read_excel(path)

#处理comments列

raw_data_comments = raw_data.loc[:,['id','comments']]#先把comments信息取出

n = 0#计数器

comments_tsukkomi = pd.DataFrame(columns=['id','评论编号','评论内容','评分'])#建立空表

error_id = []#存放comments列有问题的id

for row_num in range(raw_data_comments.shape[0]):
    temp_id = str(raw_data_comments.loc[row_num,'id'])#先取出id
    if temp_id in comments_tsukkomi['id']:#去重
        print('id' + temp_id + '\t已在数据集comments_tsukkomi中，故省略')
    else:
        temp_comments = raw_data_comments.loc[row_num,'comments']
        try:
            temp_comments = literal_eval(temp_comments)#信息转化为list
        except:#有些产品的评论过长，excel的一个单元格可能未能完整存取
            print('id' + temp_id +'\t存在问题，故跳过')
            error_id.append(temp_id)
        else:
            if len(temp_comments) ==0 :#如果没有内容
                comments_tsukkomi.loc[comments_tsukkomi.shape[0]] = [temp_id,'','','']#只填入id
            else:
                comment_NO = 1#评论编号，从1开始
                for each_comment in temp_comments:
                    comment_content = each_comment.split("|",1)[0]#只分一次，因为后面还有"||"
                    comment_score = each_comment.split("|",1)[1]
                    comment_score = re.findall(r'[0-9]+',comment_score)[0]#只取出数字
                    comments_tsukkomi.loc[comments_tsukkomi.shape[0]] = [temp_id,str(comment_NO),comment_content,comment_score]#填入一条信息
                    comment_NO += 1#编号+1
    n += 1#处理完一款产品数据
    if n % 500 == 0:#每处理完500款产品进行报告
        print('已处理\t' + str(n) + '款产品')
        
comments_tsukkomi =  comments_tsukkomi.drop_duplicates()#去重
comments_tsukkomi.to_excel('comments_tsukkomi.xlsx')#输出   
