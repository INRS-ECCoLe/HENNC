
#include "HENNC.h"

void ChaoticOscillator(stream &X, stream &W1, stream &W2, stream &B1, stream &B2, data_t Y[out_n])
{

#pragma HLS ARRAY_PARTITION dim=1 type=complete variable=Y
#pragma HLS INTERFACE mode=axis port=B2
#pragma HLS INTERFACE mode=axis port=B1
#pragma HLS INTERFACE mode=axis port=W2
#pragma HLS INTERFACE mode=axis port=W1
#pragma HLS INTERFACE mode=axis port=X



    static data_t x_reg [inp_n] = {};
#pragma HLS ARRAY_RESHAPE dim=1 type=complete variable=x_reg

	static data_t w1_reg [inp_n][hid_n] = {};
#pragma HLS ARRAY_RESHAPE dim=0 type=complete variable=w1_reg

	static data_t w2_reg [hid_n][out_n] = {};
#pragma HLS ARRAY_RESHAPE dim=0 type=complete variable=w2_reg

	static data_t b1_reg [hid_n] = {};
#pragma HLS ARRAY_RESHAPE dim=1 type=complete variable=b1_reg

	static data_t b2_reg [out_n] = {};
#pragma HLS ARRAY_RESHAPE dim=1 type=complete variable=b2_reg

	static data_t y_reg [out_n] = {};
#pragma HLS ARRAY_RESHAPE dim=1 type=complete variable=y_reg

	read_x:for (int idx = 0; idx < inp_n; idx++)
	{
#pragma HLS PIPELINE
		x_reg[idx] = X.read();
	}


	read_w1:for (int idx = 0; idx < inp_n; idx++)
	{
		for (int idy = 0; idy < hid_n; idy++)
		{
#pragma HLS PIPELINE
			w1_reg[idx][idy] = W1.read();
		}
	}

	read_w2:for (int idx = 0; idx < hid_n; idx++)
	{
		for (int idy = 0; idy < out_n; idy++)
		{
#pragma HLS PIPELINE
			w2_reg[idx][idy] = W2.read();
		}
	}

	read_b1:for (int idx = 0; idx < hid_n; idx++)
	{
#pragma HLS PIPELINE
		b1_reg[idx] = B1.read();
	}

	read_b2:for (int idx = 0; idx < out_n; idx++)
	{
#pragma HLS PIPELINE
		b2_reg[idx] = B2.read();
	}

    	int sample = 0;

	FCNN_label0:while (sample < 100)
	{



		mlp_core (x_reg, w1_reg, w2_reg, b1_reg, b2_reg, y_reg);

        Y[0] = y_reg[0]; 
		Y[1] = y_reg[1]; 
		Y[2] = y_reg[2]; 
		
        x_reg[0] = y_reg[0]; 
		x_reg[1] = y_reg[1]; 
		x_reg[2] = y_reg[2]; 
		

		sample++;
	}


}

void mlp_core(data_t mlp_in[inp_n], data_t w1_in[inp_n][hid_n], data_t w2_in[hid_n][out_n], data_t b1_in[hid_n], data_t b2_in[out_n], data_t mlp_out[out_n])

{




	data_t acc_1, acc_2 = 0;





	static data_t hidden_n [hid_n] = {};
#pragma HLS ARRAY_RESHAPE dim=1 type=complete variable=hidden_n



	for (int i = 0; i < hid_n; i++)
	{
#pragma HLS UNROLL factor= 4


		acc_1 = 0;

		for (int j = 0; j < inp_n; j++)
		{
#pragma HLS UNROLL factor= 3

			acc_1 += mlp_in[j] * w1_in[j][i];
		}

		acc_1 += b1_in[i];
		hidden_n[i] = ReLU(acc_1);
	}

	for (int i = 0; i < out_n; i++)
	{
#pragma HLS UNROLL factor= 3



		acc_2 = 0;

		for (int j = 0; j < hid_n; j++)
		{
#pragma HLS UNROLL factor= 4

			acc_2 += hidden_n[j] * w2_in[j][i];
		}

		acc_2 += b2_in[i];
		mlp_out[i] = acc_2;
	}
}



data_t ReLU (data_t inp_relu)

{
#pragma HLS INLINE
	data_t out_relu;

	out_relu = (hls::signbit(inp_relu) == 0) ? (inp_relu) : (0);

	return (out_relu);
}
