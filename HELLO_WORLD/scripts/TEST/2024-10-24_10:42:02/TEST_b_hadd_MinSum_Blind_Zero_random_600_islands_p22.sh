#!/bin/bash
ulimit -Sv 8000000
python /home/dieaigar/Work/BOAND/planner/planner.py /home/dieaigar/Work/BOAND/benchmarks/islands/domain.pddl /home/dieaigar/Work/BOAND/benchmarks/islands/p22.pddl /home/dieaigar/Work/BOAND/HELLO_WORLD/results/TEST/RUN_2024-10-24_10:42:02/b_hadd_MinSum_Blind_Zero_random_600/islands/p22/solutions/islands_p22.sol -m b -ch hadd -bh MinSum -wh Blind -sh Zero -s random