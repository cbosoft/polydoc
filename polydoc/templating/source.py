from typing import Dict, List

import bs4

from .base import HtmlTemplate


class _SourceHtmlTemplate(HtmlTemplate):

    def __init__(self):
        super().__init__('source_template.html')
    
    def format(
            self,
            index: str,
            project_name: str,
            subprojects: Dict[str, str],
            all_source_files: List[str],
            source_file_path: str,
            source_code: str,
            ) -> str:
        tag: bs4.Tag = self.soup.findAll(id='sourceFileName')[0]
        tag.clear()
        tag.href = index
        tag.string = source_file_path

        tag: bs4.Tag = self.soup.findAll(id='projectName')[0]
        tag.clear()
        tag.string = project_name or 'anonymous project'

        tag: bs4.Tag = self.soup.findAll(id='projectVersion')[0]
        tag.clear()
        for subp, ver in subprojects.items():
            tag.append(bs4.BeautifulSoup(f'<small><b>{subp}</b> v{ver}</small><br />', 'html.parser'))

        tag: bs4.Tag = self.soup.findAll(id='sourceTree')[0]
        tag.clear()
        for name, href in all_source_files:
            tag.append(bs4.BeautifulSoup(f'<li><a href="{href}">{name}</a></li>', 'html.parser'))

        plain_source_lines = source_code.split('\n')
        linked_source_code = []
        line_numbers = []
        for line_no, line in enumerate(plain_source_lines, 1):
            line = line.rstrip('\n')
            link_open = f'<a id="l{line_no}" class="lineNum">'
            link_close = '</a>'
            line = f'{link_open}{line_no}{link_close}{line}\n'
            line = bs4.BeautifulSoup(line, 'html.parser')
            linked_source_code.append(line)
            line_numbers.append(line_no)
        
        for i in range(1, len(line_numbers)+1):
            if not plain_source_lines[-i]:
                linked_source_code.pop(-i)
                line_numbers.pop(-i)
            else:
                break
        
        tag: bs4.Tag = self.soup.findAll(id='sourceCode')[0]
        tag.clear()
        for line in linked_source_code:
            tag.append(line)

        return self.soup.prettify(None)


format_source_as_html = _SourceHtmlTemplate().format
