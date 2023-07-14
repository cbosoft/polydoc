import os
from typing import Dict
import re

import networkx as nx
from matplotlib import pyplot as plt

from .unit import Unit
from .parse import parse


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
        self.links = []
        self.sources = []
    
    def parse(self, fn: str):
        nodes = parse(fn, relative_to=os.path.dirname(self.root), file_list=self.sources)
        for nodekey, unit in nodes.items():
            self.graph.add_node(nodekey, unit=unit)
            if unit.parent is not None:
                self.graph.add_edge(nodekey, unit.parent.ident, kind='heritage')
            for link in unit.links:
                self.links.append((nodekey, link))
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
        organised = []
        for (src, link) in self.links:
            print(f'LINK {src}->{link}')
            if link in self.graph.nodes:
                organised.append((src, link))
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
                organised.append((src, potential_nodes[0]))
        
        for u, v in organised:
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