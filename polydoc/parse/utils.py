from typing import Tuple


def measure_indent(line: str, indent_char=None) -> Tuple[int, str]:
    if line.startswith(' '):
        _indent_char = ' '
    elif line.startswith('\t'):
        _indent_char = '\t'
    else:
        return indent_char, 0
    
    if indent_char is None:
        indent_char = _indent_char
    else:
        assert indent_char == _indent_char, f'mismatched indents! ({indent_char!r} vs {_indent_char!r} in {line!r})'
    
    indent = 0
    for c in line:
        if c == indent_char:
            indent += 1
        else:
            break
    return indent_char, indent
