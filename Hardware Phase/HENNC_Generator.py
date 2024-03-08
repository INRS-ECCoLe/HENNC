import argparse
import yaml
from Analyzer import *



with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    

inp_ns = config['inp_ns']
hid_ns = config['hid_ns']
out_ns = config['out_ns']
sample = config['sample']
x_0 = config['x_0']
y_0 = config['y_0']
z_0 = config['z_0']
no_dsp = config['no_dsp']

parser = argparse.ArgumentParser()

parser.add_argument("-g", "--generate", help="Generate HENNC HLS model", action='store_true')
parser.add_argument("-p", "--performance", help="Generate high-performance HENNC HLS model", action='store_true')
parser.add_argument("-i", "--interactive", help="Interactive generation of HENNC HLS model", action='store_true')
parser.add_argument("-a", "--analyze", help="Analyze different solutions", action='store_true')
parser.add_argument("-f", "--file", help="YAML file with configuration", required=True)

args = parser.parse_args()

print( "generate {}       interactive {}          analyze {} ".format(
        args.generate,
        args.interactive,
        args.analyze
        ))


# default mode : generate_c
mode = 'generate_c'
if args.performance == True:
    mode = 'generate_p'
elif args.generate == True:
    mode = 'generate_c'
elif args.interactive == True:
    mode = 'interactive'
elif args.analyze == True:
    mode = 'analyze'
TOP(inp_ns, hid_ns, out_ns, sample, x_0, y_0, z_0, no_dsp, mode)