import unittest
import asyncio
from typing import Any, List, Optional, Union, Awaitable
from parameterized import parameterized
from .evolution import evolution

# Mock functions for testing
def mock_initialize_population(hyper_params: Optional[Any] = None) -> Union[List[int], Awaitable[List[int]]]:
    result = [1, hyper_params['init_param'], 3] if hyper_params and 'init_param' in hyper_params else [1, 2, 3]
    print(f"mock_initialize_population with {hyper_params} -> {result}")
    return result

async def mock_initialize_population_async(hyper_params: Optional[Any] = None) -> List[int]:
    await asyncio.sleep(0.1)
    result = [1, hyper_params['init_param'], 3] if hyper_params and 'init_param' in hyper_params else [1, 2, 3]
    print(f"mock_initialize_population_async with {hyper_params} -> {result}")
    return result

def mock_introduce_variance(population: List[int], hyper_params: Optional[Any] = None) -> Union[List[int], Awaitable[List[int]]]:
    result = [x + hyper_params['var_param'] for x in population] if hyper_params and 'var_param' in hyper_params else [x + 1 for x in population]
    print(f"mock_introduce_variance with {population} and {hyper_params} -> {result}")
    return result

async def mock_introduce_variance_async(population: List[int], hyper_params: Optional[Any] = None) -> List[int]:
    await asyncio.sleep(0.1)
    result = [x + hyper_params['var_param'] for x in population] if hyper_params and 'var_param' in hyper_params else [x + 1 for x in population]
    print(f"mock_introduce_variance_async with {population} and {hyper_params} -> {result}")
    return result

def mock_evaluate_population(population: List[int], hyper_params: Optional[Any] = None) -> Union[List[int], Awaitable[List[int]]]:
    result = [x * hyper_params['eval_param'] for x in population] if hyper_params and 'eval_param' in hyper_params else [x * 2 for x in population]
    print(f"mock_evaluate_population with {population} and {hyper_params} -> {result}")
    return result

async def mock_evaluate_population_async(population: List[int], hyper_params: Optional[Any] = None) -> List[int]:
    await asyncio.sleep(0.1)
    result = [x * hyper_params['eval_param'] for x in population] if hyper_params and 'eval_param' in hyper_params else [x * 2 for x in population]
    print(f"mock_evaluate_population_async with {population} and {hyper_params} -> {result}")
    return result

def mock_select_survivors(population: List[int], hyper_params: Optional[Any] = None) -> Union[List[int], Awaitable[List[int]]]:
    result = [x for x in population if x > hyper_params['sel_param']] if hyper_params and 'sel_param' in hyper_params else [x for x in population if x > 4]
    print(f"mock_select_survivors with {population} and {hyper_params} -> {result}")
    return result

async def mock_select_survivors_async(population: List[int], hyper_params: Optional[Any] = None) -> List[int]:
    await asyncio.sleep(0.1)
    result = [x for x in population if x > hyper_params['sel_param']] if hyper_params and 'sel_param' in hyper_params else [x for x in population if x > 4]
    print(f"mock_select_survivors_async with {population} and {hyper_params} -> {result}")
    return result

async def mock_evolve(population: List[int], hyper_params: Optional[Any] = None) -> List[int]:
    await asyncio.sleep(0.1)
    result = [x - hyper_params['evo_param'] for x in population] if hyper_params and 'evo_param' in hyper_params else [x - 1 for x in population]
    print(f"mock_evolve with {population} and {hyper_params} -> {result}")
    return result

def mock_evolve_sync(population: List[int], hyper_params: Optional[Any] = None) -> List[int]:
    result = [x - hyper_params['evo_param'] for x in population] if hyper_params and 'evo_param' in hyper_params else [x - 1 for x in population]
    print(f"mock_evolve_sync with {population} and {hyper_params} -> {result}")
    return result

mock_hyper_params = {
    "init_param": 1,
    "var_param": 2,
    "eval_param": 3,
    "sel_param": 10,
    "evo_param": 5
}

# Hyperparameter functions
def get_hyper_params():
    return mock_hyper_params

async def get_hyper_params_async():
    await asyncio.sleep(0.1)
    return mock_hyper_params

class TestEvolution(unittest.TestCase):
    @parameterized.expand([
        ("all_sync", mock_initialize_population, mock_introduce_variance, mock_evaluate_population, mock_select_survivors, mock_evolve_sync, get_hyper_params, [10]),
        ("all_async", mock_initialize_population_async, mock_introduce_variance_async, mock_evaluate_population_async, mock_select_survivors_async, mock_evolve, get_hyper_params_async, [10]),
        ("mixed_sync_async", mock_initialize_population, mock_introduce_variance_async, mock_evaluate_population, mock_select_survivors_async, mock_evolve_sync, get_hyper_params, [10]),
        ("optional_hyperparams_sync", lambda hp=None: mock_initialize_population(), lambda p, hp=None: mock_introduce_variance(p), lambda p, hp=None: mock_evaluate_population(p), lambda p, hp=None: mock_select_survivors(p), lambda p, hp=None: mock_evolve_sync(p), get_hyper_params, [5,7]),
        ("optional_hyperparams_async", lambda hp=None: mock_initialize_population_async(), lambda p, hp=None: mock_introduce_variance_async(p), lambda p, hp=None: mock_evaluate_population_async(p), lambda p, hp=None: mock_select_survivors_async(p), lambda p, hp=None: mock_evolve(p), get_hyper_params_async, [5,7])
    ])
    def test_evolution(self, name, initialize_population, introduce_variance, evaluate_population, select_survivors, evolve, get_hyper_parameters, expected_result):
        hyper_parameters = get_hyper_parameters()
        if isinstance(hyper_parameters, Awaitable):
            hyper_parameters = asyncio.run(hyper_parameters)
        print(f"Hyperparameters: {hyper_parameters}")

        population = initialize_population(hyper_parameters)
        if isinstance(population, Awaitable):
            population = asyncio.run(population)
        print(f"Initialized Population: {population}")

        varied_population = introduce_variance(population, hyper_parameters)
        if isinstance(varied_population, Awaitable):
            varied_population = asyncio.run(varied_population)
        print(f"Varied Population: {varied_population}")

        evaluated_population = evaluate_population(varied_population, hyper_parameters)
        if isinstance(evaluated_population, Awaitable):
            evaluated_population = asyncio.run(evaluated_population)
        print(f"Evaluated Population: {evaluated_population}")

        survivors = select_survivors(evaluated_population, hyper_parameters)
        if isinstance(survivors, Awaitable):
            survivors = asyncio.run(survivors)
        print(f"Survivors: {survivors}")

        evolved_population = evolve(survivors, hyper_parameters)
        if isinstance(evolved_population, Awaitable):
            evolved_population = asyncio.run(evolved_population)
        print(f"Evolved Population: {evolved_population}")

        self.assertEqual(evolved_population, expected_result)

if __name__ == '__main__':
    unittest.main()
