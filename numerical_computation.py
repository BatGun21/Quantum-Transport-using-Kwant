


import numpy  as np 
from matplotlib import pyplot as plt
a = np.random.random()*1
b = -1*(np.random.random()*10000)
c = np.random.random()*1000
a = float("{:.2f}".format(a))
b = float("{:.4f}".format(b))
c = float("{:.7f}".format(c))



num = 2*c
den = (-b - math.sqrt(b**2 - 4*a*c))
x = num/den




x= float("{:.8f}".format(x))
x



#another way 
num1 = (-b + math.sqrt(b**2 - 4*a*c))
den1 = 2*a
x1 = num1/den1
x1 = float("{:.8f}".format(x1))
x1





a , b ,c ,x , x1 = [] , [], [] , [] ,[]
np.asarray(a)
n= 10
for i in range(n):
    a.append(float("{:.2f}".format(np.random.random()*1)))
    b.append(float("{:.4f}".format(np.random.random()*10000)))
    c.append(float("{:.7f}".format(np.random.random()*1000)))
   





for i in range(n):
    a = np.random.random()*1
    b = np.random.random()*10000
    c = np.random.random()*1000
    a = float("{:.2f}".format(a))
    b = float("{:.4f}".format(b))
    c = float("{:.7f}".format(c))
    num = 2*c
    den = (-b - math.sqrt(b**2 - 4*a*c))
    x_ = (num/den)
    x.append(float("{:.8f}".format(x_)))
    
    
    num1 = (-b + math.sqrt(b**2 - 4*a*c))
    den1 = 2*a
    x_1 = num1/den1
    x1.append(float("{:.8f}".format(x_1)))



plt.figure()
plt.plot(x,x1)


def fn(n):
    k=1
    j = 2
    I0 = 1 - (1/np.e)
    I = [I0]
    I2 = [I0]
    while (k<= n):
        Ik1 = 1 - k*I[k-1]
        I.append(Ik1)
        k +=1
    while (j<=n):  
        Ip1 = (1/np.pi) - ((j*(j-1))/((np.pi)**2))*I[j-2]
        I2.append(Ip1)
        j +=2
    
    x = np.arange(0,n+1) 
    x1 = np.arange(0,n+1,2)
    plt.figure()
    plt.plot(x,I, 'r')
    plt.plot(x1,I2,'b')
    plt.show()
    print(I)
    print(I2)


# In[381]:


fn(6)


# In[ ]:





# 

# In[386]:


#4
from statistics import mean 
x = [3,5,7,3,8,4,9,4]




def std_fn(x):
    x_m = mean(x)
    n = len(x)
    p1 = 0
    p2 = 0
    for i in range(n):
        p1 += (x[i] - x_m)**2
        s1 = p1/n
        
        p2 += (x[i]**2 - x_m**2)
        s2 = p2/n
        
    return s1 , s2





from numpy.random import seed
from numpy.random import rand 
from random import gauss
# seed random number generator
seed(1)
# generate some random numbers
x = -1*rand(10)


# In[422]:


std_fn(x)


# In[ ]:




