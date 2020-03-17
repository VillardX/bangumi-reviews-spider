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
    <br/>注：其中XXXXXX为每一部作品的id

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

## 流程

### 总体
 ![image](https://github.com/VillardX/DL_ACGN/blob/master/images/web_crawler/%E6%80%BB%E4%BD%93.jpg) 

### 爬取该页所有游戏信息
 ![image](https://github.com/VillardX/DL_ACGN/blob/master/images/web_crawler/%E7%88%AC%E5%8F%96%E8%AF%A5%E9%A1%B5%E6%89%80%E6%9C%89%E4%BF%A1%E6%81%AF.jpg)

### 爬取当前游戏信息
 ![image](https://github.com/VillardX/DL_ACGN/blob/master/images/web_crawler/%E7%88%AC%E5%8F%96%E5%BD%93%E5%89%8D%E6%B8%B8%E6%88%8F%E4%BF%A1%E6%81%AF.jpg)

### 使用代码实现该流程的具体方案
- single_item_frame.py模块：爬取单款游戏的所有信息。
- 而后在crawler_for_allgame.py中导入single_item_frame.py模块，完成全部游戏信息的爬取。

 
 ## 原始数据的输出格式
一共有六个pd.DataFrame。
- 1.表raw_data_total_left：

|game_id|attr|thing|
|-|-|-|
|int|string|string|

- 字段解释：
    - game_id：以字符串的形式存放该产品在bangumi中的编号
    - attr：基本信息类别
    - thing：信息内容

- 2.表raw_data_total_mid：

|game_id|tag_name|tag_num|
|-|-|-|
|int|string|int|

- 字段解释：
    - game_id：以字符串的形式存放该产品在bangumi中的编号
    - attr：tag标签名称
    - thing：标记该标签的人数

- 3.表raw_data_total_right：

|game_id|score|rank|
|-|-|-|
|int|float|int|

- 字段解释：
    - game_id：以字符串的形式存放该产品在bangumi中的编号
    - score：该产品的总体评分
    - thing：该产品的排名

- 4.表raw_data_persons：

|game_id|person_id|work|name|other_name|
|-|-|-|-|-|
|int|int|string|string|string|

- 字段解释：
    - game_id：以字符串的形式存放该产品在bangumi中的编号
    - person_id：该工作人员在bangumi中的编号
    - work：该工作人员所担任的工作
    - name：该工作人员的原名
    - other_name：该工作人员的中文名

- 5.表raw_data_characters：

|game_id|cv_id|character_type|name|other_name|
|-|-|-|-|-|
|int|int|string|string|string|

- 字段解释：
    - game_id：以字符串的形式存放该产品在bangumi中的编号
    - cv_id：该配音人员在bangumi中的编号
    - work：该配音人员担任的角色为主角还是配角
    - name：该配音人员的原名
    - other_name：该配音人员的中文名

- 6.表raw_data_comments：

|game_id|user_id|issue_time|user_score|content|
|-|-|-|-|-|
|int|string|date|int|string|

- 字段解释：
    - game_id：以字符串的形式存放该产品在bangumi中的编号
    - user_id：该用户在bangumi中的编号
    - issue_time：评论时间
    - user_score：用户评分
    - content：评论内容
