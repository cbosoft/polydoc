from typing import Optional
import re


class Unit:

    LINK_REGEX = re.compile(r'\[.*?\]\((.*?)\)|\[(.*?)\]')

    def __init__(self, name: str, kind: str, source_file_path: str, line_no: int, doc: str, parent: Optional[str] = None, language=None):
        self.name = name
        self.kind = kind
        self.source_file_path = source_file_path
        self.line_no = line_no
        self.doc = doc
        self.parent: Optional["Unit"] = parent
        self.links = {}
        self.language = language

        for m in list(reversed(list(self.LINK_REGEX.finditer(self.doc)))):
            href = m.group(1) or m.group(2)
            k = f'LINK-{len(self.links)}'
            self.doc = self.doc[:m.start()] + k + self.doc[m.end():]
            self.links[k] = href
    
    @property
    def ident(self) -> str:
        return f'{self.source_file_path}|{self.kind}:{str(self)}'.replace('__doc__', '').rstrip(':')
    
    @property
    def path(self) -> str:
        return f'polydoc/{self.source_file_path}.{self.name}.html'
    
    def __str__(self) -> str:
        return f'{self.parent.name}/{self.name}' if self.parent is not None else self.name