from typing import Dict, List, Tuple
import os
import heapq
import signal
import time
import sys
from ai.ai import LangchainClient
from core.core import create_default_start_node, mutate, search
from models.models import Node, NodeType, Graph
from state.shared_state import shared_state
from utils.utils import visualize_graph
from utils.logger import logger

def reconstruct_path(came_from: Dict[str, str], current: str, graph: Graph) -> List[str]:
    total_path = [graph.nodes[current].prompt]
    while current in came_from:
        current = came_from[current]
        total_path.append(graph.nodes[current].prompt)
    logger.info(f"Reconstructing path: {' -> '.join(total_path)}")
    return total_path[::-1]


def a_star_search(client: LangchainClient, graph: Graph, start_prompt: str, objective_prompt: str, max_iterations: int = 10) -> List[str]:
    open_set = []
    start_node = graph.nodes.get(start_prompt) or graph.add_node(start_prompt, 0, NodeType.START)
    heapq.heappush(open_set, (-start_node.score, start_node.id))
    came_from: Dict[str, str] = {}
    g_score: Dict[str, float] = {start_node.id: 0}
    best_node = start_node

    logger.info(f"Starting A* search with objective: {objective_prompt}")

    iteration = 0
    while open_set and iteration < max_iterations:
        current_node_id = heapq.heappop(open_set)[1]
        current_node = graph.nodes[current_node_id]
        logger.info(f"Exploring node: {current_node.prompt[:100]}... with score: {current_node.score}")

        if current_node.score > best_node.score:
            best_node = current_node

        if current_node.score > 0.95:
            logger.info(f"Found high-scoring node: {current_node.prompt[:100]}... with score: {current_node.score}")
            return reconstruct_path(came_from, current_node.id, graph)

        new_node = search(client, graph, current_node, objective_prompt)
        if new_node:
            tentative_g_score = g_score[current_node.id] + 1
            if new_node.id not in g_score or tentative_g_score < g_score[new_node.id]:
                came_from[new_node.id] = current_node.id
                g_score[new_node.id] = tentative_g_score
                f_score = tentative_g_score - new_node.score  # Negative because we want to maximize score
                heapq.heappush(open_set, (f_score, new_node.id))

        iteration += 1

    logger.info(f"A* search completed after {iteration} iterations")
    return reconstruct_path(came_from, best_node.id, graph)


def load_existing_graph(client: LangchainClient, filename: str = "graph_state.json") -> Tuple[Graph, Node]:
    if os.path.exists(filename):
        graph = Graph.load_from_file(filename)
        logger.info(f"Loaded existing graph from {filename}")
        
        start_nodes = [node for node in graph.nodes.values() if node.node_type == NodeType.START]
        if start_nodes:
            start_node = max(start_nodes, key=lambda node: node.score)
        else:
            logger.info("No start node found in existing graph. Creating a new start node.")
            start_node = create_default_start_node(client, graph, "Create a captivating fairy tale with a moral lesson.")
        
        logger.info(f"Using start node: {start_node.agent_prompt[:100]}... with score: {start_node.score}")
        
        return graph, start_node
    else:
        logger.info(f"No existing graph found at {filename}. Creating a new graph with a default start node.")
        graph = Graph()
        start_node = create_default_start_node(client, graph, "Create a captivating fairy tale with a moral lesson.")
        return graph, start_node

def reconstruct_full_story(graph: Graph) -> List[str]:
    start_node = next(node for node in graph.nodes.values() if node.node_type == NodeType.START)
    
    story = []
    visited = set()

    def dfs(node_id):
        if node_id in visited:
            return
        visited.add(node_id)
        node = graph.nodes[node_id]
        story.append(node.agent_output)  # Use agent_output instead of prompt
        for edge in graph.get_outgoing_edges(node_id):
            dfs(edge.to_node_id)

    dfs(start_node.id)
    return story


def signal_handler(signum, frame):
    if signum == signal.SIGINT:
        if not shared_state.PAUSE_FLAG:
            print("\nPausing the algorithm... (Press Enter to resume, Ctrl+C again to stop)")
            shared_state.PAUSE_FLAG = True
        else:
            print("\nStopping the algorithm...")
            shared_state.STOP_FLAG = True
            sys.exit(0)  # Exit the program when stopping

def setup_signal_handling():
    signal.signal(signal.SIGINT, signal_handler)

def main():
    # TO DO:
    #     
    # should_continue: Callable[[], bool],     
    # initialize_population: Callable[[], P],
    # introduce_variance: Callable[[P], P],
    # evaluate_population: Callable[[P], P],
    # select_survivors: Callable[[P], P] = 
    #

    client = LangchainClient()
    graph, start_node = load_existing_graph(client, "graph_state.json")
    
    objective_prompt = "Create a captivating fairy tale with a moral lesson."

    logger.info("Starting the story generation process")
    
    current_node_id = start_node.id
    logger.info(f"Starting with node ID: {current_node_id}")
    iteration = 0
    max_iterations = 10  # Set a maximum number of iterations

    try:
        while iteration < max_iterations and not shared_state.STOP_FLAG:
            if shared_state.PAUSE_FLAG:
                print("Algorithm paused. Press Enter to continue or Ctrl+C to stop.")
                try:
                    input()
                    shared_state.PAUSE_FLAG = False
                except KeyboardInterrupt:
                    print("\nStopping the algorithm...")
                    shared_state.STOP_FLAG = True
                    break
                continue

            if current_node_id not in graph.nodes:
                logger.error(f"Current node ID {current_node_id} not found in the graph. Resetting to start node.")
                current_node_id = start_node.id

            new_node = search(client, graph, graph.nodes[current_node_id], objective_prompt)
            
            if new_node:
                current_node_id = new_node.id
                logger.info(f"Created new node: {new_node.agent_output[:100]}...")
            else:
                logger.info("Failed to create a new node. Trying again...")
            
            iteration += 1
            time.sleep(1)  # Small delay to allow for user interruption

        if shared_state.STOP_FLAG:
            logger.info("Story generation stopped by user.")
        elif iteration >= max_iterations:
            logger.info("Reached maximum number of iterations.")
        else:
            logger.info("Story generation completed successfully.")

        story_path = reconstruct_full_story(graph)

        if story_path:
            print("Generated Story:")
            print("\n".join(story_path))
            graph.save_to_file("graph_state.json")
            visualize_graph(graph, "story_graph.png")
            logger.info("Story graph saved and visualized")
        else:
            print("No story generated or algorithm interrupted")

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    finally:
        print("Exiting the program.")

if __name__ == "__main__":
    setup_signal_handling()
    main()