#!/bin/bash
ulimit -Sv 8000000
python /home/dieaigar/Work/BOAND/planner/planner.py /home/dieaigar/Work/BOAND/benchmarks/chain-of-rooms/domain.pddl /home/dieaigar/Work/BOAND/benchmarks/chain-of-rooms/p26.pddl /home/dieaigar/Work/BOAND/HELLO_WORLD/results/TEST/RUN_2024-10-24_10:42:02/b_hadd_MinSum_Blind_Zero_random_600/chain-of-rooms/p26/solutions/chain-of-rooms_p26.sol -m b -ch hadd -bh MinSum -wh Blind -sh Zero -s random