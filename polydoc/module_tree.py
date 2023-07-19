from typing import Dict, List, Tuple
import os

from .unit import Unit
import networkx as nx


class ModuleTree:

    def __init__(self, name=None, href=None):
        self.name = name
        self.href = href
        self.children = []

    @classmethod
    def recurse_graph(cls, gnode, graph: nx.DiGraph, parent: "ModuleTree", relative_to: str):
        unit: Unit = nx.get_node_attributes(graph, 'unit')[gnode]
        edge_attrs = nx.get_edge_attributes(graph, 'kind')
        child = ModuleTree(name=unit.name, href=os.path.relpath(unit.path, relative_to))
        parent.children.append(child)
        for (child_gnode, _) in graph.in_edges(gnode):
            if edge_attrs[child_gnode, gnode] == 'heritage':
                cls.recurse_graph(child_gnode, graph, child, relative_to)
    
    @classmethod
    def from_graph(cls, graph: nx.DiGraph, relative_to: str) -> "ModuleTree":
        root_nodes = [
            node for node in graph.nodes
            if not graph.out_edges(node)
        ]
        root = ModuleTree()
        for gnode in root_nodes:
            cls.recurse_graph(gnode, graph, root, relative_to)
        return root
    
    def to_html(self, running_path: str) -> str:
        html = ''
        if self.name is not None:
            assert self.href is not None
            html += f'<a href="{self.href}">{self.name}</a>'
        html += '<ul class="tree">'
        for child in self.children:
            html += f'<li class="node">' + child.to_html(running_path+'/'+child.name) + '</li>'
        html += '</ul>'
        return html


        