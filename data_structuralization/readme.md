#爬取数据结构化(structuralization)
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
    - 一条用户评论
    - 该评论对应给出的评分
## 结构化方式
### 属性id
- 不做处理
### 属性total
1. 作原始数据的切片，记为raw_data_total：
    |id|total|
    |-|-|
    |string|list|
2. 根据total的结构，将raw_data_total细化，记为total：
    |id|left|mid|right|
    |-|-|-|-|
    |string|string|string|string|
    其中，属性left、mid、right分别表示左侧简要信息、中部tag标签、右侧评分与rank
3. 对total取三份切片，分别记为total_left、total_mid、total_right：
    |id|left|
    |-|-|
    |string|string|

    |id|mid|
    |-|-|
    |string|string|

    |id|right|
    |-|-|
    |string|string|
    接下来对这三份切片分别作处理。
4. - 对total_left，记其处理后输出的数据集名为total_brief：
        1. 根据爬取数据时事先规定好的分割符，对属性left的内容进行分割。分割所得的每一单元对应该产品的一条基本信息。
        2. 根据基本信息的类别创建新的属性，再在该属性下填入该款产品对应基本信息的内容。
        - e.g.
            以如下信息为例演示处理方式：
            |id|left|
            |-|-|
            |XXXX|'名称:WHITE ALBUM2 -closing chapter-\|\|中文名: 白色相簿2 终章\|\|平台: PC\|\|游戏类型: AVG\|\|发行日期: 2011/12/22\|\|'|

            1. 根据分割符'\|\|'分割属性left的内容，得到如下分割：
            ['名称:WHITE ALBUM2 -closing chapter-','中文名: 白色相簿2 终章','平台: PC','游戏类型: AVG','发行日期: 2011/12/22']
            2. 根据分割内容创建total_brief：

                |id|名称|中文名|平台|游戏类型|发行日期|
                |-|-|-|-|-|-|
                |XXXX|WHITE ALBUM2 -closing chapter-|白色相簿2 终章|PC|AVG|2011/12/22|
