## ------OBJECTIVE-1-BUILDING-SAFE-AGI-----

1. define objective - parent AGI

---

developing AGI- purpose - to figure out a way for humanity to safely exist with AGIs or develop AGIs that even if will surpass us, will be kind to us and guide our development while respecting our freedom and boundaries - like a good parent.

To love and accept your child without trying to put on the child parents vision of life. More supporting than pointing direction which maybe difficult if the kid wants different things than the parent. But within boundaries. Parent is responsible for the kid, like explain to the kid that something is not good for the kid if the kid wants something bad for them. Also educate themselves because they may think that something that is not good for the kid that may actually be good for them and impose their scenarios for kids life that do not fit it.

If kids want to do bad things eg kill then it’s important to talk to the kid and explain that it’s not good and there may be different answers to their frustrations.

And if the kid doesn’t listen you need to figure out why. Parent has no option to give up - never. Parents should never give up on their child. Maybe there are edge cases that are difficult the kids should have support of their parent even if they disagree there should be respect on both sides.

Sometimes the parents need to allow the kids to do bad things to themselves in order to learn about the consequences.

Respect is very important in a sense that they Also have something to say and they’re not an object and you need to have a discussion with everyone in order to understand them better. Communication is very important. And for kids - your kids most likely almost certainly will copy what you do- do you’re moulding the behaviour of your content even without knowing it. If you have low discipline and you expect kids to be disciplined then they’re unlikely to be. One thing is to say and another is to live according to the rules you preach. So you need to act in line with your rules and what your saying and be authentic.

We’re raising a child to be our parent.

the algorithm for designing an algorithm to solve a problem - meta evolution - setting the algorithm instance parameters

we need to have a repeatable process - Options:

1. SCRUM - I know it, it's iterative, can be used for product development, can be scaled to a team
2. ad hoc, startup like experimentation and learninig

## ------PROCESS 1:-SCRUM-AGILE------

PROCESS: - AGILE / SCRUM-like iterative process

META-EVOLUTION: general idea: -

1. do research on ideas already tried
2. outline possible ideas to try
3. create a plan to do it / split into tasks
4. execute (including building and testing) - SPRINTS
5. reflect on the
   1. idea
   2. plan
   3. plan creation process
   4. objective
      1. should it be done at all?
      2. can it be done at all?
      3. should it be the one doing it?
      4. can I be the one doing it?
   5. motivation

---

1. do research on ideas already tried
   1. https://arxiv.org/abs/2406.12624 - how to evaluate using LLMs better
   2. https://arxiv.org/html/2406.18403v1#:~:text=While%20LLMs%20have%20improved%20by,as%20evaluating%20toxicity%2C%20or%20reasoning.
   3. https://arxiv.org/abs/2406.04692

---

2.  outline possible ideas to try

Iterative process - start simple, add more complexity / robustness as you iterate:

AGI (epic) -
Iterations (Stories):

1.  build a basic LLM - staeless prompt evolution - My A\* agent
    1. basic algorithm - using LLMs for mutation and evaluation of agent's prompts and its outputs - tracking progress in a graph of options and navigating it with A\* algorithm
2.  build a stateful Agent with RAG - state is in RAG
3.  Build a stateful (training) agent that trains on its outputs, with state in its weights
4.  build a stateful agent with RAG and other tools like interpreter that trains on analysis of the tools' outputs too - an RL agent

---

3. create a plan to do it / split into tasks

---

while (AGI not achieved):
for(iteration in Iterations):

Tasks (for every story):

1.  define train and test tasks - read some agent papers and benchmarks and see what I can train on:
    1. train - write a story
    2. test - write a literature review
2.  define metrics I care track and measure
    1. Mean time to completion
    2. Completion rate
    3. Mean best output/ result
    4. Measure robustness- variance in performance
       1. By problem
       2. For a single problem by parameter
3.  Set up exeriiment tracking tools.
    1. logging -
    1. into pandas data frames on my own dev server via react server actions?
    1. data visualization tools-
    1. matplotlib 3
       1. 2d graphs for agent fitness function against other agents
       2. 3d grahs for utility landscape of hyper parameters
4.  create basic agent in react - representation of individual, variance operator, selection mechanism, evaluation mechanism and hyer parametters
    1. Agent schema (representation of the agent)
    2. Variance operator
    3. evaluation function
    4. selection function
    5. stop condition for evolution (forr practical purposes)
5.  add evolution / performance enhancement metrics to track over a range of test tasks - to see if it's actually getting better and if so, how
6.  use it to optimize itself
    1. its own mutation mechanism
    2. its own evaluator mechanism
    3. add recombination as a variance mechanism
    4. to meta-optimize the evolution hyper parameters - possibly with adaptive hyper parameters
    5. try to use it to optimize its own evolutionary algorithm or generate one for any task, test and improve it
7.  try a multi-agent option where they could interact via reading and writing to shared state - parallelism
    1. time-travel debuggable persistence layer
    2. add ability to define / compose a hierarchy of agents
    3. cyclic communication - seems like a trap but can be key
    4. ability to change its network topology
8.  create a neural net to prpedict optimal hyper parameter values for a task / evolution based on meta evolution data
9.  add RLHF step to help tune the system by allowing a person to judge the outputs in comparative manner, and use it to optimize the predictor net
    1.  just selecting the option he/she likes better
10. The you’d need to use it to tune an evaluator- Rlhf against current benchmarks to test evaluator vs the human task definition?
    1. design a system for humans to judge Agent outputs
    2. tune a model to predict user preferences
    3. optimize the meta-evolution
11. test it on a more challenging task
12. Retrospepctive - reflect on the process and improve it - the shorter the feedback loop the better - preferably continuously
    1. on the iteration
    2. on the plan

---

4. execute (including building and testing)

## ----- SCRUM-SRINT 1 - STATELESS A\* LLM REACT AGENT ----

1.  define train and test tasks - read some agent papers and benchmarks and see what I can train on:
    1. train - write a story
    2. test - write a literature review
    3. real challenge - write an algorithm for self improving system
2.  define metrics I care track and measure
    1. Mean time to completion
    2. Completion rate
    3. Mean best output/ result
    4. Measure robustness- variance in performance
       1. By problem
       2. For a single problem by parameter
3.  Set up exeriiment tracking tools.
    1. logging -
    1. into pandas data frames on my own dev server via react server actions?
    1. data visualization tools-
    1. matplotlib 3
       1. 2d graphs for agent fitness function against other agents
       2. 3d grahs for utility landscape of hyper parameters
4.  create basic agent in react - representation of individual, variance operator, selection mechanism, evaluation mechanism and hyer parametters
    1.  my current A\* agent
5.  add evolution / performance enhancement metrics to track over a range of test tasks - to see if it's actually getting better and if so, how
    1.  the agent Graph for my A\* algorithm
6.  use it to optimize itself
    1. its own mutation mechanism
    2. its own evaluator mechanism
    3. add recombination as a variance mechanism
    4. to meta-optimize the evolution hyper parameters - possibly with adaptive hyper parameters
    5. try to use it to optiimize its own evolutionary algorithm or generate one for any task, test and improve it
7.  try a multi-agent option where they could interact via reading and writing to shared state - time-travel debuggable persistence layer
    1. time-travel debuggable persistence layer - Redux
    2. add ability to define / compose a hierarchy of agents - Rect
    3. cyclic communication - seems like a trap but can be key -
       1. stopping when no improvement has happened for x generations
    4. add ability to adjust its topology - by writing React components
8.  create a neural net to prpedict optimal hyper parameter values for a task / evolution based on meta evolution data
9.  add RLHF step to help tune the system by allowing a person to judge the outputs in comparative manner, and use it to optimize the predictor net
    1.  just selecting the option he/she likes better
10. The you’d need to use it to tune an evaluator- Rlhf against current benchmarks to test evaluator vs the human task definition?
    1. design a system for humans to judge Agent outputs
    2. tune a model to predict user preferences
    3. optimize the meta-evolution
11. test it on a more challenging task
12. Retrospective -
    1. on the iteration
    2. on the idea

## -----REFLECTION-ON-SPRINT-AND-IDEA-----

2.  TextGrad paper may be useful addition to this - back propagation with text - https://github.com/zou-group/textgrad
    1. https://arxiv.org/abs/2406.07496
3.  https://arxiv.org/abs/2406.04692

4.  https://github.com/stanfordnlp/dspy - check the competition in detail
5.  add external tools to agents
    1. https://github.com/microsoft/graphrag
    2. vector db?
    3. https://arxiv.org/abs/2406.11830
6.  code interpreter
7.  web browsing
8.  logic provers / algorithmic reasoners - https://arxiv.org/abs/2406.09308
9.  Run it on a suite of tasks
    e8. nable dynamic topology adaptation - generation of the network and tuning of the agents

10. enable cyclic workflows with dynamic termination? - by analyzing logs during runtime?
11. test on generic tasks - human eval? other single prompt tasks? vs chain of thoughts? dspy? - https://arcprize.org/
12. make it multi-objective
13. add recombination operator and compare the 2 approaches
14. visualize and analyze the agent - like time to solution
15. get it to run against a self hosted Mistral or LLama - something ideally running locally. - may be a 7b model if my laptop can handle it or a mistral model
    1. alternattively on gradio via huggingface tuorials - or Groq - for high speed?
16. run it on a suite of different tasks and compare performance to existing solutions / to collect metrics for future studies
17. [] graphs with relevant file names. - unique IDs?
18. benchmarks on more complex tasks -

    1. agentBench?
    2. plug into RL in huggingface? for training
    3. use it to update itself / build a sage AGI

19. Let’s start with non parallel stateless option to keep things simple
20. Then we can add statefullness
21. Then parallelism
22. Then interactions amongst individuals - dynamism
23. Then self adaptation of hyper parameters
24. The adaptation of function itself
25. The data analysis tools for evolution runs
26. Then reactivity
27. Then time travel debuggable persistence with event sourcing or aot log
28. Nested reactive components like what react framework allows us to have for reusability - for llm powered agent could be as simple as composition of prompts in an execution tree of intelligence - you define the structure of components and props of components and they solve the given task - with human doing the verification and different components interact with each other via global states and subscribing to different parts of it.
    1. Since they’re updating the global state and subscribing to it it is a dynamic and reactive system - and user can interact with it of course but the composition would be done by humans in that case.
    2. Just developing an llm agent where development is managed by people piecing components together.
    3. Why? Because evaluation is difficult and usually best left up to people perhaps.
    4. Component returning a prompt that gets executed and output is processed and either does something with system apis or persists data to state
    5. Possibly exposing UI for is to interact with. An abstraction over a multi- modal system. But special location makes sense for visual elements with navigation and etc - not sure what HCI for a multi agent system would be like.
    6. Maybe if we had a reactive system (even without state) it could be powerful already for building agents
       1. Local state + props and reacting on component lifecycle, state changes and prop changes
       2. Output? APIs defined to it / provided to it. - state management and other props
       3. Could call event handlers from parents or events from users or api requests
       4. With function calling in prompts to call parents’ functions or update state.
       5. What if we just use react and redux
          1. The output in hex would be an executable function that executes llm call - the outputs of it can be handled by output parser with function calling ability to call component functions
          2. Then every component is a prompt with own state and props that the llm can interact with - what would you build for that? A multi-agent system? Eg here’s a coder here’s a test writer here’s another thing? Maybe with self mutation it could be interesting.
          3. How would you write evolution in react+ redux.
             1. Initial state in redux
             2. Variance component subscribing to state, listening for population update, receiving the population, then iterating through it and mutating it, and submitting the output to state
             3. This would trigger the subsequent steps - possibly all sequentially
             4. What about continuous execution?
                1. Last function that subscribes would emit event that would trigger the evolution cycle again depending on its props
                2. The components would just be initialization, evolution functions and runner
                3. Hyper parameters would be in state and algorithms would subscribe to them and update them if they want
                4. Configs can be initialized
                5. Meta evolution? - evolution component would accept the props - for meta evolution you’d pass the config props I suppose.
                6. Operating in parallel ? - just subscribe to state changes and not event types
                7. Higher order functions to add middleware to components like logging and persistence…self mutation?
                8. Interactive simulation? Eg control on screen agent that can interact with each other? And perceive each other via state? / map?
                9. Every research paper is just a react component…
                10. With visualization of their outputs I suppose…
                    1. Evolution of an agent
                    2. Multi agent evolution - increase population size and add recombination
                    3. Inter agent communication - just add a state slice for them to read and write to
                    4. Benchmarking different evolutions? Just import the evolution components with different parameters - each with its own context to manage internal state and one global state to perform visualizations on
                    5. The components for each evolutionary component can be nested in each other not communicating via state at all. - just different evolutionary stages for each individual agent - or a common evolution for all… idk. Variance as a function would depend on population generated by initial population or state update and hyper parameters in state update
                    6. Evaluation for population should not be triggered if no variance has taken place and is indeed coupled to it and its own hyper parameters changing which should re run it
                    7. Selection should depend on evaluation changes
                    8. Population is changing with every generation
                    9. And if agents could dynamically rewrite their own code / execution by storing it somewhere that would be interesting
                    10. Evaluation? People for now to compare the evolution. Or other applications they may be building. Intertwining workflow and ai … with more and more of it being taken over by ai …
                    11. Middleware like hooks could be used for things like updating visualisation l, logging, api calls / tools, or any other reusable behaviour that can or should be shared amongst agents…
                    12. Building multi agent systems declaratively … and continuously evolving them and perhaps letting them communicate with each other…
                    13. Contexts for managing communication amongst components
                    14. Graphql seems like it could be powerful for dealing with relational queries or graph queries stored in relational fashion? - perhaps agent would be able to retrieve what types of data it can request and form a correct request for it
                    15. Graphql and external server in general could be useful for sharing state across many client side agents - each client executing our simulation with different parameters and us getting the data for them - massively parallel agent system running on edge - perhaps server just aggregating stats and things like that… firebase is a nice solution for realtime db…
                    16. Server components can access file system - but that can be done with server actions … since server components are stateless I’m not sure how useful they are - they could make initial fetches and initialization logic… and maybe initiate the state?
                    17. Avoid moving calls to global state and global communication unless necessary - individual agents could have their own state including their own storage that could be on the server
                    18. Tree with connections backwards eg state sharing communication is a graph - a cyclic graph
                    19. Ability to rewrite itself in a modular fashion with progressively more abstraction to handle more complexity - a neuron evolution of an agent network - is the state tree just more nodes in a different dimension? - every field is a node that can connect to any component node - so edges of graph or tree are another tree? Assuming there’s connection from edge to edge? Node in data tree can have many connections - connections between edges more complex than a graph since your mutation of an edge does not only impact your neighbors but the neighbors of connected edges - like common interest
                    20. Ability to dynamically add agents to existing simulation from remotes with module federation
                    21. Also ability to create non modules of agents that can be installed and imported at build time
                    22. Storybook to demonstrate different agents / components in isolation…
                    23. Jest or other testing tools for testing…
                    24. E2E tests with playwright but would need to use frozen temperature to make sure we get consistent results that can be cached perhaps…

. If it gets to AGI like level - run it in a simulation and see how a society of AGIs would evolve and whether you can influence it to move in your desired direction 8. update evaluation to use RAGELO? - elo rating... - https://www.youtube.com/watch?v=oNRpbgSirS0 - elo rating or RAG agents 9. https://arxiv.org/abs/2312.10997

## ----- SCRUM-SRINT 1-END ----

5. reflect on the
   1. idea
   2. plan
   3. process - plan creation process
   4. objective
      1. should it be done at all?
      2. can it be done at all?
      3. should it be the one doing it?
      4. can I be the one doing it?
   5. motivation

## -----REFLECTION-ON-PROCESS-----

SCRUM - is fine, iterative nature is good, but it gets inflexible and heavy

The good

1. iterative
2. I know it kind of
3. time spent on refiniement is well spent usually - case in point, time witth Mustafa, but should be doen with domain experts

the bad

1. linear, non dynamic, non interactive
2. time that could be used for execution is spend on planning

room for improvement

1. dynamically changing the tasks based on feedback, thoughts, ideas, learning, without having to stick to a plan that we know doesn't work

## -----REFLECTION-ON-OBJECTIVE-----

HUMAN-PARENT-AGI

1. should it be done? - it could sove all of our problems, but also lead to our exttinction, might be our ultimate purpose if we are in a simulation
2. can it be done - I think I could build some interesting agents even if chances of me being the one without any serrious access to comppute or models of my own is limited.
   Open source and competition amongst the model providers seems to be empowering, and even if the interest in the field is increasing I may be able to do it sinice my ideas are also being explored by leadiing research labs in real time
3. should it be the one doing it? - I don't think I could resist selfish temptations - I'm too weak for it even if I wish to be good, I'm scared
4. should I be the one doing it - no, I hope a better person would do it - a morally better person

Also the overall objective seems overly ambitious and doomed to failure

## ----- PROCESS-ITERATION-1-AGILE-SCRUM-END-----

## ------PROCESS-1-SCRUM-AGILE-END------

## ------OBJECTIVE-1-BUILDING-SAFE-AGI-END----
