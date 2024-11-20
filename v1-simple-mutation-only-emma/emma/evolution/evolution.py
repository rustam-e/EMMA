from typing import Callable, TypeVar, Any, Union, Awaitable, Optional
import asyncio
from .state_manager.state_manager import StateManager

# Define generic type variables
State = TypeVar('State')
InitializationOutput = TypeVar('InitializationOutput')
VarianceOutput = TypeVar('VarianceOutput')
EvaluationOutput = TypeVar('EvaluationOutput')
SelectionOutput = TypeVar('SelectionOutput')
EvolveOutput = TypeVar('EvolveOutput')

HyperParameters = TypeVar('HyperParameters', bound=Any)

def is_awaitable(obj):
    return isinstance(obj, Awaitable)

def run_if_awaitable(func, *args):
    result = func(*args)
    if is_awaitable(result):
        return asyncio.run(result)
    return result

def evolution(
    evolve: Callable[[State, SelectionOutput, Optional[HyperParameters]], Union[EvolveOutput, Awaitable[EvolveOutput]]],
    initialize_population: Callable[[State, Optional[HyperParameters]], Union[InitializationOutput, Awaitable[InitializationOutput]]],
    introduce_variance: Callable[[State, InitializationOutput, Optional[HyperParameters]], Union[VarianceOutput, Awaitable[VarianceOutput]]],
    evaluate_population: Callable[[State, VarianceOutput, Optional[HyperParameters]], Union[EvaluationOutput, Awaitable[EvaluationOutput]]],
    select_survivors: Callable[[State, EvaluationOutput, Optional[HyperParameters]], Union[SelectionOutput, Awaitable[SelectionOutput]]],
    get_hyper_parameters: Callable[[], Union[HyperParameters, Awaitable[HyperParameters]]],
    initial_state: State
) -> EvolveOutput:
    # set up state - set to initial empty values
    # set evolution configuration
    # decorate functtions to be able to update the relevant parts of the state
    # pass the state and decorated functions to the evolution_runner
    # the functions should be reactive to state changes - e.g. we should be able to have onStateChange function passed as argument that could mutate the state
    # in evolution_runner, set up stop conditions, and run the intialize population, variance, evaluation, and survivor selection functions until a stop condition is met
    


    # initialize state - some configs that the function receives, - pprobably with hypperparameters and population and evolution config like whether it's parallel or not or how many instances of the evolve function to run in parallel
    # decorate argument functions to be able to update state by triggering actions on the state - so that when they're called they're not only returning the output but also updating the state
    # pass the decorated functions to the evolve argument and return it - evolve argument is a function which handles the running of the evolution itself. It accepts state and decorated functions and runs them
    # it can run them sequentially or in prallel, it can 

    state_manager = StateManager(initial_state)

    hyper_parameters = run_if_awaitable(get_hyper_parameters)

    def update_state(state, output):
        def update_fn(current_state):
            return output.new_state
        state_manager.update_state(update_fn)
        return state_manager.get_state()

    population = run_if_awaitable(initialize_population, state_manager.get_state(), hyper_parameters)
    state = update_state(state_manager.get_state(), population)

    varied_population = run_if_awaitable(introduce_variance, state, population.output, hyper_parameters)
    state = update_state(state, varied_population)

    evaluated_population = run_if_awaitable(evaluate_population, state, varied_population.output, hyper_parameters)
    state = update_state(state, evaluated_population)

    survivors = run_if_awaitable(select_survivors, state, evaluated_population.output, hyper_parameters)
    state = update_state(state, survivors)

    evolved_population = run_if_awaitable(evolve, state, survivors.output, hyper_parameters)

    async def run_state_manager():
        await state_manager.run()

    asyncio.run(run_state_manager())

    return evolved_population
