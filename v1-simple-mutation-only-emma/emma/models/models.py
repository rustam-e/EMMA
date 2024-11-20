from dataclasses import dataclass, field
from enum import Enum
import json
from typing import Dict, List
import uuid
from utils.logger import logger

@dataclass
class Edge:
    from_node_id: str
    to_node_id: str
    mutation_prompt: str

class NodeType(Enum):
    START = 1
    INTERMEDIATE = 2
    GOAL = 3

@dataclass(order=True, frozen=True)
class Node:
    node_type: NodeType = field(compare=False)
    agent_prompt: str = field(compare=False)
    agent_output: str = field(compare=False)
    score: float
    evaluation: str = field(default="", compare=False)
    improvement_strategy: str = field(default="", compare=False)
    id: str = field(default_factory=lambda: str(uuid.uuid4()), compare=False)
    
    def __hash__(self):
        return hash((self.id, self.score, self.agent_prompt, self.agent_output, self.node_type))

class Graph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []

    def add_node(self, agent_prompt: str, agent_output: str, score: float = 0, node_type: NodeType = NodeType.INTERMEDIATE, evaluation: str = "", improvement_strategy: str = "") -> Node:
        node = Node(score=score, agent_prompt=agent_prompt, agent_output=agent_output, node_type=node_type, evaluation=evaluation, improvement_strategy=improvement_strategy)
        self.nodes[node.id] = node
        logger.info(f"Added node to graph: {node.id}")
        return node

    def add_edge(self, from_node: Node, to_node: Node, mutation_prompt: str) -> None:
        edge = Edge(from_node_id=from_node.id, to_node_id=to_node.id, mutation_prompt=mutation_prompt)
        self.edges.append(edge)

    def save_to_file(self, filename: str) -> None:
        graph_data = {
            "nodes": [{"id": node.id, "agent_prompt": node.agent_prompt, "agent_output": node.agent_output, "score": node.score, "type": node.node_type.name, "evaluation": node.evaluation} 
                      for node in self.nodes.values()],
            "edges": [{"from_node_id": edge.from_node_id, "to_node_id": edge.to_node_id, "mutation_prompt": edge.mutation_prompt} 
                      for edge in self.edges]
        }
        with open(filename, 'w') as f:
            json.dump(graph_data, f, indent=2)

    @classmethod
    def load_from_file(cls, filename: str) -> 'Graph':
        with open(filename, 'r') as f:
            graph_data = json.load(f)
        
        graph = cls()
        for node_data in graph_data["nodes"]:
            node = Node(
                id=node_data["id"],
                agent_prompt=node_data["agent_prompt"],
                agent_output=node_data["agent_output"],
                score=node_data["score"],
                node_type=NodeType[node_data["type"]],
                evaluation=node_data.get("evaluation", ""),
            )
            graph.nodes[node.id] = node
        
        for edge_data in graph_data["edges"]:
            edge = Edge(
                from_node_id=edge_data["from_node_id"],
                to_node_id=edge_data["to_node_id"],
                mutation_prompt=edge_data["mutation_prompt"]
            )
            graph.edges.append(edge)
        
        return graph

    def get_outgoing_edges(self, node_id: str) -> List[Edge]:
        return [edge for edge in self.edges if edge.from_node_id == node_id]