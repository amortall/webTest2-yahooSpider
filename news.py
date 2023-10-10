class News:
    def __init__(self, title, link,description,pub_date):
        self.title = title
        self.link = link
        self.description=description
        self.pub_date=pub_date
    def __str__(self):
        return f"标题: {self.title}\n描述: {self.description}\n链接: {self.link}\n发布日期: {self.pub_date}"