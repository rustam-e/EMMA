# TO DO:

# split evolution state management into pure functions - redux - like

# every function should listen to the change in state and react to it - like in redux - including the mutation, evaluation and other functions - they can do it sequentially or otherwise - they're reacting to changes in the world and acting upon it, not being triggered by the world

# the onChange could be sequential - like a single async function or parallel

# world -> evolution -> world.

# state (with intialization) -> variance + evaluation + selection + adaptive hyper parameter adaptation

# hyper paramater adaptation of variance hyper parameters by keeping the hyper parameters as fields of the individual in population as well as variance algorithm itself and having the variance function respect it.

a dynamic, adaptive system - with complexity just a matter of population size and their interaction capabilities

# hyper parameter adaptation in selection as a property of population and the algorithm

# feat - update evolution functions to run in parallel - e.g. mutation function updating a population while another selection function is acting upon a different population subset or even on the same items within a given population

# it should have shared state

# the state updates should be pure functions - like redux - for debuggability

# nice debugging tools like redux tools could be great.

# test it with stateful functions

# feat - udpate tests to test for meta-evolution

# implement an example evolution algorithm using my framework - perhaps my story builder

# and then can implement data analysis for meta evolution to understand the important hyper parameters and their performance on a given problem

# and then run it and analyze data of the algorithm performance on different problems.

---

# fix: turn evolution int oa papckage

# reformat codebase to use evolution properly

# fix: add some unit tests with mocks of the open ai api - especially for all the supplementary logic like utils

## fix: write a test for termination condition when the task is completed

## fix: write a test to validate that user exit signals are working in terminating the run of the program

# fix: update graph structure to make improvement strategy a field on an edge

# fix: improve visuzliaion logic to make more beautiful graphs

# fix: the evaluator should not be overly optimistic

# fix: add e2e tests actually running against the api to validate that the flow is successfully generating the graph structure as expected

---

# 1 system to generate 1 prompt to achieve 1 objective.

# agent - receives objective, produces output

# evaluator - receives agent's output and objective and evaluates it - pure, stateless, non contextual, non long-running progress, just 1 optimal prompt for a given objective

# The a\* algorithm chooses the next node (agent) to explore

# The mutator receives the agent, the mutation prompt, the objective and the evaluation. Mutator generates a mutation prompt. Mutation prompt receives agent prompt and updates it -outputs new agent

# Loop is completed
