#!/bin/bash
ulimit -Sv 8000000
python /home/dieaigar/Work/BOAND/planner/planner.py /home/dieaigar/Work/BOAND/benchmarks/tireworld-truck/domain.pddl /home/dieaigar/Work/BOAND/benchmarks/tireworld-truck/p17.pddl /home/dieaigar/Work/BOAND/HELLO_WORLD/results/TEST/RUN_2024-10-24_10:42:02/b_hadd_MinSum_Blind_Zero_random_600/tireworld-truck/p17/solutions/tireworld-truck_p17.sol -m b -ch hadd -bh MinSum -wh Blind -sh Zero -s random