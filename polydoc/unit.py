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
        self.links = []
        self.language = language

        for m in self.LINK_REGEX.finditer(self.doc):
            href = m.group(1) or m.group(2)
            # if '|' not in href:
            #     href = self.source_file_path + '|' + href
            self.links.append(href)

    
    @property
    def ident(self) -> str:
        return f'{self.source_file_path}|{self.kind}:{str(self)}'.replace('__doc__', '').rstrip(':')
    
    def __str__(self) -> str:
        return f'{self.parent.name}/{self.name}' if self.parent is not None else self.name