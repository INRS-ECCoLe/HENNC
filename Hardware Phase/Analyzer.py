
from HLS_Generator import *

def TOP (inp_ns, hid_ns, out_ns, sample, x_0, y_0, z_0, one_mac: bool, no_dsp: bool,  mode: str):

    n_factor = 4
    factor_1 = factor_2 = factor_3 = factor_4 = 1
    factor_1_list = list()
    factor_2_list = [inp_ns]
    
    solutions = [[1,1,1,1]]

    if (mode == 'interactive' or mode == 'analyze'):

        for idx_1 in reversed(range(2, hid_ns + 1)):

            if(hid_ns % idx_1 == 0):

                factor_1_list.append((idx_1)) 

        for i in factor_1_list:
            
            for j in factor_2_list:

                solutions.append([i, j, j, i])

        print(solutions)

        # Estimate Function

    if mode == 'interactive':

        print(f"You have {len(solutions)} solutions.\n")

        for i in range(len(solutions)):

            print(f"Solution {i} -> Estimated Area:        Estimated Latency:       \n")

        key = int(input("Which solution you prefer ? \n"))

        factor_1 = solutions[key][0]
        factor_2 = solutions[key][1]
        factor_3 = solutions[key][2]
        factor_4 = solutions[key][3]

    elif mode == 'analyze':
        print(f"There are {len(solutions)} solutions available:\n")
        for i in range(len(solutions)):
            print(f"Solution {i} -> Estimated Area:        Estimated Latency:       \n")
        print("drawing the plot")
        # Draw the plot
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
    else:
        print("Error: wrong mode argument in Top function")
    
    if mode == 'interactive' or mode == 'generate_c' or  mode == 'generate_p':
        
        create_h_file("Hardware Phase\HENNC.h", inp_ns, hid_ns, out_ns)
        create_cpp_file("Hardware Phase\HENNC.cpp", sample, factor_1, factor_2, factor_3, factor_4, out_ns, one_mac, no_dsp)
        create_testBench_file("Hardware Phase\ test_bench.cpp", x_0, y_0, z_0)
        print("HLS model generated successfully")








   
    