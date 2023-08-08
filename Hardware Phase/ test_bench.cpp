
#include "HENNC.h"



int main ()
{

	data_t t_i [inp_n] = {0.534522473812, 0.267261236906, 0.80178374052};

	data_t t_w1[inp_n][hid_n] = {};

	data_t t_b1[hid_n] = {};

	data_t t_w2[hid_n][out_n] = {};

	data_t t_b2[out_n] = {};

	data_t t_n[out_n] = {};

	stream i_t;
	stream w1_t;
	stream w2_t;
	stream b1_t;
	stream b2_t;


	for (int i = 0; i < inp_n; i++)
	{
		i_t.write(t_i[i]);
	}


    ifstream fin1;
    stringstream ss1;
    ss1 << "w_1.txt";
    fin1.open(ss1.str().c_str());
    for (int i = 0; i < inp_n; i++)
    {
        for (int j = 0; j < hid_n; j++)
        {
            fin1 >> t_w1[i][j];
            w1_t.write(t_w1[i][j]);
		}
	}

    ifstream fin2;
    stringstream ss2;
    ss2 << "b_1.txt";
    fin2.open(ss2.str().c_str());
    for (int i = 0; i < hid_n; i++)
    {
        fin2 >> t_b1[i];
        b1_t.write(t_b1[i]);

	}

    ifstream fin3;
    stringstream ss3;
    ss3 << "w_2.txt";
    fin3.open(ss3.str().c_str());
    for (int i = 0; i < hid_n; i++)
    {
        for (int j = 0; j < out_n; j++)
        {
            fin3 >> t_w2[i][j];
            w2_t.write(t_w2[i][j]);
		}
	}

    ifstream fin4;
    stringstream ss4;
    ss4 << "b_2.txt";
    fin4.open(ss4.str().c_str());
    for (int i = 0; i < out_n; i++)
    {
        fin4 >> t_b2[i];
        b2_t.write(t_b2[i]);
	}

    if (!fin1 | !fin2 | !fin3 | !fin4) {
        cout << "Open txt error in reading bias and weights";
        return -1;
	}


    fin1.close();
    fin2.close();
    fin3.close();
    fin4.close();


    ChaoticOscillator(i_t, w1_t, w2_t, b1_t, b2_t, t_n);

    
	return 0;
}


