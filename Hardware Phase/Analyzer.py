from HLS_Generator import *
from Estimator import *
import matplotlib.pyplot as plt
import numpy as np

def TOP (inp_ns, hid_ns, out_ns, sample, x_0, y_0, z_0, no_dsp, mode: str):

    factor_1 = factor_2 = factor_3 = factor_4 = 1
    one_mac = False
    factor_1_list = list()
    factor_2_list = [inp_ns]
    estimated_luts = []
    estimated_dsps = []
    estimated_latency = []
    
    solutions = []

    if (mode == 'interactive' or mode == 'analyze'):

        for idx_1 in reversed(range(2, hid_ns+1)):
            if(hid_ns % idx_1 == 0 and np.log2(hid_ns/idx_1)%1 == 0):

                factor_1_list.append((idx_1)) 

        for i in factor_1_list:
            
            for j in factor_2_list:

                solutions.append([i, j, j, i])
                
        solutions.append([1, 1, 1, 1])
        estimated_luts, estimated_dsps, estimated_latency = estimate(inp_ns, hid_ns, no_dsp, solutions)
        print(solutions)

        

    if mode == 'interactive':

        print(f"You have {len(solutions)} solutions.\n")

        for i in range(len(solutions)):

            print(f"Solution {i} -> Estimated LUT: {estimated_luts[i]}        Estimated DSP: {estimated_dsps[i]}        Estimated Iteration Latency (CC): {estimated_latency[i]}       \n")

        key = int(input("Which solution do you prefer? \n\n"))

        factor_1 = solutions[key][0]
        factor_2 = solutions[key][1]
        factor_3 = solutions[key][2]
        factor_4 = solutions[key][3]


    elif mode == 'analyze':
        print(f"There are {len(solutions)} solutions available:\n")
        
        for i in range(len(solutions)):
            print(f"Solution {i} -> Estimated LUT: {estimated_luts[i]}        Estimated DSP: {estimated_dsps[i]}        Estimated Iteration Latency (CC): {estimated_latency[i]}       \n")
        
        
        print("Drawing the plot")
        # Draw the plot

        plt.plot(estimated_latency, estimated_luts, linestyle = '--', marker='o', lw=2.5, mew=4)

        plt.xlabel("Estimated Iteration Ltanecy (CC)")
        plt.ylabel("Estimated # of LUTs")
        plt.ticklabel_format(axis='both', style='sci', scilimits=(3,3), useMathText=True)
        plt.rcParams["font.family"] = "serif"
        plt.grid()
        
        plt.show()

    elif mode == 'generate_p': # Generate with performance as the high priority
        factor_1 = hid_ns
        factor_2 = inp_ns
        factor_3 = out_ns
        factor_4 = hid_ns

    elif (mode == "generate_c"): # Generate with cost as the high priority
        factor_1 = 1
        factor_2 = 1
        factor_3 = 1
        factor_4 = 1
        one_mac = True
    else:
        print("Error: wrong mode argument in Top function")
    
    if mode == 'interactive' or mode == 'generate_c' or  mode == 'generate_p':
        
        create_h_file("HENNC.h", inp_ns, hid_ns, out_ns)
        create_cpp_file("HENNC.cpp", sample, factor_1, factor_2, factor_3, factor_4, out_ns, one_mac, no_dsp)
        create_testBench_file("test_bench.cpp", x_0, y_0, z_0)
        print("HLS model generated successfully")








   
    