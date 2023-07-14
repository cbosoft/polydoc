import os
import bs4


class HtmlTemplate:

    def __init__(self, filename: str):
        with open(os.path.join(os.path.dirname(__file__), filename)) as f:
            self.source = f.read()

        self.soup = bs4.BeautifulSoup(self.source, 'html.parser')
        style: bs4.Tag = self.soup.findAll('style')[0]
        with open(os.path.join(os.path.dirname(__file__), 'style_template.css')) as f:
            style.string = f.read()
    
    def format(self, *args, **kwargs) -> str:
        raise NotImplementedError
