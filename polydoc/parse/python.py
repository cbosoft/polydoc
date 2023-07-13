from typing import List, Dict
import os

from ..unit import Unit
from .utils import measure_indent


def _parse_blocks_from_python_file(filename: str, lines: List[str], line_no_offset=0, parent=None, parent_kind=None, lvl=0) -> Dict[str, List[str]]:

    log_indent = '  '*lvl
    print(log_indent, f'SCANNING BLOCK FROM LINE {line_no_offset}')

    def add_block():
        blocks[this_block] = dict(
            name=this_block,
            kind=this_kind,
            lines=[],
            source_file=filename,
            line_no=line_no_offset+i+1,
            parent=parent
        )


    blocks = {}
    last_block = None
    last_kind = None
    this_block = '__doc__'
    this_kind = 'Module'
    reading_doc = False
    n = len(lines)
    i = -1
    indent_char = indent = None
    while i < (n - 1):
        i += 1
        line = lines[i]
        if not line:
            pass
        elif line.startswith('def') or line.startswith('class'):
            indent = None
            if this_block in blocks and blocks[this_block]['lines']:
                last_block = this_block
                last_kind = this_kind
            this_kind, this_block = line[:-2].split(' ', 1)
            this_kind = {'def':'Function', 'class': 'Class'}.get(this_kind, this_kind)
            if parent_kind == 'Class' and this_kind == 'Function':
                this_kind = 'Method'
            this_block = this_block[:this_block.index('(')] if '(' in this_block else this_block
            add_block()
            print(log_indent, f'ADDING NEW BLOCK {this_kind} {this_block} CHILD OF {parent_kind} {parent}')
        elif this_block:
            if indent is None:
                try:
                    indent_char, indent = measure_indent(lines[i], indent_char)
                except:
                    pass
            
            sline = line.strip()
            has_docq = False
            q = None

            if sline.startswith('"""'):
                q = '"""'
                has_docq = True
            elif sline.startswith("'''"):
                q = "'''"
                has_docq = True
            
            if has_docq:
                if this_block not in blocks:
                    print(log_indent, f'LATE ADDING NEW BLOCK {this_kind} {this_block}, CHILD OF {parent}')
                    add_block()
                ssline = sline.replace(q, '')
                if ssline:
                    blocks[this_block]['lines'].append(ssline.strip())

                if reading_doc or (sline.endswith(q) and len(sline) > len(q)):
                    reading_doc = False
                    last_block = this_block
                    last_kind = this_kind
                    this_block = None
                    this_kind = None
                else:
                    reading_doc = True
            elif reading_doc:
                blocks[this_block]['lines'].append(line[indent:])
        elif indent is not None:
            # not reading doc, read rest of function
            j = n
            for j in range(i+1, n):
                _line = lines[j]
                if not _line.strip():
                    continue
                _, _indent = measure_indent(lines[j], indent_char)
                if _indent < indent:
                    break
            if j == n:
                s = slice(i, j+1)
                i = n
            else:
                s = slice(i, j)
                i = j-1
            _lines = [l[indent:] for l in lines[s]]
            blocks.update(_parse_blocks_from_python_file(filename, _lines, s.start, parent=last_block, parent_kind=last_kind, lvl=lvl+1))
            indent = None
    return blocks


def parse_python_file(filename: str, relative_to) -> Dict[str, Unit]:
    with open(filename) as f:
        lines = f.readlines()
    
    print(f'PARSING FILE {filename!r}')
    filename = os.path.relpath(filename, relative_to)
    
    blocks = _parse_blocks_from_python_file(filename, lines)

    units_by_blockname = {
        blockname: Unit(
                name=blockdata['name'],
                kind=blockdata['kind'],
                source_file_path=blockdata['source_file'],
                line_no=blockdata['line_no'],
                doc=''.join(blockdata['lines']),
                parent=blockdata['parent'],
                language='Python'
            )
        for blockname, blockdata in blocks.items()
    }

    for unit in units_by_blockname.values():
        if unit.parent is not None:
            unit.parent = units_by_blockname[unit.parent]
    
    units = {unit.ident: unit for unit in units_by_blockname.values()}
    return units