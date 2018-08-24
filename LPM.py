import numpy as np
import cv2
from matplotlib import pyplot as plt
import heapq
def read_img():
    img1 = cv2.imread('D:\woa.jpg')          # queryImage
    img2 = cv2.imread('D:\wo.jpg') # trainImage
# Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
# BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)
    return matches
# Apply ratio test
#距离匹配
def match(matches,t):
    good = []
    for m,n in matches:
        if m.distance < t*n.distance:
            good.append([m])
    return good
#匹配对应的特征点与特征描述符
def new_img(good):
    img_kp1=[]
    img_kp2=[]
    img_des1=[]
    img_des2=[]
    for i in good:
        img_kp1.append(kp1[i[0].queryIdx])
        img_kp2.append(kp2[i[0].trainIdx])
        img_des1.append(des1[i[0].queryIdx])
        img_des2.append(des2[i[0].trainIdx])
    return img_kp1,img_kp2,img_des1,img_des2
#print(len(img_kp1))
#print(len(img_kp2))
#print(len(img_des1))
#print(len(img_des2))
#print(img_kp1[0])
#nei=[[] for i in range(len(img_des2))]
#for i in range(len(img_des2)):
#    nei[2].append(np.linalg.norm(img_des2[4]-img_des2[i]))
#print(sorted(nei[2]))
#构建邻域
def nei_con1(img_des):
    nei=[[] for i in range(len(img_des))]
    for i in range(len(img_des)):
        for j in range(len(img_des)):
            nei[i].append(np.linalg.norm(img_des[i]-img_des[j]))#欧式距离
    con=[[] for i in range(len(img_des))]
    for i in range(len(nei)):
        con[i]=list(map(nei[i].index,heapq.nsmallest(5,nei[i])))#以heapq筛选最小距离，map取对应索引值
    return con
#以真实内部集合的近似构建邻域
def nei_con2(des1,des2):
    nei1=[[] for i in range(len(des1))]
    for i in range(len(des1)):
        for j in range(len(des2)):
            nei1[i].append(np.linalg.norm(des1[i]-des2[j]))
    con1=[[] for i in range(len(des1))]
    for i in range(len(nei1)):
        con1[i]=list(map(nei1[i].index,heapq.nsmallest(5,nei1[i])))
    return con1
#成本函数
def cost(nei_con1,nei_con2):
    pi=[]
    d=0
    dy=0
    dx=0
    for i in range(len(nei_con1)):
        for j in range(len(nei_con1[0])-1):
            if nei_con2[i][j+1] in nei_con1[i]:#在Nx内，Ny是否存在
                dy=1
                d+=dy
            else:
                dy=0
                d+=dy
            if nei_con1[i][j+1] in nei_con2[i]:#在Ny内，Nx是否存在
                dx=1
                d+=dx
            else:
                dx=0
                d+=dx
        if d<=6:#成本符合值
            pi.append(1)
        else:
            pi.append(0)
        d=0
    return pi
#真实内部集合的近似
def IO(pi,img_des1,img_des2,img_kp1,img_kp2):
    IO_index=[]
    for i,j in enumerate(pi):
        if j==1:
            IO_index.append(i)
#        else:
#            continue
    IO_kp1=[]
    IO_kp2=[]
    IO_des1=[]
    IO_des2=[]
    for i in range(len(IO_index)):
        IO_kp1.append(img_kp1[IO_index[i]])
        IO_kp2.append(img_kp2[IO_index[i]])
        IO_des1.append(img_des1[IO_index[i]])
        IO_des2.append(img_des2[IO_index[i]])
    return IO_index,IO_kp1,IO_kp2,IO_des1,IO_des2
#最优化匹配
def opti(I_pi,good):
    index=[]#筛选最优化匹配的索引
    for i,j in enumerate(I_pi):
        if j==1:
            index.append(i)
    optimize=[]
    for i in range(len(index)):
        optimize.append(good[index[i]])
        
    return optimize
    
    
    
if __name__=='__main__':
    matches=read_img()#读取图像，计算特征点与特征对应关系
    good=match(matches,0.6)#距离比去除不匹配
    img_kp1,img_kp2,img_des1,img_des2=new_img(good)#去除不匹配后的特征点与特征对应关系
    nei_co1=nei_con1(img_des1)#邻域Nx
    nei_co2=nei_con1(img_des2)#邻域Ny
#    print(nei_con1[0])
#    print(nei_con2[0])
    pi=cost(nei_co1,nei_co2)#成本计算
#    print(pi)
    IO_index1,IO_kp1,IO_kp2,IO_des1,IO_des2=IO(pi,img_des1,img_des2,img_kp1,img_kp2)#真实内部集合的近似
    IO_con1=nei_con2(img_des1,IO_des1)#新的Nx
    IO_con2=nei_con2(img_des2,IO_des2)#新的Ny
#    print(len(IO_index1))
#    print(len(IO_des1))
 
    IO_pi=cost(IO_con1,IO_con2)#新成本
    

#    I_index,I_kp1,I_kp2,I_des1,I_des2=IO(IO_pi,img_des1,img_des2,img_kp1,img_kp2)
#    print(len(IO_pi))
    #print(len(I_des1))
    optimize=opti(IO_pi,good)#最优化匹配
    print('最优化匹配个数',len(optimize))

        
# cv2.drawMatchesKnn expects list of lists as matches.
    img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,optimize,None,flags=2)
    plt.imshow(img3),plt.show()
    img4=cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
    plt.imshow(img4),plt.show()
    print('原始匹配个数',len(good))
