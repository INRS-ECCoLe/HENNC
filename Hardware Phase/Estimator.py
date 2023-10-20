
def estimate (inp_ns, hid_ns, no_dsp, solutions):
    
    fu_coeff = {"c_1": 422, "c_2": -1347, "c_3": -294, "B": 4253}
    pu1_coeff = {"c_1": 299, "c_2": -549, "c_3": -33, "B": 479}
    pu2_coeff = {"c_1": 399, "c_2": -1931, "c_3": -529, "B": 5629}
    pu3_coeff = {"c_1": 414, "c_2": -3414, "c_3": -778, "B": 12659}
    rolled_coeff = {"c_1": 336, "c_2": -1480, "c_3": -545, "B": 4803}
    
    n_mult = []
    n_add = []
    factor_split = []
    estimated_lut = ['NE'] * len(solutions)
    estimated_dsp = []
    estimated_latency = []
    
    fu_cost = E_cost(inp_ns, hid_ns, fu_coeff["c_1"], fu_coeff["c_2"], fu_coeff["c_3"], fu_coeff["B"])
    pu1_cost = E_cost(inp_ns, hid_ns, pu1_coeff["c_1"], pu1_coeff["c_2"], pu1_coeff["c_3"], pu1_coeff["B"])
    pu2_cost = E_cost(inp_ns, hid_ns, pu2_coeff["c_1"], pu2_coeff["c_2"], pu2_coeff["c_3"], pu2_coeff["B"])
    pu3_cost = E_cost(inp_ns, hid_ns, pu3_coeff["c_1"], pu3_coeff["c_2"], pu3_coeff["c_3"], pu3_coeff["B"])
    rolled_cost = E_cost(inp_ns, hid_ns, rolled_coeff["c_1"], rolled_coeff["c_2"], rolled_coeff["c_3"], rolled_coeff["B"])
    

    for i in range(len(solutions)):

        factor_split.append(solutions[i][0:2])
        n_mult.append(factor_split[i][0] * factor_split[i][1])
        n_add.append((n_mult[i] // inp_ns) if n_mult[i] != 1 else 1)


    if (no_dsp == False):

        # Estimate DSP and Latency

        for i in range(len(solutions)):

            estimated_dsp.append((n_mult[i] * 3) + (n_add[i] * 2))
            tmp = latency((len(solutions) - i) - 1, inp_ns, hid_ns)
            estimated_latency.append('NE' if tmp < 0 else int(tmp))

       # Estimate LUT
       
        if (len(solutions) < 3):
        
            estimated_lut = [fu_cost] + [rolled_cost]
        
        else:
        
        
            if (len(solutions)) == 3:
            
                estimated_lut = [fu_cost] + [pu1_cost] + [rolled_cost]
            
            elif (len(solutions)) == 4:
            
                estimated_lut = [fu_cost] + [pu1_cost] + [pu2_cost] + [rolled_cost]
            
            elif (len(solutions)) == 5:
            
                estimated_lut = [fu_cost] + [pu1_cost] + [pu2_cost] + [pu3_cost] + [rolled_cost]

            elif (len(solutions)) > 5:

            
                estimated_lut[0:4] = [fu_cost] + [pu1_cost] + [pu2_cost] + [pu3_cost]
                estimated_lut[len(estimated_lut) - 1] = rolled_cost

    else:

        estimated_dsp = [0] * len(solutions)

        for i in range(len(solutions)):

            tmp = latency_no_dsp((len(solutions) - i) - 1, inp_ns, hid_ns)
            estimated_latency.append('NE' if tmp < 0 else int(tmp))

       
        if (len(solutions)) == 3:
            
            fu_cost += E_cost_nodsp(n_mult[0], n_add[0])
            pu1_cost += E_cost_nodsp(n_mult[1], n_add[1])
            rolled_cost += E_cost_nodsp(n_mult[2], n_add[2])

            estimated_lut = [fu_cost] + [pu1_cost] + [rolled_cost]
            
        elif (len(solutions)) == 4:

            fu_cost += E_cost_nodsp(n_mult[0], n_add[0])
            pu1_cost += E_cost_nodsp(n_mult[1], n_add[1])
            pu2_cost += E_cost_nodsp(n_mult[2], n_add[2])
            rolled_cost += E_cost_nodsp(n_mult[3], n_add[3])
            
            estimated_lut = [fu_cost] + [pu1_cost] + [pu2_cost] + [rolled_cost]
            
        elif (len(solutions)) == 5:

            fu_cost += E_cost_nodsp(n_mult[0], n_add[0])
            pu1_cost += E_cost_nodsp(n_mult[1], n_add[1])
            pu2_cost += E_cost_nodsp(n_mult[2], n_add[2])
            pu3_cost += E_cost_nodsp(n_mult[3], n_add[3])
            rolled_cost += E_cost_nodsp(n_mult[4], n_add[4])
            
            estimated_lut = [fu_cost] + [pu1_cost] + [pu2_cost] + [pu3_cost] + [rolled_cost]

        elif (len(solutions)) > 5:

            fu_cost += E_cost_nodsp(n_mult[0], n_add[0])
            pu1_cost += E_cost_nodsp(n_mult[1], n_add[1])
            pu2_cost += E_cost_nodsp(n_mult[2], n_add[2])
            pu3_cost += E_cost_nodsp(n_mult[3], n_add[3])
            rolled_cost += E_cost_nodsp(n_mult[4], n_add[4])
            
            estimated_lut[0:4] = [fu_cost] + [pu1_cost] + [pu2_cost] + [pu3_cost]
            estimated_lut[len(estimated_lut) - 1] = rolled_cost


    return (estimated_lut, estimated_dsp, estimated_latency)   


        
def E_cost(x, y, c_1, c_2, c_3, B):

  res = (c_1 * x * y) + (c_2 * x) + (c_3 * y) + B
  
  return res


def E_cost_nodsp(mul, add):

    res_1 = (mul * 73) + (add * 192)
    res = ((mul * 572) + (add * 347)) - (res_1)

    return res


def latency (P, x, y):

    lat_dsp = ((-0.6 * P**3) + (6.32 * P**2) + (-25.86 * P) + (45.38)) * (x * y)

    return lat_dsp

def latency_no_dsp (P, x, y):

    lat_no_dsp = ((-0.6 * P**3) + (6.9 * P**2) + (-26.92 * P) + (41.74)) * (x * y)

    return lat_no_dsp