import torch
import torch.nn as nn
import numpy as np
gt=np.array([0,0,0,0,1,1])
pre=np.array([1,0,0,0,0,0.6])
pred = np.argmax(pre, axis=1)
num_class=2

mask= (gt >= 0) & (gt < num_class)
label = num_class * gt[mask].astype('int') + np.round(pre[mask]).astype('int')
count = np.bincount(label, minlength=num_class**2)
confusion_matrix = count.reshape(num_class, num_class)



print("test")