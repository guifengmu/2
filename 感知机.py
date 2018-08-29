import numpy as np
from matplotlib import pyplot as plt
group=np.array([[3,3],[4,3],[1,1]])
labels=[1,1,-1]


w=np.array([0,0])
b=0
t=1
print(group.shape[0])
def update(row,label):
#    for i in range(group.shape[0]):
#        L=np.dot(group[i],w.T)+b
#        if L<=0:
    global w, b
    w+=label*row
    b+=label
    return w,b
def cal(row,label):
    global w, b
    Loss=np.dot(row,w.T)+b
    Loss*=label
    return Loss
    
def perceptron():
    global w, b
    isFind=False
    while(not isFind):
        for i in range(group.shape[0]):
            if cal(group[i],labels[i]) <=0:
                print(w,b)
                w,b=update(group[i],labels[i])
                break
            elif i==group.shape[0]-1:
                print(w,b)
                isFind=True
def show():
    x, y, x_, y_= [],[],[],[]
    for i in range(group.shape[0]):
        if(labels[i]==1):
            x.append(group[i,0])
            y.append(group[i,1])
        else:
            x_.append(group[i,0])
            y_.append(group[i,1]) 
        #对中文显示进行支持设置中文字体     
    #plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.plot(x,y,'bo',x_,y_,'rx')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot([0,3], [3,0], 'bo-')
    plt.title('ganzhiji')
    plt.show()
                
if __name__ == '__main__':
    perceptron()
    show()
        

