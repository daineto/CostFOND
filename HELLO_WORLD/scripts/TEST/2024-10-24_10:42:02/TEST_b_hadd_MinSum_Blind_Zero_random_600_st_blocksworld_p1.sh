#!/bin/bash
ulimit -Sv 8000000
python /home/dieaigar/Work/BOAND/planner/planner.py /home/dieaigar/Work/BOAND/benchmarks/st_blocksworld/domain.pddl /home/dieaigar/Work/BOAND/benchmarks/st_blocksworld/p1.pddl /home/dieaigar/Work/BOAND/HELLO_WORLD/results/TEST/RUN_2024-10-24_10:42:02/b_hadd_MinSum_Blind_Zero_random_600/st_blocksworld/p1/solutions/st_blocksworld_p1.sol -m b -ch hadd -bh MinSum -wh Blind -sh Zero -s random