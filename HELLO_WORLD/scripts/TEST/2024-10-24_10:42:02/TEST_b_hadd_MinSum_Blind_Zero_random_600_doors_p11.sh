#!/bin/bash
ulimit -Sv 8000000
python /home/dieaigar/Work/BOAND/planner/planner.py /home/dieaigar/Work/BOAND/benchmarks/doors/domain.pddl /home/dieaigar/Work/BOAND/benchmarks/doors/p11.pddl /home/dieaigar/Work/BOAND/HELLO_WORLD/results/TEST/RUN_2024-10-24_10:42:02/b_hadd_MinSum_Blind_Zero_random_600/doors/p11/solutions/doors_p11.sol -m b -ch hadd -bh MinSum -wh Blind -sh Zero -s random