from parse_query import Parse
import pandas as pd
import utils
from vis.Find_value import find_value_render
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from builtins import list

def find_value_answer(query,table_path):
  #answer questions about find_value
  option={}
  query_filter=""
  table=pd.read_csv(table_path)
  Parse_instance = Parse(data_url=table_path)
  respon = Parse_instance.analyze_query(query)
  taskMap=respon.get('taskMap')
  queryPhrase_y=taskMap.get('find_value')[0].get('queryPhrase')
  queryPhrase_x=taskMap.get('filter')[0].get('queryPhrase')
  y_label=taskMap.get('find_value')[0].get('attributes')
  x_label=""
  x=[]
  result=[]
  Data=[]
  for attribute in table.columns:
      if is_numeric_dtype(table[attribute]) and attribute.lower not in utils.time:
         Data.append([attribute,list(table[attribute])])
  F = ""
  Filter=taskMap.get('filter')
  for filter in Filter:
      x_label = ""
      filter_Phrase=filter.get("queryPhrase")
      filter_opertaor=filter.get("operator")
      values=filter.get("values")
      filter_attributes=filter.get("attributes")[0]
      if filter_opertaor=="EQ" and is_string_dtype(table[filter_attributes]):
          table[filter_attributes] = table[filter_attributes].str.lower()
          table = table[table[filter_attributes].str.contains(values.lower())]
          F=F+filter_Phrase+" "+values
      elif filter_opertaor=="EQ" and is_numeric_dtype(table[filter_attributes]):
          table[filter_attributes] = table[filter_attributes].astype(int)
          table = table[table[filter_attributes] == int(values)]
          F = F + filter_Phrase + " " + values
          x_label = filter_attributes
      elif filter_opertaor=="LT" and is_numeric_dtype(table[filter_attributes]):
          table[filter_attributes] = table[filter_attributes].astype(int)
          table = table[table[filter_attributes] <= int(values)]
          F = F + filter_Phrase + " " + values + " " + filter_attributes
          x_label=filter_attributes
      elif filter_opertaor=="GT" and is_numeric_dtype(table[filter_attributes]):
          table[filter_attributes] = table[filter_attributes].astype(int)
          table = table[table[filter_attributes] >= int(values)]
          F = F + filter_Phrase + " " + values + " " + filter_attributes
          x_label=filter_attributes
      elif filter_attributes=="RANGE" and is_numeric_dtype(table[filter_attributes]):
          table[filter_attributes] = table[filter_attributes].astype(int)
          table = table[(table[filter_attributes] <= int(values[0]))&(table[filter_attributes]>=int(values[1]))]
          F = F + filter_Phrase + " " + values[0] + " and "+ values[1]+ " "+filter_attributes
          x_label=filter_attributes
      query_filter=query_filter+" "+F
  T=list(table[y_label[0]])
  for i in y_label:
    y=list(table[i])
    result.append([i,y])
  if len(x_label)==0:
      Label=[]
      for attribute in table.columns:
          if attribute.lower() in utils.time:
              Label.append(attribute)
      for attribute in table.columns:
          if attribute.lower() not in utils.time and is_string_dtype(table[attribute]):
              Label.append(attribute)
      if len(Label)!=0:
          x_label=Label[0]
          x=list(table[x_label])
      else:
          x_label="Serial"
          for i in range(len(y)):
              x.append(i+1)
  else:
      x=list(table[x_label])
  # for attribute in table.columns :
  #     if is_numeric_dtype(table[attribute]) and attribute!=y_label and attribute.lower() not in utils.time:
  #        result.append([attribute,list(table[attribute])])
  answer=""
  if len(T)==1:
    for i in range(len(y_label)):
      answer+="The value of "+ str(y_label[i])+" "+F+" is "+str(list(table[y_label[i]])[0])+"\n"+"    "
  elif len(T)>1:
    for i in range(len(y_label)):
      answer += "In the value of " + y_label[i] + " " + F + "\n"+"\n"+"the max is " + str(max(list(table[y_label[i]])))+", the min is "+str(min(list(table[y_label[i]])))+"\n"
  option=find_value_render(query_filter,x_label,x,result,Data,query,table_path,answer)
  return {"option":option,"attributes":[y_label[0]],"task":"find_value"}
  # Todo Add visualation (find value. e.g.what is the value of GDP in 2019?)