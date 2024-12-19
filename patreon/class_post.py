class Post:
    def __init__(self, title, url, published):
        self.title = title
        self.url = url
        self.published = published

    def __str__(self):
        return f'(title={self.title}, url={self.url}, published={self.published}'