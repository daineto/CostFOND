import re
import glob
import subprocess
import sys
import math
import shutil

from pathlib import Path

from pddl import parse_domain, parse_problem
from pddl.formatter import domain_to_string, problem_to_string

from utils import determinize
from preprocessing import get_alloutcome_determinization

from pyperplan.pyperplan.pddl.parser import Parser
from pyperplan.pyperplan import grounding
from pyperplan.pyperplan.heuristics.relaxation import hMaxHeuristic

from policy import Policy
from planner import extend_policy, compute_f_value, boand_star

TRANSLATE_SCRIPT_PATH = "/home/dieaigar/Work/planners/prp/prp-scripts/translate_policy.py"

def rewrite_fact(fact_str):
    index1 = fact_str.index("(")
    index2 = fact_str.index(")")

    predicate = fact_str[:index1]
    args = fact_str[index1+1:index2].replace(",","").split(" ")

    fact_tokens = [predicate]
    if index1 + 1 < index2:
        fact_tokens += args

    return "(" + " ".join(fact_tokens) + ")"

def parse_prp_policy(prp_policy_file):
    with open(prp_policy_file, "r") as f:
        prp_policy_out = f.readlines()

    strategy = dict()
    for i in range(len(prp_policy_out)):
        if "If" == prp_policy_out[i][:2]:
            assert "Execute" == prp_policy_out[i+1][:7]

            partial_state_str = prp_policy_out[i][9:].strip()
            action_str = prp_policy_out[i+1][8:]
            action_str = action_str[:action_str.index("/")].strip()


            partial_state_facts = partial_state_str.split("/")
            action_tokens = action_str.replace(",","").split(" ")

            if action_tokens[0] == "goal":
                continue
            else:
                action = "(" + " ".join(action_tokens) + ")"
                partial_state = frozenset([rewrite_fact(fact) for fact in partial_state_facts])

            strategy[partial_state] = action
        elif "FSAP" == prp_policy_out[i][:4]:
            break

    return strategy


def parse_cf_policy(policy_file):
    with open(policy_file, "r") as f:
        policy_out = f.readlines()

    strategy = dict()
    for i in range(len(policy_out)):
        if "If" == policy_out[i][:2]:
            assert "Execute" == policy_out[i+1][:7]

            state_str = policy_out[i][9:].strip()
            action = policy_out[i+1][8:].strip()


            state_facts = state_str.split("/")
   
            state = frozenset(state_facts)

            strategy[state] = action

    return strategy


def evaluate_policy(domain_file, problem_file, policy_file, planner="cf"):

    assert planner in {"cf", "prp"}
    if planner == "cf":
        strategy = parse_cf_policy(policy_file)
    elif planner == "prp":
        strategy = parse_prp_policy(policy_file)

    
    domain = parse_domain(domain_file)
    problem = parse_problem(problem_file)

    task = get_alloutcome_determinization(domain, problem)

    nondet_to_det_action = dict()
    for op in task.operators:
        nondet_action = re.sub('_detdup_' + '[0-9]*', '', op.name)

        det_actions = nondet_to_det_action.get(nondet_action, set())
        det_actions.add(op)
        nondet_to_det_action[nondet_action] = det_actions

    pi = Policy(dict(), {task.initial_state}, set())
    while(pi.pending):
        state = pi.pending.pop()
        for partial_state,action in strategy.items():
            if partial_state <= state:
                successors = {det_action.apply(state) for det_action in nondet_to_det_action[action]}
                pi = extend_policy(pi,state,action,nondet_to_det_action[action],successors,task)
                break

    fscore = compute_f_value(pi, task, hMaxHeuristic(task), dict())

    # closed, cyclic, proper, best, worst
    return pi.is_closed(), pi.cyclic, pi.is_proper(task), fscore[0], fscore[1]


def run_prp(domain_folder):

    domain_file = domain_folder + "/domain.pddl"
    problem_files = sorted(glob.glob(domain_folder + "/p*.pddl"))


    for problem_file in problem_files:
        #prp domain.pddl p02.pddl --dump-policy 2
        try:
            subprocess.run(["prp", domain_file, problem_file, "--dump-policy", "2"], timeout=10)
            translator = subprocess.run(["python2", TRANSLATE_SCRIPT_PATH], stdout=subprocess.PIPE)
            with open(problem_file[:-4]+"prp.out", "w") as out:
                out.write(translator.stdout.decode('UTF-8'))
        except subprocess.TimeoutExpired:
            print("timeout")


def process_solutions(domain_folder, planner="cf"):
    
    assert planner in {"cf", "prp"}
    
    domain_file = domain_folder + "/domain.pddl"
    policy_files = sorted(glob.glob(domain_folder + "/p*.%s.out" % planner))

    suffix_len = len(planner) + 4

    for policy_file in policy_files:
        problem_file = policy_file[:-suffix_len]+"pddl"
        closed, cyclic, proper, best, worst = evaluate_policy(domain_file, problem_file, policy_file, planner=planner)

        problem_name = problem_file.split("/")[-1][:-5]

        print("Problem %s: closed = %s, cyclic = %s, proper = %s, best = %s, worst = %s" % (problem_name, closed, cyclic, proper, best, worst))


def compare_solutions(domain_folder):
    
    best_prp = dict()
    worst_prp = dict()
    best_boand = dict()
    worst_boand = dict()
    

    # PRP
    planner = "prp"
    domain_file = domain_folder + "/domain.pddl"
    policy_files = sorted(glob.glob(domain_folder + "/p*.%s.out" % planner))
    suffix_len = len(planner) + 4

    for policy_file in policy_files:
        problem_file = policy_file[:-suffix_len]+"pddl"
        closed, cyclic, proper, best, worst = evaluate_policy(domain_file, problem_file, policy_file, planner=planner)
        if not proper:
            worst = math.inf

        problem_name = problem_file.split("/")[-1][:-5]

        best_prp[problem_name] = best
        worst_prp[problem_name] = worst

    # CF
    planner = "cf"
    domain_file = domain_folder + "/domain.pddl"
    policy_files = sorted(glob.glob(domain_folder + "/p*.%s.out" % planner))
    suffix_len = len(planner) + 4

    for policy_file in policy_files:
        problem_file = policy_file[:-suffix_len]+"pddl"
        closed, cyclic, proper, best, worst = evaluate_policy(domain_file, problem_file, policy_file, planner=planner)
        if not proper:
            worst = math.inf

        problem_name = problem_file.split("/")[-1][:-5]

        best_boand[problem_name] = best
        worst_boand[problem_name] = worst


    problems = set(best_prp.keys())
    sorted(list(problems.union(set(best_boand.keys()))))

    for problem in problems:
        print("Problem %s: PRP = (%s,%s) | BOAND* (%s,%s)" % (problem, best_prp.get(problem,None), worst_prp.get(problem,None), best_boand.get(problem,None), worst_boand.get(problem,None)))


def run_boand(domain_folder, config):

    # ("bw",False,"hadd","random",60)
    metric = config[0]
    tiebreak = config[1]
    heuristic = config[2]
    selector = config[3]
    timeout = config[4]

    results_folder = "_".join(map(str,list(config)))

    domain_name = domain_folder[domain_folder.rfind("/"):]
    Path("results/{}/{}".format(domain_name, results_folder)).mkdir(parents=True, exist_ok=True)

    domain_file = domain_folder + "/domain.pddl"
    problem_files = sorted(glob.glob(domain_folder + "/p*.pddl"))

    for problem_file in problem_files:
        print("Solving %s" % problem_file)
        command = ["python", "planner.py", domain_file, problem_file, "-m", metric, "-h", heuristic, "-s", selector]
        if tiebreak:
            command += ["-tb"]
        try:
            subprocess.run(command, timeout=timeout)
        except subprocess.TimeoutExpired:
            print("timeout")

        policy_files = sorted(glob.glob(domain_folder + "/p*.boand.*.out"))
        for policy_file in policy_files:
            file_name = policy_file[policy_file.rfind("/"):]
            shutil.move(policy_file, "results/{}/{}/{}".format(domain_name, results_folder, file_name))
        
        try:
            problem_name = problem_file[problem_file.rfind("/"):][:-5]
            shutil.move(problem_file[:-4]+"stats", "results/{}/{}/{}.stats".format(domain_name, results_folder, problem_name))
        except:
            pass

def run_boand_all_domains(configs):
    folders = sorted(glob.glob("benchmarks/*"))
    for config in configs:
        for folder in folders:
            run_boand(folder, config)


# CONFIGS: metric, tiebreak, heuristic, selector, timeout
# config = ("bw",False,"hadd","random",60)
# config = ("bw",False,"hadd","bounds",60)
# config = ("bw",True,"hadd","random",60)
# config = ("bw",True,"hadd","bounds",60)


configs = [
    # ("bw",False,"hadd","random",60),
    # ("bw",True,"hadd","bounds",60),
    # ("b",False,"hadd","random",60),
    # ("w",False,"hadd","random",60),
    # ("wb",True,"hadd","bounds",60),
    # ("bw",True,"hadd","random",60),
    # ("bw",False,"hadd","best",60),
    ("bw",True,"hadd","best",60),
]

run_boand_all_domains(configs)

# domain = "acrobatics"
# domain_folder = "fond-domains/benchmarks/{}".format(domain)


# domain_folder = "benchmarks/mod_first_responders"
# run_boand(domain_folder, config)

# run_prp(domain_folder)
# run_boand(domain_folder, "boand_bw_opt")
# process_solutions(domain_folder, planner="prp")
# process_solutions(domain_folder, planner="cf")
# compare_solutions(domain_folder)