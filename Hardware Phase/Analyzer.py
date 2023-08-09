
from HLS_Generator import *

def TOP (inp_ns, hid_ns, out_ns, sample, x_0, y_0, z_0, one_mac: bool, no_dsp: bool, solution: bool, mode: str):

    factor_1 = factor_2 = factor_3 = factor_4 = 1

    factor_1_list = list()
    factor_2_list = list()
    factor_3_list = list()
    factor_4_list = list()

    solutions = list()
    
    if (solution == True and mode == ""):

        for idx_1 in reversed(range(1, hid_ns + 1)):

            if(hid_ns % idx_1 == 0):

                factor_1_list.append((idx_1)) 

        print(factor_1_list)


        for idx_2 in reversed(range(1, inp_ns + 1)):

            if(inp_ns % idx_2 == 0):

                factor_2_list.append((idx_2)) 

        print(factor_2_list)

        for idx_3 in reversed(range(1, out_ns + 1)):

            if(out_ns % idx_3 == 0):

                factor_3_list.append((idx_3)) 

        print(factor_3_list)


        for idx_4 in reversed(range(1, hid_ns + 1)):

            if(hid_ns % idx_4 == 0):

                factor_4_list.append((idx_4)) 

        print(factor_4_list)



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

    create_h_file("Hardware Phase\HENNC.h", inp_ns, hid_ns, out_ns)
    create_cpp_file("Hardware Phase\HENNC.cpp", sample, factor_1, factor_2, factor_3, factor_4, out_ns, one_mac, no_dsp)
    create_testBench_file("Hardware Phase\ test_bench.cpp", x_0, y_0, z_0)


TOP(3, 8, 3, 100, 0.534522473812, 0.267261236906, 0.80178374052, 1, 1, True, "")




   
    