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
- 整体为一个pd.DataFrame，其结构为：

|id|total|characters|persons|comments|
|-|-|-|-|-|
|string|list|list|list|list|

如上表格所示，对于每一款产品，都是该DataFrame中的一行。各产品信息都有5个属性：

- id：以字符串的形式存放该产品在bangumi中的编号
- total：以列表的形式存放该产品的概览页面的信息，该列表中有3个元素，每个元素都是字符串，分别存放了：
    - 左侧简要信息
    - 中部所有tag标签
    - 右部的评分、rank
- characters：以列表的形式存放该产品的角色页面信息，该列表的每个元素为字符串，每个字符串存放：
    - cv姓名
    - 是主角还是配角
- persons：以列表的形式存放该产品的制作人员页面信息，该列表的每个元素为字符串，每个字符串存放：
    - 每位成员名称
    - 担任职务
- comments：以列表的形式存放该产品的吐槽页面信息，该列表的每个元素为字符串，每个字符串存放：
    - 每条评论的用户id
    - 每条评论的评论时间
    - 每条评论的内容
    - 每条评论给出的产品评分
