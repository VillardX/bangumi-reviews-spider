
class one_item:
    def __init__(self, base_html):
        """
            初始化每一款游戏产品页面的基础地址
            形如
            https://bangumi.tv/subject/XXXXXX
        """
        self.base_html = base_html#初始化，赋予该款游戏产品的基址
        self.id = 0#id初始化
        self.total = {}#概览信息初始化
        self.characters = {}#角色信息初始化
        self.persons = {}#制作人员信息初始化
        self.comments = {}#评论信息初始化


    def info_id(self):
        """
            获取该款游戏产品的id
        """
     
    def info_total(self):
        """
            获取概览页面信息
        """
        pass

    def info_characters(self):
        """
            获取角色页面信息
        """
        pass
    
    def info_persons(self):
        """
            获取制作人员信息
        """
        pass
    
    def info_comments(self):
        """
            获取吐槽页面信息
        """
        pass