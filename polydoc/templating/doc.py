from typing import Dict, List

import bs4

from ..source_tree import SourceFileTree
from ..module_tree import ModuleTree
from .base import HtmlTemplate


class _DocHtmlTemplate(HtmlTemplate):

    def __init__(self):
        super().__init__('doc_template.html')
    
    def format(
            self,
            index: str,
            project_name: str,
            subprojects: Dict[str, str],
            all_source_files: SourceFileTree,
            all_modules: ModuleTree,
            item_name: str,
            item_kind: str,
            item_source: str,
            item_line_no: int,
            doc_string: str,
            ) -> str:
        self.set_title(f'{item_name} - {project_name}')
        self.set_project_name(project_name, index, subprojects)
        self.set_source_tree(all_source_files)
        self.set_module_tree(all_modules)

        self.set_text(id='itemNameAndKind', text=f'{item_kind} {item_name}')

        self.set_link(
            id='sourceFileLink',
            href=f'{item_source}#l{item_line_no}',
            text=f'{item_source} at line {item_line_no}'
        )
        
        self.set_text(id='docString', text=doc_string)

        return self.soup.prettify(None)


format_doc_as_html = _DocHtmlTemplate().format
