import os
from typing import Dict
import re

import networkx as nx
from matplotlib import pyplot as plt

from .unit import Unit
from .parse import parse
from .parse.utils import markdown2html
from .templating import format_source_as_html, format_doc_as_html


class Project:

    LANGUAGE_COLOURS = {
        'Python': '#1472de',
        'Javascript': '#f59714',
    }

    LINK_PARTS_RE = re.compile(r'(?:([\w\d\/\.]+)\|)?(?:(\w+):)?([\w\d]+)')

    def __init__(self, name: str, root: str):
        self.name = name
        self.subprojects = {}
        self.root = root
        self.graph = nx.DiGraph()
        self.links = {}
        self.sources = []
    
    def parse(self, fn: str):
        if self.name is None:
            self.name = os.path.basename(self.root)
        nodes = parse(fn, relative_to=os.path.dirname(self.root), file_list=self.sources)
        for nodekey, unit in nodes.items():
            self.graph.add_node(nodekey, unit=unit)
            if unit.parent is not None:
                self.graph.add_edge(nodekey, unit.parent.ident, kind='heritage')
            for srck, href in unit.links.items():
                self.links[(nodekey, srck)] = href
    
    def guess_subprojects(self):
        versions = []
        version_re = re.compile('.*(?:let|var|const)?\\s*version(?::\\s?\\w+)?\\s*=\\s+[\'"](.*)[\'"];?.*')
        relto = os.path.dirname(self.root)
        for source in self.sources:
            if 'version' in source or 'Cargo.toml' in source:
                with open(os.path.join(relto, source)) as f:
                    contents = f.read().lower()
                    m = version_re.match(contents)
                    if m:
                        v = m.group(1)
                        if v.startswith('v'):
                            v = v[1:]
                        versions.append((source, v))

        unnamed_projects = [p for p, _ in versions]
        named_projects = []
        level = 0
        while unnamed_projects:
            parts = [up.split('/')[level] for up in unnamed_projects]
            for i, part in reversed(list(enumerate(parts))):
                count = parts.count(part)
                if count > 1:
                    continue
                unnamed_projects.pop(i)
                named_projects.append((part, versions[i][1]))
            level += 1
        
        for name, version in named_projects:
            self.subprojects[name] = version

    
    def organise_links(self):
        for (src, srck), link in self.links.items():
            print(f'LINK {src}->{link}')
            if link in self.graph.nodes:
                continue
            
            m = self.LINK_PARTS_RE.match(link)
            print('MATCH', m.groups())
            path, kind, name = m.groups()
            if name == 'Module':
                kind = name
                name = None
            
            path = path or r'[\/\w\.\d]+'
            kind = kind or r'\w+'
            name = name or r'[\d\w]+'
            
            potential_name_re = re.compile(f'^{path}\\|{kind}:{name}$')
            potential_nodes = sorted([
                node for node in self.graph.nodes
                if potential_name_re.match(node)
            ], key=lambda s: len(s))

            if potential_nodes:
                self.links[(src, srck)] = potential_nodes[0]
        
        for (u, _), v in self.links.items():
            if not self.graph.has_edge(u, v):
                self.graph.add_edge(u, v, kind='link')


    def draw(self):
        loc = nx.layout.spring_layout(self.graph)
        units: Dict[str, Unit] = nx.get_node_attributes(self.graph, 'unit')
        node_colours = [
            self.LANGUAGE_COLOURS[units[node].language] if node in units else '#AAAAAA'
            for node in self.graph.nodes
        ]

        edge_kinds = [
            nx.get_edge_attributes(self.graph, 'kind')[e]
            for e in self.graph.edges
        ]
        heritage_edges = [e for e, k in zip(self.graph.edges, edge_kinds) if k == 'heritage']
        link_edges = [e for e, k in zip(self.graph.edges, edge_kinds) if k == 'link']
        nx.draw_networkx_edges(self.graph, loc, heritage_edges, arrows=True)
        nx.draw_networkx_edges(self.graph, loc, link_edges, arrows=False, edge_color='#CCCCCC')
        nx.draw(self.graph, loc, node_color=node_colours, edgelist=[], with_labels=True)
        
        plt.axis('off')
        plt.gca().set_aspect('equal')
        plt.tight_layout()
        plt.show()

    def html_for_source(self, source_file: str) -> str:
        fp_source = os.path.join(os.path.dirname(self.root), source_file)
        with open(fp_source) as f:
            contents = f.readlines()
        for unit in nx.get_node_attributes(self.graph, 'unit').values():
            unit_path = os.path.relpath(unit.path, os.path.dirname('polydoc/sources/'+source_file))
            print(unit.source_file_path, source_file, unit_path)
            if unit.source_file_path == source_file:
                contents[unit.line_no - 1] = f'<a id="l{unit.line_no}" href="{unit_path}">' + contents[unit.line_no - 1] + '</a>'
        contents = ''.join(contents)
        return format_source_as_html(
            index=os.path.relpath('polydoc/sources/' + os.path.dirname(self.root) + '/index.html', source_file),
            project_name=self.name,
            subprojects=self.subprojects,
            all_source_files=[],
            source_file_path=source_file,
            source_code=contents,
        )
    
    def get_doc_fixed_links_html(self, unit: Unit) -> str:
        this_node_links = {
            srck: href
            for (src, srck), href in self.links.items()
            if src == unit.ident
        }
        unit_doc = unit.doc
        for srck, href in this_node_links.items():
            href_unit = nx.get_node_attributes(self.graph, 'unit')[href]
            local_href = href_unit.path
            local_href = os.path.relpath(local_href, os.path.dirname(unit.path))
            link = f'<a href="{local_href}">{href_unit.name}</a>'
            unit_doc = unit_doc.replace(srck, link)
        unit_doc = markdown2html(unit_doc)
        print(repr(unit_doc))
        return unit_doc
    
    def html_for_doc(self, unit: Unit) -> str:
        unit_doc = self.get_doc_fixed_links_html(unit)
        source_path = os.path.relpath(f'polydoc/sources/{unit.source_file_path}.html', os.path.dirname(unit.path))
        return format_doc_as_html(
            index=os.path.relpath('polydoc/sources/' + os.path.dirname(self.root) + '/index.html', unit.path),
            project_name=self.name,
            subprojects=self.subprojects,
            all_source_files=[],
            item_name=unit.name,
            item_kind=unit.kind,
            item_source=source_path,
            item_line_no=unit.line_no,
            doc_string=unit_doc,
        )
    
    def write_documentation(self):
        files = {}
        for source_file in self.sources:
            files[f'polydoc/sources/{source_file}.html'] = self.html_for_source(source_file)
        
        units = nx.get_node_attributes(self.graph, 'unit')
        for unit in units.values():
            files[unit.path] = self.html_for_doc(unit)

        for filename, filecontents in files.items():
            filename = os.path.join(self.root, filename)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            print('WRITING', filename)
            with open(filename, 'w') as f:
                f.write(filecontents)
            
