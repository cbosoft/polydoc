import os
import bs4
from typing import List


class HtmlTemplate:

    def __init__(self, filename: str):
        with open(os.path.join(os.path.dirname(__file__), filename)) as f:
            self.source = f.read()

        self.soup = bs4.BeautifulSoup(self.source, 'html.parser')
        style: bs4.Tag = self.soup.findAll('style')[0]
        with open(os.path.join(os.path.dirname(__file__), 'style_template.css')) as f:
            style.string = f.read()
    
    def set_link(self, id: str, href: str, text: str):
        tag: bs4.Tag = self.soup.findAll(id=id)[0]
        tag.clear()
        tag.attrs['href'] = href
        tag.string = text
    
    def set_children(self, id: str, children: List[str]):
        tag: bs4.Tag = self.soup.findAll(id=id)[0]
        tag.clear()
        for child in children:
            if isinstance(child, str):
                child = bs4.BeautifulSoup(child, 'html.parser')
            tag.append(child)
    
    def set_text(self, id: str, text: str):
        tag: bs4.Tag = self.soup.findAll(id=id)[0]
        tag.clear()
        tag.append(bs4.BeautifulSoup(text, 'html.parser'))
    
    def set_title(self, title: str):
        tag: bs4.Tag = self.soup.findAll('title')[0]
        tag.string = title
    
    def set_project_name(self, project_name: str, index_href: str, subprojects=None):
        self.set_link('projectName', index_href, project_name)
        if subprojects:
            self.set_children(
                id='projectVersion',
                children=[
                    f'<small><b>{subp}</b> v{ver}</small><br />'
                    for subp, ver in subprojects.items()
                ]
            )
    
    def format(self, *args, **kwargs) -> str:
        raise NotImplementedError
