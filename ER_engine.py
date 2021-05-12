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

def user_recommend(attributes,task,table_path,feedback):
    result=[]
    Feedback=feedback.split("-")

    tasks = ["find_extremum", "trend", "find_value", "correlation", "difference", "distribution", "rank", "proportion",
             "derived_value"]
    TTM = [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
           [0.12, 0.08, 0.13, 0.07, 0.14, 0.06, 0.1, 0.2, 0.2],
           [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
           [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
           [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
           [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
           [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
           [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
           [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2]]
    #根据用户点击反馈调整TTM
    if feedback!="init_feedback" and Feedback[0]=="positive_feedback":
        index_now=0
        index_next=0
        for i in range(len(tasks)):
            if Feedback[1].lower()==tasks[i].lower():
                index_now=i
            elif Feedback[2].lower()==tasks[i].lower():
                index_next=i
        TTM[index_now][index_next]+=0.2#0.2为可调节系数
        max=0
        for i in range(len(TTM[index_next])):
            if i!=index_next:
                if TTM[index_next][i]>max:
                    max=TTM[index_next][i]
        sum=0
        for i in range(len(TTM[index_next])):
            if i!=index_next:
                sum+=max/TTM[index_next][i]
        for i in range(len(TTM[index_now])):
            if i!=index_next:
                TTM[index_now][i]-=0.2*(max/TTM[index_next][i]/sum)
                # TTM[index_now][i]-=0.2*(1-TTM[index_next][i]/(1-TTM[index_next][index_next]))/3
        #如果概率矩阵纯在负数，进行标准化
        for i in TTM:
            MIN=min(i)
            if MIN<0:
                for j in range(len(i)):
                    i[j]=(i[j]-MIN)/(1-MIN)
    elif feedback!="init_feedback" and Feedback[0]=="negative_feedback":
        for i in range(2):
            index_now = 0
            index_next = 0
            for i in range(len(tasks)):
                if Feedback[1].lower() == tasks[i].lower():
                    index_now = i
                elif Feedback[i+2].lower() == tasks[i].lower():
                    index_next = i
            TTM[index_now][index_next] -= 0.2  # 0.2为可调节系数
            max = 0
            for i in range(len(TTM[index_next])):
                if i != index_next:
                    if TTM[index_next][i] > max:
                        max = TTM[index_next][i]
            sum = 0
            for i in range(len(TTM[index_next])):
                if i != index_next:
                    sum += max / TTM[index_next][i]
            for i in range(len(TTM[index_now])):
                if i != index_next:
                    TTM[index_now][i] += 0.2 * (max / TTM[index_next][i] / sum)
                    # TTM[index_now][i]-=0.2*(1-TTM[index_next][i]/(1-TTM[index_next][index_next]))/3
            # 如果概率矩阵纯在负数，进行标准化
            for i in TTM:
                MIN = min(i)
                if MIN < 0:
                    for j in range(len(i)):
                        i[j] = (i[j] - MIN) / (1 - MIN)

    Atrs = []
    APM = []

    table = pd.read_csv(table_path)
    for attribute in table.columns:
        if attribute.lower() not in utils.time and is_numeric_dtype(table[attribute]):
            Atrs.append(attribute)

    for i in range(len(Atrs)):
        APM.append(round(1 / len(Atrs), 2))

    T_index=0
    for t in range(len(tasks)):
        if tasks[t]==task:
            T_index=t

    Tnext_list=[]
    sort_array = np.argsort(TTM[T_index])
    Tnext_list.append(tasks[sort_array[len(sort_array)-1]])
    Tnext_list.append(tasks[sort_array[len(sort_array)-2]])
    Attributes=list(map(lambda x:x.lower(),attributes))
    Correlation=[]
    for attribute in Atrs:
        if attribute.lower() not in Attributes:
          Correlation.append([attribute, stats.pearsonr(list(table[attributes[0]]), list(table[attribute]))[0]])
    Correlation.sort(reverse=True, key=lambda x: x[1])
    for task in Tnext_list:
        print("----------")
        print(task)
        Anext_list = []
        if task == "find_extremum" or task == "trend" or task == "find_value" or task == "rank" or task == "derived_value" or task=="distribution":
            if len(attributes)==1:
              Anext_list.append(attributes[0])
              Anext_list.append(Correlation[0][0])
            elif len(attributes)>1:
              Anext_list.append(attributes[0])
              Anext_list.append(attributes[1])
            for i in range(len(Anext_list)):
                keyword=task+" "+Anext_list[i]
                query=genQsents(keyword,table_path)[0]
                result.append(parse(query,table_path))
        elif task=="correlation" or task=="difference" or task=="proportion" : # 涉及2个属性
            if len(attributes)==1:
                Anext_list.append(attributes[0])
                Anext_list.append(Correlation[0][0])
                Anext_list.append(Correlation[len(Correlation)-1][0])
                keyword=task+" "+Anext_list[0]+" "+Anext_list[1]
                query=genQsents(keyword,table_path)[0]
                result.append(parse(query,table_path))
                keyword1=task+" "+Anext_list[0]+" "+Anext_list[2]
                query1=genQsents(keyword1,table_path)[0]
                result.append(parse(query1,table_path))
            elif len(attributes)==2:
                Anext_list.append(attributes[0])
                Anext_list.append(attributes[1])
                Anext_list.append(Correlation[0][0])
                keyword=task+" "+Anext_list[0]+" "+Anext_list[1]
                query=genQsents(keyword,table_path)[0]
                result.append(parse(query,table_path))
                keyword1=task+" "+Anext_list[0]+" "+Anext_list[2]
                query1=genQsents(keyword1,table_path)[0]
                result.append(parse(query1,table_path))
            elif len(attributes)>2:
                Anext_list.append(attributes[0])
                Anext_list.append(attributes[1])
                Anext_list.append(attributes[2])
                keyword=task+" "+Anext_list[0]+" "+Anext_list[1]
                query=genQsents(keyword,table_path)[0]
                result.append(parse(query,table_path))
                keyword1=task+" "+Anext_list[0]+" "+Anext_list[2]
                query1=genQsents(keyword1,table_path)[0]
                result.append(parse(query1,table_path))
    return result
def user_recommend_v1(attributes,task,table_path,feedback,TTM):
    result=[]
    Feedback=feedback.split("-")
    print(Feedback)
    print(TTM)
    tasks = ["find_extremum", "trend", "find_value", "correlation", "difference", "distribution", "rank", "proportion",
             "derived_value"]
    # TTM = [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
    #        [0.12, 0.08, 0.13, 0.07, 0.14, 0.06, 0.1, 0.2, 0.2],
    #        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
    #        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
    #        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
    #        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
    #        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
    #        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
    #        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2]]
    #根据用户点击反馈调整TTM
    if feedback!="init_feedback" and Feedback[0]=="positive_feedback"and len(Feedback)==3:
        index_now=0
        index_next=0
        for i in range(len(tasks)):
            if Feedback[1].lower()==tasks[i].lower():
                index_now=i
            elif Feedback[2].lower()==tasks[i].lower():
                index_next=i
        TTM[index_now][index_next]+=0.05#0.2为可调节系数
        max=0
        for i in range(len(TTM[index_next])):
            if i!=index_next:
                if TTM[index_next][i]>max:
                    max=TTM[index_next][i]
        sum=0
        for i in range(len(TTM[index_next])):
            if i!=index_next:
                sum+=max/TTM[index_next][i]
        for i in range(len(TTM[index_now])):
            if i!=index_next:
                TTM[index_now][i]-=0.05*(max/TTM[index_next][i]/sum)
                # TTM[index_now][i]-=0.2*(1-TTM[index_next][i]/(1-TTM[index_next][index_next]))/3
        #如果概率矩阵纯在负数，进行标准化
        for i in TTM:
            MIN=min(i)
            if MIN<0:
                for j in range(len(i)):
                    i[j]=(i[j]-MIN)/(1-MIN)
    elif feedback!="init_feedback" and Feedback[0]=="negative_feedback"and len(Feedback)==4:
        for j in range(2):
            index_now = 0
            index_next = 0
            for i in range(len(tasks)):
                if Feedback[1].lower() == tasks[i].lower():
                    index_now = i
                elif Feedback[j+2].lower() == tasks[i].lower():
                    index_next = i
            TTM[index_now][index_next] -= 0.05  # 0.2为可调节系数
            max = 0
            for i in range(len(TTM[index_next])):
                if i != index_next:
                    if TTM[index_next][i] > max:
                        max = TTM[index_next][i]
            sum = 0
            for i in range(len(TTM[index_next])):
                if i != index_next:
                    sum += max / TTM[index_next][i]
            for i in range(len(TTM[index_now])):
                if i != index_next:
                    TTM[index_now][i] += 0.05 * (max / TTM[index_next][i] / sum)
                    # TTM[index_now][i]-=0.2*(1-TTM[index_next][i]/(1-TTM[index_next][index_next]))/3
            # 如果概率矩阵纯在负数，进行标准化
            for i in TTM:
                MIN = min(i)
                if MIN < 0:
                    for j in range(len(i)):
                        i[j] = (i[j] - MIN) / (1 - MIN)
    print(TTM)

    Atrs = []
    APM = []

    table = pd.read_csv(table_path)
    for attribute in table.columns:
        if attribute.lower() not in utils.time and is_numeric_dtype(table[attribute]):
            Atrs.append(attribute)

    for i in range(len(Atrs)):
        APM.append(round(1 / len(Atrs), 2))

    T_index=0
    for t in range(len(tasks)):
        if tasks[t]==task:
            T_index=t

    Tnext_list=[]
    sort_array = np.argsort(TTM[T_index])
    Tnext_list.append(tasks[sort_array[len(sort_array)-1]])
    Tnext_list.append(tasks[sort_array[len(sort_array)-2]])
    # Attributes=list(map(lambda x:x.lower(),attributes))
    Attributes=[]
    for i in attributes:
        Attributes.append(i.lower())
    Correlation=[]
    for attribute in Atrs:
        if attribute.lower() not in Attributes:
          Correlation.append([attribute, stats.pearsonr(list(table[attributes[0]]), list(table[attribute]))[0]])
    Correlation.sort(reverse=True, key=lambda x: x[1])
    for task in Tnext_list:
        print("----------")
        print(task)
        Anext_list = []
        if task == "find_extremum" or task == "trend" or task == "find_value" or task == "rank" or task == "derived_value" or task=="distribution":
            if len(attributes)==1:
              Anext_list.append(attributes[0])
              Anext_list.append(Correlation[0][0])
            elif len(attributes)>1:
              Anext_list.append(attributes[0])
              Anext_list.append(attributes[1])
            print(Anext_list)
            for i in range(len(Anext_list)):
                keyword=task+" "+Anext_list[i]
                query=genQsents(keyword,table_path)[0]
                result.append([task,query])
        elif task=="correlation" or task=="difference" or task=="proportion" : # 涉及2个属性
            if len(attributes)==1:
                Anext_list.append(attributes[0])
                Anext_list.append(Correlation[0][0])
                Anext_list.append(Correlation[len(Correlation)-1][0])
                keyword=task+" "+Anext_list[0]+" "+Anext_list[1]
                query=genQsents(keyword,table_path)[0]
                result.append([task,query])
                keyword1=task+" "+Anext_list[0]+" "+Anext_list[2]
                query1=genQsents(keyword1,table_path)[0]
                result.append([task,query1])
            elif len(attributes)==2:
                Anext_list.append(attributes[0])
                Anext_list.append(attributes[1])
                Anext_list.append(Correlation[0][0])
                keyword=task+" "+Anext_list[0]+" "+Anext_list[1]
                query=genQsents(keyword,table_path)[0]
                result.append([task,query])
                keyword1=task+" "+Anext_list[0]+" "+Anext_list[2]
                query1=genQsents(keyword1,table_path)[0]
                result.append([task,query1])
            elif len(attributes)>2:
                Anext_list.append(attributes[0])
                Anext_list.append(attributes[1])
                Anext_list.append(attributes[2])
                keyword=task+" "+Anext_list[0]+" "+Anext_list[1]
                query=genQsents(keyword,table_path)[0]
                result.append([task,query])
                keyword1=task+" "+Anext_list[0]+" "+Anext_list[2]
                query1=genQsents(keyword1,table_path)[0]
                result.append([task,query1])
    return result,TTM



