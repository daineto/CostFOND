#!/usr/bin/env python3

import os
import shutil

working_dir = "/home/dieaigar/Work/BOAND/HELLO_WORLD/PLANNERS_COPY/copy_TEST_b_hadd_MinSum_Blind_Zero_random_600_tireworld-truck_p18_2024-10-24_10:42:02"

stde_path = "/home/dieaigar/Work/BOAND/HELLO_WORLD/results/TEST/RUN_2024-10-24_10:42:02/b_hadd_MinSum_Blind_Zero_random_600/tireworld-truck/p18/err_tireworld-truck_p18.txt"
stdo_path = "/home/dieaigar/Work/BOAND/HELLO_WORLD/results/TEST/RUN_2024-10-24_10:42:02/b_hadd_MinSum_Blind_Zero_random_600/tireworld-truck/p18/out_tireworld-truck_p18.txt"
time_limit = 600

exec_str = "/home/dieaigar/Work/BOAND/HELLO_WORLD/scripts/TEST/2024-10-24_10:42:02/TEST_b_hadd_MinSum_Blind_Zero_random_600_tireworld-truck_p18.sh 2>> " + stde_path + " 1>> " + stdo_path

system_0_src = "/home/dieaigar/Work/BOAND/planner"
system_0_dst = "/home/dieaigar/Work/BOAND/HELLO_WORLD/PLANNERS_COPY/copy_TEST_b_hadd_MinSum_Blind_Zero_random_600_tireworld-truck_p18_2024-10-24_10:42:02/planner"

open(stdo_path, "w")
open(stde_path, "w")
os.makedirs(working_dir)
os.chdir(working_dir)

################## COPY ALL SRC TO DST ##################
shutil.copytree(system_0_src, system_0_dst)
#########################################################

os.system("time -p timeout --signal=HUP 600 " + exec_str)
shutil.rmtree("/home/dieaigar/Work/BOAND/HELLO_WORLD/PLANNERS_COPY/copy_TEST_b_hadd_MinSum_Blind_Zero_random_600_tireworld-truck_p18_2024-10-24_10:42:02")