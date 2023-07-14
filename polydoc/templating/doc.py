from typing import Dict, List

import bs4

from .base import HtmlTemplate


class _DocHtmlTemplate(HtmlTemplate):

    def __init__(self):
        super().__init__('doc_template.html')
    
    def format(
            self,
            index: str,
            project_name: str,
            subprojects: Dict[str, str],
            all_source_files: List[str],
            item_name: str,
            item_kind: str,
            item_source: str,
            item_line_no: int,
            doc_string: str,
            ) -> str:

        tag: bs4.Tag = self.soup.findAll(id='projectName')[0]
        tag.clear()
        tag.href = index
        tag.string = project_name or 'anonymous project'

        tag: bs4.Tag = self.soup.findAll(id='projectVersion')[0]
        tag.clear()
        for subp, ver in subprojects.items():
            tag.append(bs4.BeautifulSoup(f'<small><b>{subp}</b> v{ver}</small><br />', 'html.parser'))

        tag: bs4.Tag = self.soup.findAll(id='sourceTree')[0]
        tag.clear()
        for name, href in all_source_files:
            tag.append(bs4.BeautifulSoup(f'<li><a href="{href}">{name}</a></li>', 'html.parser'))

        tag: bs4.Tag = self.soup.findAll(id='itemNameAndKind')[0]
        tag.clear()
        tag.string = f'{item_kind} {item_name}'

        tag: bs4.Tag = self.soup.findAll(id='sourceFileLink')[0]
        tag.attrs['href'] = f'{item_source}#l{item_line_no}'
        tag.string = f'{item_source} at line {item_line_no}'

        tag: bs4.Tag = self.soup.findAll(id='docString')[0]
        tag.clear()
        tag.append(bs4.BeautifulSoup(doc_string, 'html.parser'))

        return self.soup.prettify(None)


format_doc_as_html = _DocHtmlTemplate().format
