import networkx as nx
import matplotlib.pyplot as plt
from models.models import Graph

def visualize_graph(graph: Graph, filename: str) -> None:
    G = nx.DiGraph()
    for node in graph.nodes.values():
        G.add_node(node.id, output=node.agent_output[:50] + "...", score=node.score, type=node.node_type.name)
    for edge in graph.edges:
        G.add_edge(edge.from_node_id, edge.to_node_id, mutation=edge.mutation_prompt)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(20, 20))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', 
            font_size=8, font_weight='bold', arrows=True)
    nx.draw_networkx_labels(G, pos, {node: f"{data['output']}\nScore: {data['score']:.2f}" 
                                     for node, data in G.nodes(data=True)})
    edge_labels = nx.get_edge_attributes(G, 'mutation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    plt.title("Story Generation Graph")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
