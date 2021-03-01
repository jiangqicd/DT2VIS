#*******
#*******************
#用户行为序列推荐算法
#*******************
#*******
import numpy as np
import csv
import utils
import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from genSent import genQsents
from qt2vis import parse
import scipy.stats as stats
# 读取表格内容
tasks=["extremum","trend","find_value","correlation","difference","distribution","rank","proportion","aggregation"]

TTM = np.mat(np.zeros((9,9)))
#APM = np.mat(np.full((1,l),1/l))
TTM=[[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
     [0.12, 0.08, 0.13, 0.07, 0.14, 0.06, 0.1, 0.2, 0.2],
     [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
     [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
     [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
     [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
     [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
     [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
     [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2]]
#APM初始化
Atrs=[]
APM=[]
def getAttribute(table_path):
    table=pd.read_csv(table_path)
    for attribute in table.columns:
        if attribute.lower() not in utils.time and is_numeric_dtype(table[attribute]):
            Atrs.append(attribute)
def getAPM():
    for i in range(len(Atrs)):
        APM.append(round(1/len(Atrs),2))
def getTindex(in_t):  #找到输入的task对应矩阵中的index
    index=-1
    for t in tasks:
        index=index + 1
        if (t == in_t.lower()):
            print(index)
            break
    return index
def getAindex(in_a): #找到输入的atr对应矩阵中的index
    index=-1
    for t in Atrs:
        index=index+1
        if(t.lower()==in_a.lower()):
            break
    return index

def getTnext(in_t): #排序 找出概率最高的前两个task
    Tnext_list=[]
    index=getTindex(in_t)
    sort_array=np.argsort(TTM[index])
    l=len(sort_array)
    Tnext1_index=sort_array[l-1]
    Tnext2_index=sort_array[l-2]
    Tnext1=tasks[Tnext1_index]
    Tnext2 = tasks[Tnext2_index]
    Tnext_list.append(Tnext1)
    Tnext_list.append(Tnext2)
    #todo Update TTM based on user click feedback
    return Tnext_list

def getAnext(in_a,table_path): #排序 得到按概率从小到大排序的list,in_a必须是表头属性
    table=pd.read_csv(table_path)
    Anext_list = []
    Correlation=[]
    for attribute in Atrs:
        if attribute.lower()!=in_a.lower():
           Correlation.append([attribute,stats.pearsonr(table[in_a],table[attribute])[0]])
    Correlation.sort(reverse=True,key=lambda x:x[1])
    for i in range(len(Correlation)):
        Anext_list.append(Correlation[0])
    #todo Update APM based on user click feedback
    return Anext_list
def getRec(Tnext_list,Anext_list,table_path): #根据task控制属性的个数
    Option=[]
    for task in Tnext_list:
        if task == "extremeum" or task == "trend" or task == "find_value" or task == "rank" or task == "aggregation":  # 涉及1个属性
            for i in range(len(Anext_list)):
                if i<2:
                    keyword=task+" "+Anext_list[i]
                    query=genQsents(keyword,table_path)[0]
                    Option.append(parse(query,table_path))
def getRec(in_t,Tnext_list,Anext_list,table_path): #根据task控制属性的个数
    Option=[]
    nAnext_list = []
    l=len(Anext_list)
    if in_t=="extremeum" or in_t=="trend" or in_t=="find_value" or in_t=="rank" or in_t=="aggregation":  #涉及1个属性
        for task in Tnext_list:
            for i in range(len(Anext_list)):
                if i<2:
                    keyword=task+" "+Anext_list[i]
                    query=genQsents(keyword,table_path)[0]
                    Option.append(parse(query,table_path))
    elif in_t=="proportion" : #涉及2个属性
        nAnext_list.append(Anext_list[l - 1])
        nAnext_list.append(Anext_list[l - 2])
        nAnext_list.append(Anext_list[l - 3])
        for t in Tnext_list:
            for i in range(0,len(nAnext_list)-1):
                print(t+" + "+nAnext_list[i]+","+nAnext_list[i+1])
    elif in_t=="correlation" or in_t=="difference" or in_t=="distribution" : # 涉及3个属性
        nAnext_list.append(Anext_list[l - 1])
        nAnext_list.append(Anext_list[l - 2])
        nAnext_list.append(Anext_list[l - 3])
        nAnext_list.append(Anext_list[l - 4])
        for t in Tnext_list:
            for i in range(0,len(nAnext_list)-2):
                print(t+" + "+nAnext_list[i]+","+nAnext_list[i+1]+" and "+nAnext_list[i+2])

    return

#def update_TTM(in_t): #TTM矩阵更新

#def update_APM(in_a):  #APM矩阵更新



#in_t=input("task:")
#in_a=input("atr:")
Tnext_list=[]
Anext_list=[]
in_t="proportion"
in_a="mpg"
Tnext_list=getTnext(in_t)
Anext_list=getAnext(in_a)
getRec(in_t,Tnext_list,Anext_list)

#update_TTM(in_t)
#update_APM(in_a)

