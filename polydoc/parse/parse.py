from typing import List, Dict, Tuple
import os

from ..unit import Unit
from .python import parse_python_file
from .javascript import parse_javascript_file


PARSERS = dict(
    py=parse_python_file,
    js=parse_javascript_file,
)


def parse(fn_or_dn: str, relative_to: str, file_list: List[str]) -> Dict[str, Unit]:
    if os.path.isfile(fn_or_dn):
        return parse_file(fn_or_dn, relative_to, file_list)
    elif os.path.isdir(fn_or_dn):
        return parse_dir(fn_or_dn, relative_to, file_list)
    else:
        # f'{fn_or_dn} is not a file or a directory.'
        pass


def parse_dir(dn: str, relative_to: str, file_list: List[str]) -> Dict[str, Unit]:
    rv = {}
    for root, _, files in os.walk(dn):
        for fn in files:
            fn = os.path.join(root, fn)
            rv.update(parse_file(fn, relative_to, file_list))
    return rv


def parse_file(fn: str, relative_to: str, file_list: List[str]) -> Dict[str, Unit]:

    ext = os.path.splitext(fn)[1].lower()[1:]

    if ext in PARSERS:
        file_list.append(os.path.relpath(fn, relative_to))
        return PARSERS[ext](fn, relative_to)
    else:
        return {}