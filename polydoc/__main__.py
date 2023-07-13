import sys
import argparse
from typing import List

from .project import Project


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, nargs='*')
    parser.add_argument('--name', '-n', type=str)
    parser.add_argument('--dir', '-d', type=str, nargs='*')
    parser.add_argument('--root', type=str, default='.', help='Project root, location to which all paths are relative.')
    args = parser.parse_args()

    if args.dir and len(args.dir) == 1 and not args.root:
        args.root = args.dir[0]
    
    if not args.dir and not args.file and args.root:
        args.dir = [args.root]
    
    return args


def main(files: List[str], dirs: List[str], project_name: str, root: str):
    project = Project(project_name, root)
    files = files or []
    for fn in files:
        project.parse(fn)
    dirs = dirs or []
    for dir in dirs:
        project.parse(dir)
    project.organise_links()
    project.draw()


if __name__ == '__main__':
    args = parse_args()
    sys.exit(main(args.file, args.dir, args.name, args.root))