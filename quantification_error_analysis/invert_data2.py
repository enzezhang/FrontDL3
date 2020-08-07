import argparse

import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument('--input', help='input gmt file')

parser.add_argument('--output', help='ouput gmt file')


args = parser.parse_args()
print(args)
input_data=np.loadtxt(args.input)
output_data=input_data[::-1]
np.savetxt(args.output,output_data,delimiter=' ',fmt='%10.13f')