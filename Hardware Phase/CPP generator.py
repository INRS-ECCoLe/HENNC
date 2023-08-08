def create_cpp_file(filename, inp_sample:int):
    cpp_code = f"""
#include <iostream>

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

		Y[0] = y_reg[0];
		Y[1] = y_reg[1];
		Y[2] = y_reg[2];

		x_reg[0] = y_reg[0];
		x_reg[1] = y_reg[1];
		x_reg[2] = y_reg[2];


		sample++;
	}}


}}
"""

    with open(filename, "w") as file:
        file.write(cpp_code)

if __name__ == "__main__":

    cpp_filename = "Hardware Phase\HENNC.cpp"
    create_cpp_file(cpp_filename, 100)
    print(f"{cpp_filename} has been created.")