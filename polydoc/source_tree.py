from typing import Dict, List, Tuple
import os


class SourceFileTree:

    def __init__(self) -> None:
        self.directories: Dict[str, "SourceFileTree"] = {}
        self.files: Dict[str, Tuple[str, str]] = {}
    
    @classmethod
    def from_file_list(cls, list_of_files: List[str], relative_to: str) -> "SourceFileTree":
        root = cls()
        ptr = root
        for source_file in list_of_files:
            ptr = root
            *dirs, fn = source_file.split('/')
            for d in dirs:
                if d not in ptr.directories:
                    ptr.directories[d] = SourceFileTree()
                ptr = ptr.directories[d]
            ptr.files[fn] = (source_file, os.path.relpath(f'polydoc/sources/{source_file}.html', relative_to))
        return root
    
    def to_html(self, running_path: str) -> str:
        html = '<ul class="tree">'
        for dname, dtree in self.directories.items():
            html += f'<li class="node">{dname}' + dtree.to_html(running_path+'/'+dname) + '</li>'
        for fn, (sfn, href) in self.files.items():
            html += f'<li><a href="{href}">{fn}<a></li>'
        html += '</ul>'
        return html