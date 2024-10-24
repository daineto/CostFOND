from utils import determinize

from pddl import parse_domain, parse_problem
from pddl.formatter import domain_to_string, problem_to_string

from pyperplan.pyperplan.pddl.parser import Parser
from pyperplan.pyperplan import grounding
from pyperplan.pyperplan.heuristics.relaxation import *
from pyperplan.pyperplan.search.searchspace import SearchNode




domain = parse_domain("fond-domains/benchmarks/tireworld/domain.pddl")
problem = parse_problem("fond-domains/benchmarks/tireworld/p01.pddl")
detdomain = determinize(domain)

# print(domain_to_string(detdomain))
# print(problem_to_string(problem))

with open("domain.pddl", "w") as f:
    f.write(domain_to_string(detdomain))
with open("problem.pddl", "w") as f:
    f.write(problem_to_string(problem))

parser = Parser("domain.pddl", "problem.pddl")
domain = parser.parse_domain()
problem = parser.parse_problem(domain)

task = grounding.ground(
        problem, True, True
    )

initial_state = task.initial_state

hmax = hMaxHeuristic(task)

hmax(SearchNode(initial_state, None, None, 0))

pass