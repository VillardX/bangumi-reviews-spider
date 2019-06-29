# 爬虫结构
## 网站格式
- 以游戏《素晴日》为例，该游戏页面有如下结构：
    1. 概览页面网址为：https://bangumi.tv/subject/259061
    2. 角色页面网址为：https://bangumi.tv/subject/259061/characters
    3. 制作人员页面网址为； https://bangumi.tv/subject/259061/persons
    4. 吐槽页面网址为： https://bangumi.tv/subject/259061/comments
- 因而不难推测，对于bangumi上的一款游戏，基本的页面结构如下：
    1. 概览页面网址为：https://bangumi.tv/subject/XXXXXX
    2. 角色页面网址为：https://bangumi.tv/subject/XXXXXX/characters
    3. 制作人员页面网址为: https://bangumi.tv/subject/XXXXXX/persons
    4. 吐槽页面网址为： https://bangumi.tv/subject/XXXXXX/comments
其中XXXXXX为每一部作品的id



## 爬取的内容
 0. 作品id（可以作为后面数据处理中每个样本的key，可从概览页面网址本身爬取） 
 1. 概览页面
    - 左侧简要信息
    - 中部所有tag标签
    - 右部的评分、rank
 2. 角色页面
    - cv姓名
    - 配音角色性别
    - 是主角还是配角
 3. 制作人员页面
    - 每位成员名称（法人和自然人混在了一起了，得另外区分）
    - 担任职务（可能有一人多职的存在）
4. 吐槽页面（评论）
    - 爬取所有评论（后期准备nlp）

## 细节问题
4. 吐槽页面
     - 得确定吐槽页面的页数
## 流程

### 总体
 ![image](https://github.com/VillardX/DL_ACGN/blob/master/images/web_crawler/%E6%80%BB%E4%BD%93.jpg) 

### 爬取该页所有游戏信息
 ![image](https://github.com/VillardX/DL_ACGN/blob/master/images/web_crawler/%E7%88%AC%E5%8F%96%E8%AF%A5%E9%A1%B5%E6%89%80%E6%9C%89%E4%BF%A1%E6%81%AF.jpg)

### 爬取当前游戏信息
 ![image](https://github.com/VillardX/DL_ACGN/blob/master/images/web_crawler/%E7%88%AC%E5%8F%96%E5%BD%93%E5%89%8D%E6%B8%B8%E6%88%8F%E4%BF%A1%E6%81%AF.jpg)
