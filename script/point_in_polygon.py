import argparse
from matplotlib import path
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument('--input', help='input gmt file')
parser.add_argument('--polygon', help='polygon file')
parser.add_argument('--output', help='ouput gmt file')


args = parser.parse_args()
print(args)


def smooth_line(data,step):
    [len_data,wid_data]=data.shape
    len_data=len_data-step
    output=np.zeros([len_data,wid_data])
    for i in range(len(data)-step):
        for w in range(wid_data):
            output[i,w]=np.average(data[i:i+step,w])
    return output







polygon_data=np.loadtxt(args.polygon)
p = path.Path(polygon_data)
input=np.loadtxt(args.input)
index=p.contains_points(input)
#print(input[1])
output=input[index]
output_smooth=smooth_line(output,4)
#print(output[1])



np.savetxt(args.output,output_smooth,delimiter=' ',fmt='%10.13f')
