#-*- coding: UTF-8 -*- 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd

class one_item:
    def __init__(self, base_html):
        """
            初始化每一款游戏产品页面的基础地址
            形如
            https://bangumi.tv/subject/XXXXXX
        """
        self.base_html = base_html#初始化，赋予该款游戏产品的基址
        self.id = ''#id初始化
        self.total_left = pd.DataFrame(columns=['game_id','attr','thing'])#游戏信息初始化,id，属性，内容
        self.total_mid = pd.DataFrame(columns=['game_id','tag_name','tag_num'])
        self.total_right = pd.DataFrame(columns=['game_id','score','rank'])
        self.characters = pd.DataFrame(columns=['game_id','cv_id','charcter_type','name','other_name'])#角色信息初始化,声优id，角色类型，声优原名，别名
        self.persons = pd.DataFrame(columns=['game_id','person_id','work','name','other_name'])#制作人员信息初始化，职务、名字、别名
        self.comments = pd.DataFrame(columns=['game_id','user_id','issue_time','user_score','content'])#存储数据的dataframe#评论信息初始化
        
        #先获取id
        match = re.search(r'[0-9]+', self.base_html)
        self.id = match.group(0)
        
        #self.info ={'id':self.id, 'total':self.total, 'characters':self.characters, 'persons':self.persons, 'comments':self.comments}
        
     
    def is_crawlable(self):
        """
            确认是否可爬
        """
        #设置超时(timeout)重新请求
        for times in range(50):#默认最多重新请求50次，并假定50次内必定请求成功
            try:
                html = urlopen(self.base_html, timeout = 5)#设置timeout
                bs0bj = BeautifulSoup(html)
                break
            except:
                print('在检测是否可爬时，请求网址:\t'+ self.base_html + '\t超时\n再尝试一次，已累计尝试' + str(times + 1) + '次')#出错输出
        

        if len(bs0bj.findAll('img',{'src':r'/img/bangumi/404.png', 'class':'ll'})) != 0:#如果有该页面信息，则说明不可爬
            print(self.id + "页面信息不存在")
            return False
        else:
            print(self.id + "页面信息存在,可爬取")
            return True
    
    
    def info_total(self):
        """
            获取概览页面信息
        """
        #设置超时(timeout)重新请求
        for times in range(50):#默认最多重新请求50次，并假定50次内必定请求成功
            try:
                html = urlopen(self.base_html, timeout = 5)#设置timeout
                bs0bj = BeautifulSoup(html)
                break
            except:
                print('在获取产品概览信息时，请求网址:\t'+ self.base_html + '\t超时\n再尝试一次，已累计尝试' + str(times + 1) + '次')#出错输出
        
        
        #左侧简要信息
        
        #先找产品名称
        name = bs0bj.find('a',{'property':'v:itemreviewed'}).get_text()
        #先加入名称信息
        self.total_left = self.total_left.append({'game_id':self.id, 'attr':'产品名称', 'thing':name}, ignore_index = True)#将该条信息加入dataframe中


        #再找其他信息
        brief_info_tag = bs0bj.find('ul',{'id':'infobox'})#<ul id="infobox">的标签在该页面中只有一个，故只需要使用find函数即可
        brief_info_list = brief_info_tag.findAll('li')
        for each_info in brief_info_list:
            seg_list = each_info.get_text().split(': ')#分割后一号为attr，二号位thing
            self.total_left = self.total_left.append({'game_id':self.id, 'attr':seg_list[0], 'thing':seg_list[1]}, ignore_index = True)#将该条信息加入dataframe中
        
        
        
        #中部所有标签
        mid_info_tag_LV1 = bs0bj.find('div',{'class':'subject_tag_section'})#无法直接定位，故采用二级式标签
        #查空
        if mid_info_tag_LV1 != None:#有此标签才会有内容
            mid_info_tag_LV2 = mid_info_tag_LV1.find('div',{'class':'inner'})
            mid_info_list = mid_info_tag_LV2.findAll('a')
            for x in mid_info_list:#贴的标签名称与所贴标签人数
                temp_tag = x.find('span').get_text()
                temp_num = x.find('small').get_text()
                self.total_mid = self.total_mid.append({'game_id':self.id, 'tag_name':temp_tag, 'tag_num':temp_num}, ignore_index = True)#数据加入


        
        #右部的评分、rank
        right_info_tag = bs0bj.find('div',{'class':'global_score'})#定位大页面
        score = right_info_tag.find('span',{'class':'number','property':'v:average'}).get_text()#爬取评分
        #爬取rank,要区分有rank和没有rank的情况
        if right_info_tag.find('small',{'class':'alarm'}) == None:#如果没有该标签，说明暂无rank
            rank = ''
        else:
            rank = right_info_tag.find('small',{'class':'alarm'}).get_text()#爬取rank
            rank = rank.replace('#','')#把#替换掉
        self.total_right = self.total_right.append({'game_id':self.id, 'score':score, 'rank':rank}, ignore_index=True)
        
    def info_characters(self):
        """
            获取角色页面信息
        """
        suffix = r'/characters'#角色信息页面后缀名
        characters_URL = self.base_html + suffix

        
        #单条声优的数据格式
        def gen_single_character_structure():
            """
                生成一个角色的数据结构
            """
            single_character_info_temp = {
                'game_id':self.id,
                'cv_id':'',
                'charcter_type':'',
                'name':'',
                'other_name':''
            }
            return single_character_info_temp
        
        
        #设置超时(timeout)重新请求
        for times in range(50):#默认最多重新请求50次，并假定50次内必定请求成功
            try:
                html = urlopen(characters_URL, timeout = 5)#设置timeout
                bs0bj = BeautifulSoup(html)
                break
            except:
                print('在获取产品角色信息时，请求网址:\t'+ characters_URL + '\t超时\n再尝试一次，已累计尝试' + str(times + 1) + '次')#出错输出
        
        
        #开始查找
        character_info_tag = bs0bj.find('div',{'class':'column','id':'columnInSubjectA'})
        #查空
        if len(character_info_tag.contents) != 0:
            each_character_list = character_info_tag.findAll('div',{'style':'padding-left: 90px;','class':'clearit'})
            for each_character in each_character_list:
                character_type = each_character.find('span',{'class':'badge_job'}).get_text()#主配角
                #有的角色可能并未提供cv角色，故需要进一步判断
                character_col = each_character.find('div',{'class':'actorBadge clearit'})
                if (character_col) != None:
                    voice_id = character_col.find('p').find('a')['href'][8:]#cv的id
                    voice_name = character_col.find('p').find('a').get_text()
                    voice_other_name = character_col.find('p').find('small').get_text()
                    
                    temp_character_structure = gen_single_character_structure()#首先生成一个空的结构
                    temp_character_structure['cv_id'] = voice_id
                    temp_character_structure['charcter_type'] = character_type
                    temp_character_structure['name'] = voice_name
                    temp_character_structure['other_name'] = voice_other_name
                    
                    ###把当前的一条信息放入dataframe
                    self.characters = self.characters.append(temp_character_structure, ignore_index = True)#将该条信息加入dataframe中
                        
                        
#         print(self.characters)

    
    def info_persons(self):
        """
            获取制作人员信息
        """
        suffix = r'/persons'#制作人员后缀名
        persons_URL = self.base_html + suffix
        
        #单条工作人员的数据格式
        def gen_single_person_structure():
            """
                生成一个单条评论的数据结构
            """
            single_person_info_temp = {
                'game_id':self.id,
                'person_id':'',
                'work':'',
                'name':'',
                'other_name':''
            }
            return single_person_info_temp
        
        
        #设置超时(timeout)重新请求
        for times in range(50):#默认最多重新请求50次，并假定50次内必定请求成功
            try:
                html = urlopen(persons_URL, timeout = 5)#设置timeout
                bs0bj = BeautifulSoup(html)
                break
            except:
                print('在获取产品制作人员信息时，请求网址:\t'+ persons_URL + '\t超时\n再尝试一次，已累计尝试' + str(times + 1) + '次')#出错输出
        

        #开始查找
        persons_info_tag = bs0bj.find('div',{'id':'columnInSubjectA','class':'column'})#包含所有工作人员及其任务的tag
        #查空
        if len(persons_info_tag.contents) != 0:
            each_person_list = persons_info_tag.findAll('div',{'style':'padding-left: 100px;'})
            for each_person in each_person_list:
                #该工作人的名字，含本名与中文名，按'  / '分割
                one_member = each_person.find('h2').get_text()
                one_member_list = one_member.split('  / ')#分割，可能会有一个或两个元素，取决于有没有中文名
                member_id = each_person.find('h2').find('a')['href'][8:]#找出此人id
                #该该工作人员的职务
                each_person_work_list = each_person.findAll('span',{'class':'badge_job'})
                for each_person_work in each_person_work_list:
                    
                    temp_person_structure = gen_single_person_structure()#首先生成一个空的结构
                    
                    temp_person_structure['person_id'] = member_id
                    temp_person_structure['work'] = each_person_work.get_text()
                    temp_person_structure['name'] = one_member_list[0]
                    if len(one_member_list) > 1:#说明有别名
                        temp_person_structure['other_name'] = one_member_list[1]
                    
                    ###把当前的一条评论放入dataframe
                    self.persons = self.persons.append(temp_person_structure, ignore_index = True)#将该条信息加入dataframe中




    
    def info_comments(self):
        """
            获取吐槽页面信息
        """
        suffix = r'/comments'#吐槽页面后缀名
        
        initial_page = self.base_html + suffix#初始页面
        present_page = self.base_html + suffix#当前页面

        
        #一款游戏的所有评论暂寸于下dataframe中
        #单条评论的数据格式
        def gen_single_comment_structure():
            """
                生成一个单条评论的数据结构
            """
            single_comment_info_temp = {
                'game_id':self.id,
                'user_id':'',
                'issue_time':'',
                'user_score':'',
                'content':''
            }
            return single_comment_info_temp
        
        
        for times in range(50):
            try:
                present_html = urlopen(present_page,timeout = 5)#设置timeout
                present_bs0bj = BeautifulSoup(present_html)
                break
            except:
                print('在获取产品评论信息时，请求网址:\t'+ present_page + '\t超时\n再尝试一次，已累计尝试' + str(times + 1) + '次')#出错输出
        

        #开始查找
        #查空
        if len(present_bs0bj.find('div',{'id':'comment_box'}).contents) != 0:#所有得子节点用列表返回，无子节点代表列表长度为0#说明有子项，说明有评论
            #爬取当前页面内容+换页
            while True:
                for times in range(50):
                    try:
                        present_html = urlopen(present_page,timeout = 5)#设置timeout
                        present_bs0bj = BeautifulSoup(present_html)
                        break
                    except:
                        print('在获取产品评论信息时，请求网址:\t'+ present_page + '\t超时\n再尝试一次，已累计尝试' + str(times + 1) + '次')#出错输出
                        #
                total_comment_tag = present_bs0bj.find('div',{'id':'comment_box'})#包含了每页所有评论的总tag
                comment_list_tag = total_comment_tag.findAll('div',{'class':'text'})#该列表中包含了每条评论及其评分,以及评论用户名及评论时间

                for each_comment in comment_list_tag:#遍历该页中的每一条评论
                    temp_comment_structure = gen_single_comment_structure()#首先生成一个空的结构
                    
                    comment_user_id = each_comment.find('a')['href'][6:]#每条评论的用户名,存在了href属性中，只取第7位到最后一位为id
                    comment_time = each_comment.find('small').get_text()#每条评论的评论时间
                    comment_time = comment_time[2:]#时间以“@ ”开头，去除即可
                    comment_content = each_comment.find('p').get_text()#每条评论的内容
                    #每条评论对应的评分，分两种情况：一种是有评分的，一种是没有评分的
                    is_score = each_comment.find('span')#是否有评分的标记,如果没有，is_score返回None
                    if is_score == None:
                        comment_score = '0'#没有评分的记为0星方便后面数值化处理
                    else:#说明有评分
                        comment_score = is_score.find('span')['class'][1]#每条评论对应的评分，是个list，第二个为评分
                        comment_score = comment_score[5:]
                    #print(comment_score)
                    
                    temp_comment_structure['user_id'] = comment_user_id
                    temp_comment_structure['issue_time'] = comment_time
                    temp_comment_structure['user_score'] = comment_score
                    temp_comment_structure['content'] = comment_content
                    
                    ###把当前的一条评论放入dataframe
                    self.comments = self.comments.append(temp_comment_structure, ignore_index = True)#将该条评论加入dataframe中

                #跳页过程
                pages_tag = present_bs0bj.find('div',{'class':'page_inner'})#可以知道有多少页评论的tag在这里
                if (pages_tag != None):#==None时说明评论只有一页，而一页的评论是没有划页选项的
                    if ('››' in pages_tag.get_text()):#如果返回True说明当前页还有下一页
                        #跳到下一页
                        next_page = pages_tag.findAll(name = 'a')#返回一个列表，要在该列表中寻找下一页的连接
                        for x in next_page:
                            if x.get_text() == '››':#有"››"即为下一页连接
                                present_page = initial_page + x['href']         
                    else:#否则说明没有下一页
                        break
                else:#说明只有一页
                    break
