import argparse
import csv
from Analyzer import *
parser = argparse.ArgumentParser()




#with open('config_file.csv') as csv_file:

    #csv_reader = csv.reader(csv_file, delimiter=',')

inp_ns = 3
hid_ns = 8
out_ns = 3
sample = 100
x_0 = 0.534522473812
y_0 = 0.267261236906
z_0 = 0.80178374052

#-db DATABSE -u USERNAME -p PASSWORD -size 20
parser.add_argument("-g", "--generate", help="Generate HENNC HLS model", action='store_true')
parser.add_argument("-p", "--performance", help="Generate high-performance HENNC HLS model", action='store_true')
parser.add_argument("-i", "--interactive", help="Interactive generation of HENNC HLS model", action='store_true')
parser.add_argument("-a", "--analyze", help="Analyze different solutions", action='store_true')

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
TOP(inp_ns, hid_ns, out_ns, sample, x_0, y_0, z_0, mode)