import matplotlib.pyplot as plt
import numpy as np
import model

model = model.fromFile('output.txt')

N=2000
x = np.random.rand(N)
y = np.random.rand(N)

x1=[]
max=[]
min=[]
mean=[]

x=model.data[:,1]
x=model.data[:,5]
x=np.around(x,-3)
for i in range(0,len(x)-1):
	if x[i] in x1:
		index=x1.index(x[i])
		mean[index]+=y[i]
		if max[index]<y[i]:
			max[index]=y[i]
		if min[index]>y[i]:
			min[index]=y[i]
	else:
		x1.append(x[i])
		max.append(y[i])
		min.append(y[i])
		mean.append(y[i])

unique, counts = np.unique(x, return_counts=True)

for unique in x1:
	index=x1.index(unique)
	mean[index]=mean[index]/counts[index]
print(x1,min,mean) 
plt.plot(x1, min, 'b',mean,'k',max,'r')
#plt.scatter(x, y,alpha=0.5)
plt.show()