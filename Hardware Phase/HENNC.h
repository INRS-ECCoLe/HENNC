
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

const int inp_n = 3;
const int hid_n = 8;
const int out_n = 3;


void ChaoticOscillator(stream &X, stream &W1, stream &W2, stream &B1, stream &B2, data_t Y[out_n]);

void mlp_core(data_t mlp_in[inp_n], data_t w1_in[inp_n][hid_n], data_t w2_in[hid_n][out_n], data_t b1_in[hid_n], data_t b2_in[out_n], data_t mlp_out[out_n]);

data_t ReLU (data_t inp_relu);

