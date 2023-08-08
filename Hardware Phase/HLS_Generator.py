
def create_h_file(filename, inp_ns: int, hid_ns: int, out_ns: int):

	h_code = f"""
#pragma once

#include <iostream>
#include <fstream>
#include <cstring>
#include <sstream>
#include <hls_stream.h>
#include <hls_math.h>

using namespace std;

typedef float data_t;

typedef hls::stream <data_t> stream;

const int inp_n = {inp_ns};
const int hid_n = {hid_ns};
const int out_n = {out_ns};


void ChaoticOscillator(stream &X, stream &W1, stream &W2, stream &B1, stream &B2, data_t Y[out_n]);

void mlp_core(data_t mlp_in[inp_n], data_t w1_in[inp_n][hid_n], data_t w2_in[hid_n][out_n], data_t b1_in[hid_n], data_t b2_in[out_n], data_t mlp_out[out_n]);

data_t ReLU (data_t inp_relu);

"""
	with open(filename, "w") as file:
		
		file.write(h_code)


def create_cpp_file(filename, inp_sample: int, out_n: int, one_mac: bool, no_dsp: bool):
    
	output_reg = ""
	feedback = ""

	factor_1 = 8
	factor_2 = 3
	factor_3 = 3
	factor_4 = 8

	if (one_mac == True):

		factor_1 = factor_2 = factor_3 = factor_4 = 1

		alloc_1 = "#pragma HLS ALLOCATION operation instances=fmul limit=1"
		alloc_2 = "#pragma HLS ALLOCATION operation instances=fadd limit=1"
	
	else:
		alloc_1 = ""
		alloc_2 = ""

	if (no_dsp == True):
		
		bind_op1 = "#pragma HLS BIND_OP variable=acc_1 op=fadd impl=fabric"
		bind_op2 = "#pragma HLS BIND_OP variable=acc_1 op=fmul impl=fabric"
		bind_op3 = "#pragma HLS BIND_OP variable=acc_2 op=fadd impl=fabric"
		bind_op4 = "#pragma HLS BIND_OP variable=acc_2 op=fmul impl=fabric"
	
	else:

		bind_op1 = ""
		bind_op2 = ""
		bind_op3 = ""
		bind_op4 = ""
		



	for i in range (out_n):
    
		output_reg = output_reg + f"Y[{i}] = y_reg[{i}] \n\t\t"
		feedback = feedback + f"x_reg[{i}] = y_reg[{i}] \n\t\t"
	
	cpp_code = f"""
#include "HENNC.h"

void ChaoticOscillator(stream &X, stream &W1, stream &W2, stream &B1, stream &B2, data_t Y[out_n])
{{

#pragma HLS ARRAY_PARTITION dim=1 type=complete variable=Y
#pragma HLS INTERFACE mode=axis port=B2
#pragma HLS INTERFACE mode=axis port=B1
#pragma HLS INTERFACE mode=axis port=W2
#pragma HLS INTERFACE mode=axis port=W1
#pragma HLS INTERFACE mode=axis port=X



    static data_t x_reg [inp_n] = {{}};
#pragma HLS ARRAY_RESHAPE dim=1 type=complete variable=x_reg

	static data_t w1_reg [inp_n][hid_n] = {{}};
#pragma HLS ARRAY_RESHAPE dim=0 type=complete variable=w1_reg

	static data_t w2_reg [hid_n][out_n] = {{}};
#pragma HLS ARRAY_RESHAPE dim=0 type=complete variable=w2_reg

	static data_t b1_reg [hid_n] = {{}};
#pragma HLS ARRAY_RESHAPE dim=1 type=complete variable=b1_reg

	static data_t b2_reg [out_n] = {{}};
#pragma HLS ARRAY_RESHAPE dim=1 type=complete variable=b2_reg

	static data_t y_reg [out_n] = {{}};
#pragma HLS ARRAY_RESHAPE dim=1 type=complete variable=y_reg

	read_x:for (int idx = 0; idx < inp_n; idx++)
	{{
#pragma HLS PIPELINE
		x_reg[idx] = X.read();
	}}


	read_w1:for (int idx = 0; idx < inp_n; idx++)
	{{
		for (int idy = 0; idy < hid_n; idy++)
		{{
#pragma HLS PIPELINE
			w1_reg[idx][idy] = W1.read();
		}}
	}}

	read_w2:for (int idx = 0; idx < hid_n; idx++)
	{{
		for (int idy = 0; idy < out_n; idy++)
		{{
#pragma HLS PIPELINE
			w2_reg[idx][idy] = W2.read();
		}}
	}}

	read_b1:for (int idx = 0; idx < hid_n; idx++)
	{{
#pragma HLS PIPELINE
		b1_reg[idx] = B1.read();
	}}

	read_b2:for (int idx = 0; idx < out_n; idx++)
	{{
#pragma HLS PIPELINE
		b2_reg[idx] = B2.read();
	}}

    	int sample = 0;

	FCNN_label0:while (sample < {inp_sample})
	{{



		mlp_core (x_reg, w1_reg, w2_reg, b1_reg, b2_reg, y_reg);

        {output_reg}
        {feedback}

		sample++;
	}}


}}

void mlp_core(data_t mlp_in[inp_n], data_t w1_in[inp_n][hid_n], data_t w2_in[hid_n][out_n], data_t b1_in[hid_n], data_t b2_in[out_n], data_t mlp_out[out_n])

{{

{alloc_1}
{alloc_2}

	data_t acc_1, acc_2 = 0;
{bind_op1}
{bind_op2}
{bind_op3}
{bind_op4}

	static data_t hidden_n [hid_n] = {{}};
#pragma HLS ARRAY_RESHAPE dim=1 type=complete variable=hidden_n



	for (int i = 0; i < hid_n; i++)
	{{
#pragma HLS UNROLL factor= {factor_1}


		acc_1 = 0;

		for (int j = 0; j < inp_n; j++)
		{{
#pragma HLS UNROLL factor= {factor_2}

			acc_1 += mlp_in[j] * w1_in[j][i];
		}}

		acc_1 += b1_in[i];
		hidden_n[i] = ReLU(acc_1);
	}}

	for (int i = 0; i < out_n; i++)
	{{
#pragma HLS UNROLL factor= {factor_3}



		acc_2 = 0;

		for (int j = 0; j < hid_n; j++)
		{{
#pragma HLS UNROLL factor= {factor_4}

			acc_2 += hidden_n[j] * w2_in[j][i];
		}}

		acc_2 += b2_in[i];
		mlp_out[i] = acc_2;
	}}
}}



data_t ReLU (data_t inp_relu)

{{
#pragma HLS INLINE
	data_t out_relu;

	out_relu = (hls::signbit(inp_relu) == 0) ? (inp_relu) : (0);

	return (out_relu);
}}
"""

	with open(filename, "w") as file:

		file.write(cpp_code)


def create_testBench_file(filename, x_0: float, y_0: float, z_0: float):

	tb_code = f"""
#include "HENNC.h"



int main ()
{{

	data_t t_i [inp_n] = {{{x_0}, {y_0}, {z_0}}};

	data_t t_w1[inp_n][hid_n] = {{}};

	data_t t_b1[hid_n] = {{}};

	data_t t_w2[hid_n][out_n] = {{}};

	data_t t_b2[out_n] = {{}};

	data_t t_n[out_n] = {{}};

	stream i_t;
	stream w1_t;
	stream w2_t;
	stream b1_t;
	stream b2_t;


	for (int i = 0; i < inp_n; i++)
	{{
		i_t.write(t_i[i]);
	}}


    ifstream fin1;
    stringstream ss1;
    ss1 << "w_1.txt";
    fin1.open(ss1.str().c_str());
    for (int i = 0; i < inp_n; i++)
    {{
        for (int j = 0; j < hid_n; j++)
        {{
            fin1 >> t_w1[i][j];
            w1_t.write(t_w1[i][j]);
		}}
	}}

    ifstream fin2;
    stringstream ss2;
    ss2 << "b_1.txt";
    fin2.open(ss2.str().c_str());
    for (int i = 0; i < hid_n; i++)
    {{
        fin2 >> t_b1[i];
        b1_t.write(t_b1[i]);

	}}

    ifstream fin3;
    stringstream ss3;
    ss3 << "w_2.txt";
    fin3.open(ss3.str().c_str());
    for (int i = 0; i < hid_n; i++)
    {{
        for (int j = 0; j < out_n; j++)
        {{
            fin3 >> t_w2[i][j];
            w2_t.write(t_w2[i][j]);
		}}
	}}

    ifstream fin4;
    stringstream ss4;
    ss4 << "b_2.txt";
    fin4.open(ss4.str().c_str());
    for (int i = 0; i < out_n; i++)
    {{
        fin4 >> t_b2[i];
        b2_t.write(t_b2[i]);
	}}

    if (!fin1 | !fin2 | !fin3 | !fin4) {{
        cout << "Open txt error in reading bias and weights";
        return -1;
	}}


    fin1.close();
    fin2.close();
    fin3.close();
    fin4.close();


    ChaoticOscillator(i_t, w1_t, w2_t, b1_t, b2_t, t_n);

    
	return 0;
}}


"""
	with open(filename, "w") as file:
		
		file.write(tb_code)


if __name__ == "__main__":

	h_filename = "Hardware Phase\HENNC.h"
	cpp_filename = "Hardware Phase\HENNC.cpp"
	tb_filename = "Hardware Phase\ test_bench.cpp"

	create_h_file(h_filename, 3, 8, 3)
	create_cpp_file(cpp_filename, 100, 3, 0, 0)
	create_testBench_file(tb_filename, 0.534522473812, 0.267261236906, 0.80178374052)

	print(f"{h_filename} has been created.")
	print(f"{cpp_filename} has been created.")
	print(f"{tb_filename} has been created.")