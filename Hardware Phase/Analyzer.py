
from HLS_Generator import *

def TOP (inp_ns, hid_ns, out_ns, sample, x_0, y_0, z_0, one_mac: bool, no_dsp: bool, solution: bool, mode: str):

    n_factor = 4
    factor_1 = factor_2 = factor_3 = factor_4 = 1

    factor_1_list = list()
    factor_2_list = [inp_ns]
    
    
    
    solutions = [[1,1,1,1]]
    
    if (solution == True and mode == ""):

        for idx_1 in reversed(range(2, hid_ns + 1)):

            if(hid_ns % idx_1 == 0):

                factor_1_list.append((idx_1)) 

        
        for i in factor_1_list:
            
            for j in factor_2_list:

                solutions.append([i, j, j, i])

        print(solutions)


    elif (solution == False and mode == "Performance"):

        factor_1 = hid_ns
        factor_2 = inp_ns
        factor_3 = out_ns
        factor_4 = hid_ns

    elif (solution == False and mode == "Cost"):

        factor_1 = 1
        factor_2 = 1
        factor_3 = 1
        factor_4 = 1


    else:

        print("Hi.")
        pass

    
    # Estimate Function

    print(f"You have {len(solutions)} solutions.\n")

    for i in range(len(solutions)):

        print(f"Solution {i} -> Estimated Area:        Estimated Latency:       \n")


    key = int(input("Which solution you prefer ? \n"))

    factor_1 = solutions[key][0]
    factor_2 = solutions[key][1]
    factor_3 = solutions[key][2]
    factor_4 = solutions[key][3]

    
    create_h_file("Hardware Phase\HENNC.h", inp_ns, hid_ns, out_ns)
    create_cpp_file("Hardware Phase\HENNC.cpp", sample, factor_1, factor_2, factor_3, factor_4, out_ns, one_mac, no_dsp)
    create_testBench_file("Hardware Phase\ test_bench.cpp", x_0, y_0, z_0)



TOP(3, 8, 3, 100, 0.534522473812, 0.267261236906, 0.80178374052, 0, 0, 1, "")




   
    