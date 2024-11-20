# import unittest
# from unittest.mock import Mock, patch
# from ai.ai import LangchainClient
# from core.core import Graph, Node, NodeType
# from state.shared_state import shared_state
# from utils.logger import logger

# class TestStoryGeneration(unittest.TestCase):
#     def setUp(self):
#         self.client = Mock(spec=LangchainClient)
#         self.graph = Graph()
#         self.start_node = self.graph.add_node("Start prompt", 0.5, NodeType.START)
#         self.objective_prompt = "Create a captivating fairy tale with a moral lesson."
#         self.max_iterations = 10

#     @patch('core.core.search')
#     def test_termination_on_high_score(self, mock_search):
#         # Mock the search function to return a high-scoring node on the third iteration
#         mock_search.side_effect = [
#             Node("Node 1", 0.6, NodeType.NORMAL),
#             Node("Node 2", 0.7, NodeType.NORMAL),
#             Node("High score node", 0.96, NodeType.NORMAL),
#         ]

#         story_path = self.generate_story()

#         self.assertIn("High score node", story_path)
#         self.assertEqual(mock_search.call_count, 3)
#         logger.info("Test passed: Story generation terminated on high score")

#     @patch('core.core.search')
#     def test_termination_on_max_iterations(self, mock_search):
#         # Mock the search function to always return a low-scoring node
#         mock_search.return_value = Node("Low score node", 0.5, NodeType.NORMAL)

#         story_path = self.generate_story()

#         self.assertEqual(len(story_path), self.max_iterations + 1)  # +1 for the start node
#         self.assertEqual(mock_search.call_count, self.max_iterations)
#         logger.info("Test passed: Story generation terminated on max iterations")

#     def generate_story(self):
#         current_node_id = self.start_node.id
#         story_path = [self.start_node.prompt]
#         iteration = 0

#         while iteration < self.max_iterations and not shared_state.STOP_FLAG:
#             new_node = search(self.client, self.graph, self.graph.nodes[current_node_id], self.objective_prompt)
            
#             if new_node:
#                 current_node_id = new_node.id
#                 story_path.append(new_node.agent_output)
                
#                 if new_node.score > 0.95:
#                     break
            
#             iteration += 1

#         return story_path

# if __name__ == "__main__":
#     unittest.main()
