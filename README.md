# HENNC

## Table of contents
* [Description](#Description)
* [Technologies](#Technologies)
* [Requirements](#Requirements)

## Description
The HENNC framework automates the generation of hardware cores for ANN-based chaotic oscillators tailored for FPGAs. The framework uses user-defined hyper-parameters to train an ANN model that approximates a chaotic system, and then explores the design space to generate various potential hardware architectures for implementing the chaotic system. Each architecture provides a unique trade-off between hardware cost and throughput. After selecting a solution, the framework generates the corresponding high-level synthesis (HLS) code and a validation testbench. The results show that the HENNC framework is not only capable of speeding up the hardware design process, but also produces efficient architectures that outperform previous manually designed works in terms of hardware cost and throughput.

HENNC has been innovated and developed at the Edge Computing, Communication, and Learning Lab at INRS University in close collaboration with Prof. Pierre Langlois' research group at Polytechnique Montréal.
	
## Technologies
* AMD_Xilinx Vitis HLS 2023.1
* AMD_Xilinx Vivado ML 2023.1
* Keras (high-level API of the TensorFlow )
* Python 3.10
	
## Requirements
$ pip install numpy pandas matplotlib scipy scikit-learn

## Components
This repository consists of two components: Software design phase and Hardware design phase

### Software Design



### Hardware Design



