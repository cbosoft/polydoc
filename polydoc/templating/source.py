from typing import Dict, List

from ..source_tree import SourceFileTree
from ..module_tree import ModuleTree
from .base import HtmlTemplate


class _SourceHtmlTemplate(HtmlTemplate):

    def __init__(self):
        super().__init__('source_template.html')
    
    def format(
            self,
            index: str,
            project_name: str,
            subprojects: Dict[str, str],
            all_source_files: SourceFileTree,
            all_modules: ModuleTree,
            source_file_path: str,
            source_code: str,
            ) -> str:
        self.set_title(f'{source_file_path} - {project_name}')
        self.set_project_name(project_name, index, subprojects)
        self.set_text(id='sourceFileName', text=source_file_path)
        self.set_source_tree(all_source_files)
        self.set_module_tree(all_modules)

        plain_source_lines = source_code.split('\n')
        linked_source_code = []
        line_numbers = []
        for line_no, line in enumerate(plain_source_lines, 1):
            line = line.rstrip('\n')
            link_open = f'<a id="l{line_no}" class="lineNum">'
            link_close = '</a>'
            line = f'{link_open}{line_no}{link_close}{line}\n'
            linked_source_code.append(line)
            line_numbers.append(line_no)
        
        for i in range(1, len(line_numbers)+1):
            if not plain_source_lines[-i]:
                linked_source_code.pop(-i)
                line_numbers.pop(-i)
            else:
                break
        
        self.set_children(
            id='sourceCode',
            children=linked_source_code,
        )

        return self.soup.prettify(None)


format_source_as_html = _SourceHtmlTemplate().format
