from parse_query import Parse
from itertools import combinations
import pandas as pd
from vis.Correlation import find_correlation_render
import scipy.stats as stats
from builtins import list

def correlation_answer(query,table_path):
  #Answer questions about correlation
  option={}
  table=pd.read_csv(table_path)
  Parse_instance = Parse(data_url=table_path)
  respon = Parse_instance.analyze_query(query)
  taskMap = respon.get('taskMap')
  attributes=taskMap.get('correlation')[0].get('attributes')
  Data=[]
  attributes_data=[]
  for attribute in attributes:
    attr=[]
    attr.append(attribute)
    attr=attr+list(table[attribute])
    attributes_data.append(attr)
    Data.append(list(table[attribute]))
  attributes_data=list(combinations(attributes_data,2))
  pearsonr=[]
  for i in attributes_data:
    object=[]
    object.append(i[0][0])
    object.append(i[1][0])
    pearsonr.append([object,stats.pearsonr(i[0][1:], i[1][1:])[0]])
  min_index=0
  max_index=0
  min,max=1,0
  for i in range(len(pearsonr)):
    if pearsonr[i][1]>max:
      max=pearsonr[i][1]
      max_index=i
    elif pearsonr[i][1]<min:
      min=pearsonr[i][1]
      min_index=i
  answer='the most relevant attribute pair : '+ pearsonr[max_index][0][0] +' and '+ pearsonr[max_index][0][1]+'\n'+'the least relevant attribute pair : '+pearsonr[min_index][0][0]+' and '+pearsonr[min_index][0][1]
  option=find_correlation_render(attributes,Data, pearsonr,query,table_path,answer)
  return {"option":option,"attributes":attributes,"task":"correlation"}