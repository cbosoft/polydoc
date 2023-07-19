from typing import Tuple
import re


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


class _Markdown2HTML:

    MD_H1_RE = re.compile(r'^(#[^#](.*))$', re.MULTILINE)
    MD_H2_RE = re.compile(r'^(##[^#](.*))$', re.MULTILINE)
    MD_H3_RE = re.compile(r'^(###[^#](.*))$', re.MULTILINE)
    MD_H4_RE = re.compile(r'^(####[^#](.*))$', re.MULTILINE)
    MD_ITALIC_RE = re.compile(r'[^\*](\*(\w(?:.*?\w)?)\*)[^\*]?')
    MD_BOLD_RE = re.compile(r'[^\*](\*\*(\w(?:.*?\w)?)\*\*)[^\*]?')
    MD_CODE_RE = re.compile(r'(`(\w(?:.*?\w)?)`)')
    MD_PRE_RE = re.compile(r'(```(?:\w+)?([\s\S]*?)```)', re.MULTILINE)

    TRANSLATIONS = [
        (MD_H1_RE, 'h1', ''),
        (MD_H2_RE, 'h2', ''),
        (MD_H3_RE, 'h3', ''),
        (MD_H4_RE, 'h4', ''),
        (MD_ITALIC_RE, 'i', ''),
        (MD_BOLD_RE, 'b', ''),
        (MD_CODE_RE, 'code', ''),
        (MD_PRE_RE, 'pre', 'class="codeBlock"'),
    ]

    MD_UL_RE = re.compile(r'^((\s*-.*)+)', re.MULTILINE)

    def convert(self, markdown: str) -> str:
        html = markdown

        # TODO: paragraphs?

        html = html.replace('\n\n', '<p>')
        for regex, tag, attrs in self.TRANSLATIONS:
            for m in reversed(list(regex.finditer(html))):
                inner = m.group(2)
                if tag == 'pre':
                    inner = inner.replace('<', '&lt;').replace('>', '&gt;')
                html = html[:m.start(1)] + f'<{tag} {attrs}>' + inner + f'</{tag}>' + html[m.end(1):]
        
        for m in reversed(list(self.MD_UL_RE.finditer(html))):
            ul = m.group(1)
            html = html[:m.start(1)] + '<ul>\n  <li>' + '</li>\n  <li>'.join([i.lstrip()[1:].lstrip() for i in ul.split('\n')]) + f'</li>\n</ul>' + html[m.end(1):]

        return html


markdown2html = _Markdown2HTML().convert