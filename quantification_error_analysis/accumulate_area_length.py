import numpy as np
import argparse
import matplotlib.pyplot as plt
import datetime

parser=argparse.ArgumentParser()
parser.add_argument('--input',help='input area change file')
parser.add_argument('--output',help='path to stole retreat rate')
args=parser.parse_args()

def convert_time(date):
    date=str(date)
    year=int(date[0:4])
    month=int(date[4:6])
    day=int(date[6:8])
    d1 = datetime.datetime(year,month,day)
    d2=datetime.datetime(year,1,1)
    intervel=d1-d2
    out_date=year+(intervel.days)/365.25
    return out_date

def accumulate(data):
    accu=np.zeros(len(data))
    for i in range(len(data)):
        accu[i]=np.sum(data[0:i+1])
    return accu


def cal_annual_rate(data):
    date=data[:,2]
    area=data[:,0]
    length=data[:,1]
    year_min=int(date[0])
    year_max=int(date[-1])
    p_area=[]
    p_length=[]
    plt.figure()
    #plt.plot(input_data[:, 2], input_data[:, 0])
    plt.plot(accu[:, 2], accu[:, 0])
    #plt.legend(('ori', 'accu'), loc='upper right')

    for i in range(year_min+1,year_max,1):
        index=np.where( (date > i-1) & (date < i+2))
        temp=np.array(date[index])
        p_area = np.polyfit(date[index],area[index],1)
        p_length = np.polyfit(date[index], length[index],1)
        z_area=np.polyval(p_area,date[index])
        z_length = np.polyval(p_length, date[index])
        plt.plot(date[index],z_area,color='red')
        with open(args.path+'/'+str(i)+'.txt', 'a') as log:
            out_massage='%s %.3f'%(args.name,p_length[0])
            log.writelines(out_massage + '\n')


        #plt.plot(date[index],z_length)
        print p_length[0],i
    p_area_t=np.polyfit(date,area,1)
    p_length_t = np.polyfit(date, length, 1)
    with open(args.path+'/'+'total.txt','a') as log_t:
        out_massage_t='%s %.3f'%(args.name,p_length_t[0])
        log_t.writelines(out_massage_t + '\n')
    print p_length_t[0]
    #plt.show()
    plt.savefig(args.output)
if __name__=='__main__':
    input_data=np.loadtxt(args.input)
    #for i in range(len(input_data)):
    #    input_data[i,2]=convert_time(input_data[i,2])
    accu=np.zeros(input_data.shape)
    accu[:,0]=accumulate(input_data[:,0])
    accu[:, 1] = accumulate(input_data[:, 1])
    accu[:,2]=input_data[:,2]
    accu[:,3]=input_data[:,3]
    np.savetxt(args.output,accu,fmt="%.4f %.4f %.4f %d",delimiter=" ")





