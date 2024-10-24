

from abc import ABC, abstractmethod
import heapq
import math
import re
import time
import sys

from pddl import parse_domain, parse_problem

from pyperplan.pyperplan.heuristics.relaxation import *
from pyperplan.pyperplan.heuristics.lm_cut import LmCutHeuristic
from pyperplan.pyperplan.search.searchspace import SearchNode

from policy import Policy, CYCLE_COST
from preprocessing import get_alloutcome_determinization

class StateSelector(ABC):
    @abstractmethod
    def select_pending_state(self, policy:Policy, heuristic: Heuristic):
        pass

class RandomStateSelector(StateSelector):
    def select_pending_state(self, policy:Policy, heuristic: Heuristic):
        state = policy.pending.pop()
        return state
    
class BoundsFirstStateSelector(StateSelector):
    def select_pending_state(self, policy:Policy, heuristic: Heuristic):
        prio_list = []
        if len(policy.goal_states) == 0:
            for state in policy.pending:
                heapq.heappush(prio_list, (policy.get_best_g(state) + heuristic(SearchNode(state, None, None, 0)),state))
        else:
            for state in policy.pending:
                heapq.heappush(prio_list, (-(policy.get_best_g(state) + heuristic(SearchNode(state, None, None, 0))),state))
        g,state = heapq.heappop(prio_list)
        policy.pending.remove(state)

        return state
    
class BestStateSelector(StateSelector):
    def select_pending_state(self, policy:Policy, heuristic: Heuristic):
        prio_list = []
        for state in policy.pending:
            heapq.heappush(prio_list, (policy.get_best_g(state) + heuristic(SearchNode(state, None, None, 0)),state))
        policy.pending.remove(state)

        return state

class OpenListSorter(ABC):
    @abstractmethod
    def push(self, open_list, f_best, f_worst, f_close, policy):
        pass

class BestWorstOpenListSorter(OpenListSorter):
    def push(self, open_list, f_best, f_worst, f_close, policy):
        heapq.heappush(open_list, ((f_best,f_worst,0),policy))

class BestWorstCloseOpenListSorter(OpenListSorter):
    def push(self, open_list, f_best, f_worst, f_close, policy):
        heapq.heappush(open_list, ((f_best,f_worst,f_close),policy))

class WorstBestOpenListSorter(OpenListSorter):
    def push(self, open_list, f_best, f_worst, f_close, policy):
        heapq.heappush(open_list, ((f_worst,f_best,0),policy))

class WorstBestCloseOpenListSorter(OpenListSorter):
    def push(self, open_list, f_best, f_worst, f_close, policy):
        heapq.heappush(open_list, ((f_worst,f_best,f_close),policy))

class BestOpenListSorter(OpenListSorter):
    def push(self, open_list, f_best, f_worst, f_close, policy):
        heapq.heappush(open_list, ((f_best,0,0),policy))

class BestCloseOpenListSorter(OpenListSorter):
    def push(self, open_list, f_best, f_worst, f_close, policy):
        heapq.heappush(open_list, ((f_best,0,f_close),policy))

class WorstOpenListSorter(OpenListSorter):
    def push(self, open_list, f_best, f_worst, f_close, policy):
        heapq.heappush(open_list, ((f_worst,0,0),policy))

class WorstCloseOpenListSorter(OpenListSorter):
    def push(self, open_list, f_best, f_worst, f_close, policy):
        heapq.heappush(open_list, ((f_worst,0,f_close),policy))

def select_pending_state(policy, task, heuristic):
    # 1: Expanding lower g first
    # prio_list = []
    # for state in policy.pending:
    #     heapq.heappush(prio_list, (policy.get_best_g(state) + heuristic(SearchNode(state, None, None, 0)),state))
    # g,state = heapq.heappop(prio_list)
    # policy.pending.remove(state)
    
        
    # 2: Establish bounds
    prio_list = []
    if len(policy.goal_states) == 0:
        for state in policy.pending:
            heapq.heappush(prio_list, (policy.get_best_g(state) + heuristic(SearchNode(state, None, None, 0)),state))
    else:
        for state in policy.pending:
            heapq.heappush(prio_list, (-(policy.get_best_g(state) + heuristic(SearchNode(state, None, None, 0))),state))
    g,state = heapq.heappop(prio_list)
    policy.pending.remove(state)

    return state

def update_g_values(policy, state, reached_states, task):
    all_new = True
    for reached_state in reached_states:
        # First time reaching the state
        # tile is the best and worst ancestor
        if policy.best_ancestors.get(reached_state,None) is None:
            # if reached_state != task.initial_state:
            policy.best_ancestors[reached_state] = state
            policy.worst_ancestors[reached_state] = state
        # Not the first time
        else:
            all_new = False

    if not all_new:
        update_g_brute(policy, task)


def update_g_brute(policy:Policy, task:Task):   
    # BRUTE FORCE: Compute al pi-trajectories

    trajectories = list()
    cycles = list()
    frontier = {task.initial_state:[]}
    while frontier:
        state,ancestors = frontier.popitem()
        action = policy.strategy.get(state, None)
        if action is None: #State has no action assigned: end of trajectory
            trajectories.append(ancestors)
        else: # State has action assigned
            reached_states = {det_action.apply(state) for det_action in action[1]}
            for reached_state in reached_states:
                if reached_state in ancestors: # Cycle
                    cycles.append(ancestors[ancestors.index(reached_state):]+[state])
                    pass
                else: # Not a cycle
                    aux1 = policy.get_worst_g(state)
                    aux2 = policy.get_worst_g(policy.worst_ancestors[reached_state])
                    if aux1 > aux2:
                    # if policy.get_worst_g(state,task.initial_state) > policy.get_worst_g(policy.worst_ancestors[reached_state],task.initial_state):
                        policy.worst_ancestors[reached_state] = state
                    if policy.get_best_g(state) < policy.get_best_g(policy.best_ancestors[reached_state]):
                        policy.best_ancestors[reached_state] = state
                    # Extend trajectory
                    new_ancestors = ancestors.copy()
                    new_ancestors.append(state)
                    frontier[reached_state] = new_ancestors
    loopy_states = set().union(*cycles)
    extended_loopy_states = set()
    for cycle in cycles:
        for state in cycle:
            action = policy.strategy.get(state, None)
            reached_states = {det_action.apply(state) for det_action in action[1]}
            for reached_state in reached_states:
                if reached_state not in loopy_states:
                    extended_loopy_states.add(reached_state)
                policy.worst_ancestors[reached_state] = state
    
    already_seen = set()
    while extended_loopy_states:
        state = extended_loopy_states.pop()
        if state not in already_seen:
            action = policy.strategy.get(state, None)
            if action is not None: #State has no action assigned: end of trajectory
                reached_states = {det_action.apply(state) for det_action in action[1]}
                for reached_state in reached_states:
                    policy.worst_ancestors[reached_state] = state
                reached_states.difference_update(already_seen)
                extended_loopy_states.update(reached_states)
            already_seen.add(state)
        

    if len(cycles) > 0:
        policy.cyclic = True


def extend_policy(current_policy, state, nondet_action, det_actions, successors, task):
    new_policy = current_policy.copy()
    new_policy.strategy[state] = (nondet_action, det_actions)

    # TODO: is it better to compute the pending first? 
    # if every successor is in new_pending then no need update_g_brute?

    # Update the g-values (ancestors) of the reached states 
    update_g_values(new_policy,state,successors, task)

    # Compute pending tiles for the new policy
    new_pending = [succ for succ in successors if not task.goal_reached(succ) and new_policy.strategy.get(succ,None) is None]
    new_policy.pending.update(new_pending)

    new_goal_states = [succ for succ in successors if task.goal_reached(succ)]
    new_policy.goal_states.update(new_goal_states)

    return new_policy

def compute_f_value(policy:Policy, task:Task, heuristic:hMaxHeuristic):
    # if policy.is_closed():
    #     f_best = policy.get_best_g(goal,init)
    #     if policy.cyclic:
    #         f_worst = math.inf
    #     else:
    #         f_worst = policy.get_worst_g(goal,init)
    # else:
    #     if policy.best_ancestors.get(goal, None) is not None:
    #         f_best = policy.get_best_g(goal,init)
    #     else:
    #         f_best = min([policy.get_best_g(pending_tile, init) + manhattan(pending_tile,goal) for pending_tile in policy.pending])

    #     if policy.cyclic:
    #         f_worst = math.inf
    #     else:
    #         f_worst = max([policy.get_worst_g(pending_tile, init) + manhattan(pending_tile,goal) for pending_tile in policy.pending])

    Out = policy.pending.union(policy.goal_states)
    # WITHOUT H CACHE

    h_values = {state: heuristic(SearchNode(state, None, None, 0)) for state in Out}

    f_best = min([policy.get_best_g(state) + h_values[state] for state in Out], default=math.inf)

    f_worst_values = []
    for state in Out:
        g_worst = policy.get_worst_g(state)
        h = h_values[state]
        if g_worst == CYCLE_COST:
            f_worst_values += [max(CYCLE_COST, h)]
        else:
            f_worst_values += [g_worst + h]
    f_worst = max(f_worst_values, default=math.inf)

    # DISCARDED: it assigns CYCLE_COST + h in case of cyclic policies
    # f_worst = max([policy.get_worst_g(state) + h_values[state] for state in Out], default=math.inf)
    
    h_vector = sorted([h_values[state] for state in policy.pending])
    if len(h_vector) > 0:
        f_close = max([h_vector[i] + i for i in range(len(h_vector))])
    else:
        f_close = 0

    # f_close = len(policy.pending)


    # WITH H CACHE

    # f_best = min([policy.get_best_g(state, task.initial_state) + hcache.setdefault(state,heuristic(SearchNode(state, None, None, 0))) for state in Out], default=math.inf)
    # f_worst = max([policy.get_worst_g(state, task.initial_state) + hcache.setdefault(state,heuristic(SearchNode(state, None, None, 0))) for state in Out], default=math.inf)
    # # f_close = len(policy.pending)
    # h_vector = sorted([hcache[state] for state in policy.pending])
    # if len(h_vector) > 0:
    #     f_close = max([h_vector[i] + i for i in range(len(h_vector))])
    # else:
    #     f_close = 0

    if f_worst > CYCLE_COST and f_worst < math.inf:
        pass

    # DEADLOCK in the policy: it cannot become proper
    if policy.cyclic and f_worst < CYCLE_COST:
        f_worst = math.inf

    return f_best, f_worst, f_close

def boand_star(domain_file, problem_file, use_metric = "bw", tie_break = True, use_heuristic = "hadd", use_selector = "bounds_first"):
    
    # Read FOND task
    domain = parse_domain(domain_file)
    problem = parse_problem(problem_file)

    task = get_alloutcome_determinization(domain, problem)

    # CONFIG
    if use_heuristic == "hadd":
        heuristic = hMaxHeuristic(task)
    elif use_heuristic == "lmcut":
        heuristic = LmCutHeuristic(task)
    else:
        print("heuristic must be 'hadd' or 'lmcut'")
        exit()

    if use_selector == "random":
        selector = RandomStateSelector()
    elif use_selector == "best":
        selector = BestStateSelector()
    elif use_selector == "bounds":
        selector = BoundsFirstStateSelector()
    else:
        print("selector must be 'random' or 'bounds'")
        exit()

    if use_metric == "bw":
        if tie_break:
            openListSorter = BestWorstCloseOpenListSorter()
        else:
            openListSorter = BestWorstOpenListSorter()
    elif use_metric == "wb":
        if tie_break:
            openListSorter = WorstBestCloseOpenListSorter()
        else:
            openListSorter = WorstBestOpenListSorter()
    elif use_metric == "b":
        if tie_break:
            openListSorter = BestCloseOpenListSorter()
        else:
            openListSorter = BestOpenListSorter()
    elif use_metric == "w":
        if tie_break:
            openListSorter = WorstCloseOpenListSorter()
        else:
            openListSorter = WorstOpenListSorter()
    else:
        print("metric must be 'b' (best), 'w' (worst), 'bw' (best,worst) or 'wb' (worst,best).")
        exit()
    

    
    # hcache = dict()

    # Initialize open and closed list
    open_list = []
    # closed_list = set()
    
    # Generate empty policy
    empty_policy = Policy(dict(),set(), set())
    empty_policy.pending.add(task.initial_state)
    empty_policy.best_ancestors = {task.initial_state:"dummy"}
    empty_policy.worst_ancestors = {task.initial_state:"dummy"}
    # Push the empty policy onto the open list
    heapq.heappush(open_list, ((0,0), empty_policy))

    pareto_frontier = []
    pareto_f = (math.inf, math.inf)
    # repeated = 0
    stats = {"best":[], "worst":[], "size":[], "time":[], "iterations":[], "expansions":[], "generations":[], "max_open":[]}

    max_open = 0
    it = 0
    expansions = 0
    generations = 0
    start_time = time.time()
    # Loop until the open list is empty
    while open_list:
        # Get the policy with the lowest f value
        f_value, current_policy = heapq.heappop(open_list)
        it += 1

        # Pruning non-Pareto solutions
        if f_value[0] >= pareto_f[0] and f_value[1] >= pareto_f[1]:
            continue

        # CLOSED LIST SEEMS UNNECESSARY
        # hashable_strategy = frozenset(current_policy.strategy.items())
        # if hashable_strategy in closed_list:
        #     repeated += 1
        #     pass # Add a breakpoint here to see hits
        # closed_list.add(hashable_strategy)
        

        # Check if the policy is closed
        if current_policy.is_closed():
            # If closed and proper, it is a solution
            if current_policy.is_proper(task):
                pareto_frontier += [current_policy]
                pareto_f = (f_value[0], f_value[1])
                
                elapsed_time = time.time() - start_time

                f_best, f_worst, f_close = compute_f_value(current_policy,task,heuristic)

                stats["best"] += [f_best]
                stats["worst"] += [f_worst]
                stats["size"] += [len(current_policy.strategy)]
                stats["time"] += [elapsed_time]
                stats["iterations"] += [it]
                stats["expansions"] += [expansions]
                stats["generations"] += [generations]
                stats["max_open"] += [max_open]

                
                write_solution(current_policy, len(pareto_frontier), problem_file)
                write_stats(stats, problem_file)
                
            # Closed policies cannot be expanded
            continue

        ### EXPANSION ###
        expansions += 1
        # Select a state from Out~(current_policy)
        state = selector.select_pending_state(current_policy, heuristic)

        op_successors = task.get_successor_states(state)
        nondet_action_to_successors = dict()
        # TODO: caching?
        nondet_to_det_action = dict()
        for (op,succ) in op_successors:
            nondet_action = re.sub('_detdup_' + '[0-9]*', '', op.name)

            successors = nondet_action_to_successors.get(nondet_action, set())
            successors.add(succ)
            nondet_action_to_successors[nondet_action] = successors

            det_actions = nondet_to_det_action.get(nondet_action, set())
            det_actions.add(op)
            nondet_to_det_action[nondet_action] = det_actions


        for (nondet_action,successors) in nondet_action_to_successors.items():
            # Create new_policy by extending current_policy
            # Extension: map tile to action
            new_policy = extend_policy(current_policy, state, nondet_action, nondet_to_det_action[nondet_action], nondet_action_to_successors[nondet_action], task)
            generations += 1

            # Calculate new_policy's f-value
            f_best, f_worst, f_close = compute_f_value(new_policy,task,heuristic)

            # Uncomment to discard weak policies
            if f_worst == math.inf or f_close == math.inf:
                continue

            # Uncomment to discard cyclic policies
            # if new_policy.cyclic:
            #     continue

            # Add the child to the open list
            openListSorter.push(open_list,f_best,f_worst,f_close,new_policy)
            # heapq.heappush(open_list, ((f_best,f_worst,f_close),new_policy)) # BEST then WORST
            # heapq.heappush(open_list, ((f_worst,f_best,f_close),new_policy)) # WORST then BEST

        max_open = max(max_open, len(open_list))

    elapsed_time = time.time() - start_time

    stats["best"] += [-1]
    stats["worst"] += [-1]
    stats["size"] += [-1]
    stats["time"] += [elapsed_time]
    stats["iterations"] += [it]
    stats["expansions"] += [expansions]
    stats["generations"] += [generations]
    stats["max_open"] += [max_open]
    
    write_stats(stats, problem_file)

    # print(len(closed_list))
    return pareto_frontier


def write_solution(policy, sol_number, problem_file):

    policy_str = ""
    for state, action in policy.strategy.items():
        policy_str += "If holds: " + "/".join(state) + "\n"
        policy_str += "Execute: %s\n" % action[0]
        policy_str += "\n"

    with open(problem_file[:-4]+"boand.%s.out" % str(sol_number).zfill(3), "w") as out:
        out.write(policy_str)

def write_stats(stats, problem_file):

    stats_str = ""
    for i in range(len(stats["best"])):
        stats_str += ";".join(map(str,[stats["best"][i], stats["worst"][i], stats["size"][i], stats["time"][i], stats["iterations"][i], stats["expansions"][i], stats["generations"][i], stats["max_open"][i]])) + "\n"

    with open(problem_file[:-4]+"stats", "w") as out:
        out.write(stats_str)


def main(argv, arc):
    # print(argv, arc)

    # print("Example call: python planner <domain> <problem> -m <metric> -tb <0/1> -h <heuristic> -s <selector>")

    domain_file = argv[1]
    problem_file = argv[2]

    metric = "bw"
    if "-m" in argv:
        index = argv.index("-m")
        metric = argv[index+1]
    tiebreak = False
    if "-tb" in argv:
        tiebreak = True
    heuristic = "hadd"
    if "-h" in argv:
        index = argv.index("-h")
        heuristic = argv[index+1]
    selector = "bounds"
    if "-s" in argv:
        index = argv.index("-s")
        selector = argv[index+1]
    
    solution = boand_star(domain_file, problem_file, use_metric=metric, tie_break=tiebreak, use_heuristic=heuristic, use_selector=selector)
 

def test():
    # PARSING ERRORS: 
    # blocksworld(s) - NNF (not (= ?b1 ?b2))
    # faults(s) - same name "fault" for object and predicate
    # puffbot_dialogue_pddl - same name "initiate" for action and predicate
    # st_faults - same name "fault"
    # st_mapfdu - determinizer error
    # tidyup-mdp - NNF (not (= a b))
    # zenotravel - forall


    domain = "frozenlake" 

    domain_file = "fond-domains/benchmarks/{}/domain.pddl".format(domain)
    problem_file = "fond-domains/benchmarks/{}/p_1_3.pddl".format(domain)

    domain_file = "benchmarks/{}/domain.pddl".format(domain)
    problem_file = "benchmarks/{}/motivating.pddl".format(domain)

    solution = boand_star(domain_file, problem_file, use_metric="bw", tie_break=False, use_heuristic = "hadd", use_selector="random")

if __name__ == '__main__':
    main(sys.argv, len(sys.argv))
    # test()

    


