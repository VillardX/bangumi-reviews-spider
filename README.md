# bangumi_reviews
## 爬取bangumi网站的所有游戏数据与对应评论
### 涵盖内容：
 - 数据爬取（于web_crawler文件夹中）
 - 数据结构化（于data_structuralization文件夹中）

# 一、爬虫结构
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
\n其中XXXXXX为每一部作品的id

## 爬取内容
 1. 概览页面
    - 左侧简要信息
    - 中部所有tag标签及各标签的标记人数
    - 右部的评分、rank
 2. 角色页面
    - cv原文姓名
    - cv中文姓名
    - 是主角还是配角
 3. 制作人员页面
    - 每位成员原文名称
    - 每位成员中文名称
    - 该成员担任的职务
4. 吐槽页面
    - 评论用户的id
    - 评论时间
    - 用户评分
    - 评论内容
