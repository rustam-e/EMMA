import heapq
import re
import logging
from typing import Optional, Tuple, List
from langchain_core.prompts import PromptTemplate

from ai.ai import LangchainClient
from models.models import Node, NodeType, Graph
from state.shared_state import shared_state
from utils.logger import logger

def evaluate(client: LangchainClient, agent_output: str, target_goal: str, context: str) -> Tuple[float, str]:
    logger.info(f"Evaluating output: {agent_output[:100]}... against goal: {target_goal}")

    evaluation_template = PromptTemplate.from_template(
        "Given the following context and goal, assess how well the new output continues to progress towards the goal.\n"
        "Context: {context}\n"
        "Goal: {goal}\n"
        "New output: {output}\n\n"
        "Provide a score from 0 to 1, where 1 is a perfect continuation that meets the goal, and 0 is completely irrelevant or contradictory. "
        "Your response should start with the numeric score, followed by your explanation. "
        "For example: '0.8 - This output continues the progress well and aligns with the goal because...'\n\n"
        "After your explanation, suggest a specific strategy to improve the output if the score is less than 1. "
        "Your suggestion should be prefixed with ```Improvement strategy: ```."
    )

    evaluation_prompt = evaluation_template.format(
        context=context,
        output=agent_output,
        goal=target_goal
    )

    try:
        response = client.complete(evaluation_prompt)
        logger.info(f"Evaluation response: {response}")

        match = re.match(r'^(\d+(\.\d+)?)', response.strip())
        if match:
            score = float(match.group(1))
            logger.info(f"Extracted evaluation score: {score}")
            
            # Extract improvement strategy
            strategy_match = re.search(r'Improvement strategy: (.+)$', response, re.MULTILINE)
            improvement_strategy = strategy_match.group(1) if strategy_match else response
            
            return min(max(score, 0), 1), response, improvement_strategy
        else:
            logger.error(f"Could not extract numeric score from evaluation response: {response}")
            return 0.0, response, ""
    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        return 0.0, str(e), ""

def create_default_start_node(client: LangchainClient, graph: Graph, objective_prompt: str) -> Node:
    logger.info(f"Creating starting agent prompt for: {objective_prompt}")

    starting_template = PromptTemplate.from_template(
        "Given the task: '{objective}', create an initial prompt for an AI agent to begin working on this task."
    )

    prompt_text = starting_template.format(objective=objective_prompt)

    try:
        agent_prompt = client.complete(prompt_text)
        logger.info(f"Created default start node prompt: {agent_prompt}")
        
        # Generate initial output using the agent prompt
        initial_output = client.complete(agent_prompt)
        
        score, evaluation, improvement_strategy = evaluate(client, initial_output, objective_prompt, "")
        new_node = graph.add_node(agent_prompt=agent_prompt, agent_output=initial_output, score=score, evaluation=evaluation, improvement_strategy=improvement_strategy, node_type=NodeType.START)
        graph.save_to_file("graph_state.json")
        return new_node    
    except Exception as e:
        logger.error(f"Langchain error during prompt creation: {e}")
        return Node(agent_prompt="Error creating start node", agent_output="", score=0, node_type=NodeType.START)

def generate_mutation_prompts(client: LangchainClient, node: Node, objective_prompt: str, num_prompts: int = 5) -> List[str]:
    base_template = PromptTemplate.from_template(
        "Based on the following evaluation and improvement strategy for a given AI agent, "
        "generate a specific mutation prompt to guide the AI in improving the story.\n\n"
        "Evaluation: {evaluation}\n"
        "Improvement strategy: {strategy}\n"
        "Overall objective: {objective}\n\n"
        "Mutation prompt:"
    )

    mutation_prompts = []
    for _ in range(num_prompts):
        prompt_text = base_template.format(
            evaluation=node.evaluation,
            strategy=node.improvement_strategy,
            objective=objective_prompt
        )
        try:
            mutation_prompt = client.complete(prompt_text).strip()
            mutation_prompts.append(mutation_prompt)
        except Exception as e:
            logger.error(f"Error generating mutation prompt: {e}")
            mutation_prompts.append("Improve the story segment")

    return mutation_prompts

def evaluate_multiple(client: LangchainClient, outputs: List[Tuple[str, str]], target_goal: str, context: str) -> List[Tuple[float, str, str, str, str]]:
    evaluation_template = PromptTemplate.from_template(
        "Given the following context and goal, assess how well each of the new outputs continues to progress towards the goal.\n"
        "Context: {context}\n"
        "Goal: {goal}\n"
        "{outputs}\n\n"
        "For each output, provide a score from 0 to 1, where 1 is a perfect continuation that meets the goal, and 0 is completely irrelevant or contradictory. "
        "Your response should be in the following format for each output:\n"
        "Output X:\nScore: [numeric score]\nExplanation: [your explanation]\nImprovement strategy: [specific strategy to improve the output]\n\n"
    )

    outputs_text = "\n".join([f"Output {i+1}: {output}" for i, (_, output) in enumerate(outputs)])
    
    evaluation_prompt = evaluation_template.format(
        context=context,
        outputs=outputs_text,
        goal=target_goal
    )

    try:
        response = client.complete(evaluation_prompt)
        logger.info(f"Evaluation response: {response}")

        evaluated_outputs = []
        for i, (prompt, output) in enumerate(outputs):
            output_evaluation = re.search(f"Output {i+1}:(.+?)(?=Output {i+2}:|$)", response, re.DOTALL)
            if output_evaluation:
                eval_text = output_evaluation.group(1)
                score_match = re.search(r'Score: ([\d.]+)', eval_text)
                explanation_match = re.search(r'Explanation: (.+)', eval_text)
                strategy_match = re.search(r'Improvement strategy: (.+)', eval_text)

                if score_match and explanation_match and strategy_match:
                    score = float(score_match.group(1))
                    explanation = explanation_match.group(1)
                    strategy = strategy_match.group(1)
                    evaluated_outputs.append((score, prompt, output, explanation, strategy))

        return evaluated_outputs
    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        return []

def mutate(client: LangchainClient, agent_node_id: str, objective_prompt: str, graph: Graph, num_prompts: int = 5, top_k: int = 3) -> Optional[str]:
    if shared_state.STOP_FLAG:
        return None

    from_node = graph.nodes.get(agent_node_id)
    if not from_node:
        logger.error(f"Node with ID {agent_node_id} not found in the graph")
        return None

    mutation_prompts = generate_mutation_prompts(client, from_node, objective_prompt, num_prompts)
    logger.info(f"Generated {len(mutation_prompts)} mutation prompts")

    mutation_outputs = []
    for mutation_prompt in mutation_prompts:
        logger.info(f"Mutating with agent node ID: {agent_node_id}, mutation prompt: {mutation_prompt}")
        mutation_template = PromptTemplate.from_template(
            "Given the task: '{objective}', and the current agent prompt: '{current_prompt}', {mutation_strategy}"
            "Provide a new agent prompt that incorporates this mutation."
        )

        prompt_text = mutation_template.format(
            objective=objective_prompt,
            current_prompt=from_node.agent_prompt,
            mutation_strategy=mutation_prompt
        )
        try:
            new_agent_output = client.complete(prompt_text)
            mutation_outputs.append((prompt_text, new_agent_output))
        except Exception as e:
            logger.error(f"Error generating output for mutation prompt: {e}")

    evaluated_options = evaluate_multiple(client, mutation_outputs, objective_prompt, from_node.agent_output)
    
    # Sort options by score in descending order and get top k
    top_k_options = heapq.nlargest(top_k, evaluated_options, key=lambda x: x[0])

    if top_k_options:
        best_option = top_k_options[0]
        new_node = graph.add_node(
            agent_prompt=best_option[1],
            agent_output=best_option[2],
            score=best_option[0],
            evaluation=best_option[3],
            improvement_strategy=best_option[4]
        )
        
        # Add edges for all top k options
        for option in top_k_options:
            graph.add_edge(from_node, new_node, option[1])  # Using the mutation prompt as the edge label
        
        graph.save_to_file("graph_state.json")
        logger.info(f"Created new node with prompt: {new_node.agent_prompt[:300]}... and output: {new_node.agent_output[:300]}... with score: {new_node.score}")
        return new_node.id
    else:
        logger.warning("No valid mutation options were generated")
        return None

def search(client: LangchainClient, graph: Graph, start_node: Node, objective_prompt: str) -> Optional[Node]:
    logger.info(f"Starting search from node: {start_node.agent_prompt[:30]}...")
    mutated_prompt = mutate(client, start_node.id, objective_prompt, graph)
    if mutated_prompt:
        new_node = graph.nodes[mutated_prompt]
        logger.info(f"Created new node with prompt: {new_node.agent_prompt[:300]}... and output: {new_node.agent_output[:300]}... with score: {new_node.score}")
        if new_node.score > 0.9:
            logger.info(f"Found high-scoring node with prompt: {new_node.agent_prompt[:300]}... and output: {new_node.agent_output[:300]}... with score: {new_node.score}")
            return new_node
    return None