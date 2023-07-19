from typing import Dict, Optional

from ..source_tree import SourceFileTree
from ..module_tree import ModuleTree
from .base import HtmlTemplate


class IndexTemplate(HtmlTemplate):

    def __init__(self):
        super().__init__('index_template.html')
    
    def format(
            self,
            project_name: str,
            subprojects: Dict[str, str],
            all_source_files: SourceFileTree,
            all_modules: ModuleTree,
            project_description: Optional[str],
    ) -> str:
        self.set_title(project_name)
        self.set_project_name(project_name, './index.html', subprojects)
        self.set_source_tree(all_source_files)
        self.set_module_tree(all_modules)
        if project_description:
            self.set_text('projectDescription', project_description)
        return self.soup.prettify(None)


format_index_as_html = IndexTemplate().format
