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
tag=type:content:url
元素类型代表意义start开始end结束/完成operation流程操作subroutine预定子流程condition条件判断inputoutput输入输出
- 总体
```flow
st=>start: 开始
o1=>operation: 人为确定爬取范围：游戏-galgame
o2=>operation: 换页
c1=>condition: 是否为最后一页？
s1=>subroutine: 爬取该页所有游戏信息
s2=>subroutine: 爬取该页所有游戏信息
ed=>end: 结束

st->o1->o2->c1
c1(yes)->s2->ed
c1(no)->s1->o2->c1
```

- 爬取该页所有游戏信息
```flow
st=>start: 开始
o2=>operation: 换下一款游戏
c1=>condition: 是否为该页最后一款游戏？
s1=>subroutine: 爬取当前游戏信息
s2=>subroutine: 爬取当前游戏信息
ed=>end: 结束

st->o2->c1
c1(yes)->s1->ed
c1(no)->s2->o2->c1
```
- 爬取当前游戏信息
```flow
st=>start: 开始
s1=>subroutine: 爬取游戏id
s2=>subroutine: 爬取概览页面信息
s3=>subroutine: 爬取角色页面信息
s4=>subroutine: 爬取制作人员页面信息
s5=>subroutine: 爬取吐槽页面信息
ed=>end: 结束

st->s1->s2->s3->s4->s5->ed
````
