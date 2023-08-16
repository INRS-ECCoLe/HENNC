
def estimate (inp_ns, hid_ns, solutions):
    
    fu_coeff = {"c_1": 369, "c_2": 666, "c_3": 698, "B": 8704}
    pu1_coeff = {"c_1": 4176, "c_2": -9169, "c_3": 6780, "B": -26471}
    pu2_coeff = {"c_1": 2179, "c_2": -4171, "c_3": 3625, "B": -9347}
    pu3_coeff = {"c_1": 841, "c_2": 3824, "c_3": 2168, "B": -2935}
    rolled_coeff = {"c_1": 192, "c_2": 1257, "c_3": 1109, "B": 12405}
    
    estimated_lut = [0] * len(solutions)
    estimated_dsp = [0] * len(solutions)
    estimated_throughput = [0] * len(solutions)
    
    fu_cost = E_cost(inp_ns, hid_ns, fu_coeff["c_1"], fu_coeff["c_2"], fu_coeff["c_3"], fu_coeff["B"])
    rolled_cost = E_cost(inp_ns, hid_ns, rolled_coeff["c_1"], rolled_coeff["c_2"], rolled_coeff["c_3"], rolled_coeff["B"])
    
    if (len(solutions) < 3):
        
        estimated_lut = [fu_cost] + [rolled_cost]
        
    else:
        
        
        if (len(solutions)) == 3:
            
            pu1_cost = E_cost(inp_ns, hid_ns, pu1_coeff["c_1"], pu1_coeff["c_2"], pu1_coeff["c_3"], pu1_coeff["B"])
            estimated_lut = [fu_cost] + [pu1_cost] + [rolled_cost]
            
        elif (len(solutions)) == 4:
            
            pu1_cost = E_cost(inp_ns, hid_ns, pu1_coeff["c_1"], pu1_coeff["c_2"], pu1_coeff["c_3"], pu1_coeff["B"])
            pu2_cost = E_cost(inp_ns, hid_ns, pu2_coeff["c_1"], pu2_coeff["c_2"], pu2_coeff["c_3"], pu2_coeff["B"])
            estimated_lut = [fu_cost] + [pu1_cost] + [pu2_cost] + [rolled_cost]
            
        elif (len(solutions)) == 5:
            
            pu1_cost = E_cost(inp_ns, hid_ns, pu1_coeff["c_1"], pu1_coeff["c_2"], pu1_coeff["c_3"], pu1_coeff["B"])
            pu2_cost = E_cost(inp_ns, hid_ns, pu2_coeff["c_1"], pu2_coeff["c_2"], pu2_coeff["c_3"], pu2_coeff["B"])
            pu3_cost = E_cost(inp_ns, hid_ns, pu3_coeff["c_1"], pu3_coeff["c_2"], pu3_coeff["c_3"], pu3_coeff["B"])
            estimated_lut = [fu_cost] + [pu1_cost] + [pu2_cost] + [pu3_cost] + [rolled_cost]
            
            
            
    
    return (estimated_lut, estimated_dsp, estimated_throughput)   


        
def E_cost(x, y, c_1, c_2, c_3, B):

  res = (c_1 * x * y) + (c_2 * x) + (c_3 * y) + B
  
  return res