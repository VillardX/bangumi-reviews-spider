from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

class one_item:
    def __init__(self, base_html):
        """
            初始化每一款游戏产品页面的基础地址
            形如
            https://bangumi.tv/subject/XXXXXX
        """
        self.base_html = base_html#初始化，赋予该款游戏产品的基址
        self.id = ''#id初始化
        self.total = []#概览信息初始化
        self.characters = {}#角色信息初始化
        self.persons = {}#制作人员信息初始化
        self.comments = []#评论信息初始化
        
        #先获取id
        match = re.search(r'[0-9]+', self.base_html)
        self.id = match.group(0)
     
    def is_crawlable(self):
        """
            确认是否可爬
        """
        html = urlopen(self.base_html)
        bs0bj = BeautifulSoup(html)
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
        html = urlopen(self.base_html)
        bs0bj = BeautifulSoup(html)
        
        #左侧简要信息
        brief_info_string = ""#使用”||“分割
        brief_info_tag = bs0bj.find('ul',{'id':'infobox'})#<ul id="infobox">的标签在该页面中只有一个，故只需要使用find函数即可
        brief_info_list = brief_info_tag.findAll('li')
        for x in brief_info_list:
            brief_info_string += (x.get_text() + '||')
        self.total.append(brief_info_string)
#         print(brief_info_string)
        
        #中部所有标签
        mid_info_string = ""#使用”||“分割
        mid_info_tag_LV1 = bs0bj.find('div',{'class':'subject_tag_section'})#无法直接定位，故采用二级式标签
        mid_info_tag_LV2 = mid_info_tag_LV1.find('div',{'class':'inner'})
        mid_info_list = mid_info_tag_LV2.findAll('a')
        for x in mid_info_list:#贴的标签名称与所贴标签人数
            mid_info_string += (x.get_text() + '||')
        self.total.append(mid_info_string)
#         print(mid_info_string)

        #右部的评分、rank
        right_info_string = ""#使用”||“分割
        right_info_tag = bs0bj.find('div',{'class':'global_score'})#定位大页面
        score = right_info_tag.find('span',{'class':'number'}).get_text()#爬取评分
        #爬取rank,要区分有rank和没有rank的情况
        if type(right_info_tag.find('small',{'class':'alarm'})):#如果没有该标签，说明暂无rank
            rank = '-'
        else:
            rank = right_info_tag.find('small',{'class':'alarm'}).get_text()#爬取rank
        right_info_string =  (score + "||" + rank)
        self.total.append(right_info_string)
#         print(right_info_string)

        print(self.total)

    def info_characters(self):
        """
            获取角色页面信息
        """
        suffix = r'/characters'#角色信息页面后缀名
        html = urlopen(self.base_html + suffix)
        bs0bj = BeautifulSoup(html)
        character_info_tag = bs0bj.find('div',{'class':'column','id':'columnInSubjectA'})
        print(character_info_tag.child == None)
    
    def info_persons(self):
        """
            获取制作人员信息
        """
        pass
    
    def info_comments(self):
        """
            获取吐槽页面信息
        """
        suffix = r'/comments'#吐槽页面后缀名
        
        initial_page = self.base_html + suffix#初始页面
        present_page = self.base_html + suffix#当前页面
        
        #爬取当前页面内容+换页
        while True:
            present_html = urlopen(present_page)
            present_bs0bj = BeautifulSoup(present_html)
            
            #爬取评论
            present_html = urlopen(present_page)
            present_bs0bj = BeautifulSoup(present_html)

            total_comment_tag = present_bs0bj.find('div',{'id':'comment_box'})#包含了每页所有评论的总tag
            comment_list_tag = total_comment_tag.findAll('div',{'class':'text'})#该列表中包含了每条评论及其评分
            for each_comment in comment_list_tag:
                comment_content = each_comment.find('p').get_text()#每条评论的内容
                #每条评论对应的评分，分两种情况：一种是有评分的，一种是没有评分的
                is_score = each_comment.find('span')#是否有评分的标记,如果没有，is_score返回None
                if is_score == None:
                    comment_score = 'sstars99'#没有评分的记为99星方便后面数值化处理
                else:#说明有评分
                    comment_score = each_comment.find('span')['class'][0]#每条评论对应的评分
                together_comment = (comment_content + "|" + comment_score + "||")#整合，单条评论的内容与评分用|分割，不同评论之间用||分割
                self.comments.append(together_comment)#加入评论数据
                
            
            pages_tag = present_bs0bj.find('div',{'class':'page_inner'})#可以知道有多少页评论的tag在这里
            if ('››' in pages_tag.get_text()):#如果返回True说明当前页还有下一页
                #跳到下一页
                next_page = pages_tag.findAll(name = 'a')#返回一个列表，要在该列表中寻找下一页的连接
                for x in next_page:
                    if x.get_text() == '››':#有"››"即为下一页连接
                        present_page = initial_page + x['href']
            else:#否则说明没有下一页
                break
        print(self.comments)
