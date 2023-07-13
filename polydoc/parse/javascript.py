from typing import Dict
import os
import re

from ..unit import Unit

FUNCTION_RE = re.compile('\/\/\/([\s\S]*?)(?:export )?function (\w+) ?\(', re.MULTILINE)


def parse_javascript_file(filename: str, relative_to: str) -> Dict[str, Unit]:
    with open(filename) as f:
        contents = f.read()
    
    print(f'PARSING FILE {filename!r}')
    filename = os.path.relpath(filename, relative_to)

    units_by_blockname = {}
    for m in FUNCTION_RE.finditer(contents):
        doc, fname = m.groups()
        doc = doc.strip().replace('///', '').replace('//', '')
        line_no = contents[:m.end()].count('\n')

        units_by_blockname[f'{filename}@{line_no}|{fname}'] = Unit(
            fname, 'Function', filename, line_no, doc, None, language='Javascript'
        )
    
    return {unit.ident: unit for unit in units_by_blockname.values()}
