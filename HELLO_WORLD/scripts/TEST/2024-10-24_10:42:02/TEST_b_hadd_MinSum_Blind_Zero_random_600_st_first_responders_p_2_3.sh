#!/bin/bash
ulimit -Sv 8000000
python /home/dieaigar/Work/BOAND/planner/planner.py /home/dieaigar/Work/BOAND/benchmarks/st_first_responders/domain.pddl /home/dieaigar/Work/BOAND/benchmarks/st_first_responders/p_2_3.pddl /home/dieaigar/Work/BOAND/HELLO_WORLD/results/TEST/RUN_2024-10-24_10:42:02/b_hadd_MinSum_Blind_Zero_random_600/st_first_responders/p_2_3/solutions/st_first_responders_p_2_3.sol -m b -ch hadd -bh MinSum -wh Blind -sh Zero -s random