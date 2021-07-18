from parse_query import Parse
import pandas as pd
import utils
import numpy as np
from vis.Rank import find_rank_render
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from builtins import list

def rank_answer(query,table_path):
  #Answer questions about rank
  option={}
  table=pd.read_csv(table_path)
  Parse_instance = Parse(data_url=table_path)
  respon = Parse_instance.analyze_query(query)
  taskMap = respon.get('taskMap')
  y_label = taskMap.get('rank')[0].get('attributes')[0]
  if len(taskMap) >= 2:
      x_label = ""
      Filter = taskMap.get('filter')
      F = ""
      for filter in Filter:
          filter_Phrase = filter.get("queryPhrase")
          filter_opertaor = filter.get("operator")
          values = filter.get("values")
          filter_attributes = filter.get("attributes")[0]
          if filter_opertaor == "EQ" and is_string_dtype(table[filter_attributes]):
              table[filter_attributes] = table[filter_attributes].str.lower()
              table = table[table[filter_attributes].str.contains(values.lower())]
              F = F + filter_Phrase + " " + values + " " + filter_attributes
          elif filter_opertaor == "EQ" and is_numeric_dtype(table[filter_attributes]):
              table[filter_attributes] = table[filter_attributes].astype(int)
              table = table[table[filter_attributes] == int(values)]
              F = F + filter_Phrase + " " + values + " " + filter_attributes
              x_label = filter_attributes
          elif filter_opertaor == "LT" and is_numeric_dtype(table[filter_attributes]):
              table[filter_attributes] = table[filter_attributes].astype(int)
              table = table[table[filter_attributes] <= int(values)]
              F = F + filter_Phrase + " " + values + " " + filter_attributes
              x_label = filter_attributes
          elif filter_opertaor == "GT" and is_numeric_dtype(table[filter_attributes]) and filter_Phrase != "over":
              table[filter_attributes] = table[filter_attributes].astype(int)
              table = table[table[filter_attributes] >= int(values)]
              F = F + filter_Phrase + " " + values + " " + filter_attributes
              x_label = filter_attributes
          elif filter_Phrase != "over":
            x_label = filter_attributes
          elif filter_attributes == "RANGE" and is_numeric_dtype(table[filter_attributes]):
              table[filter_attributes] = table[filter_attributes].astype(int)
              table = table[
                  (table[filter_attributes] <= int(values[0])) & (table[filter_attributes] >= int(values[1]))]
              F = F + filter_Phrase + " " + values[0] + " and " + values[1] + " " + filter_attributes
              x_label = filter_attributes
      x = []
      y = list(table[y_label])
      if len(x_label) == 0:
          Label = []
          for attribute in table.columns:
              if attribute.lower() in utils.time:
                  Label.append(attribute)
          for attribute in table.columns:
              if attribute.lower() not in utils.time and is_string_dtype(table[attribute]):
                  Label.append(attribute)
          if len(Label)!=0:
              x_label = Label[0]
              x = list(table[x_label])
          else:
              x_label = "Serial"
              for i in range(len(y)):
                  x.append(i + 1)
      else:
          x = list(table[x_label])
      y_rank = np.array(y)
      index = np.argsort(y_rank)
      X = []
      Y = []
      for i in range(len(index)):
         if x_label!="Serial":
           X.append(x[index[i]])
         else:
           X.append(i+1)
         Y.append(y[index[i]])
      answer=""
      answer+="In "+y_label+": "+"the max value is "+str(Y[0])+", the min value is "+str(Y[len(Y)-1])+" "+F
      option = find_rank_render(X, Y, query, table_path,answer)
  elif len(taskMap)==1:
    rank_attribute = taskMap.get('rank')[0].get('attributes')[0]
    rank_queryPhrase = taskMap.get('rank')[0].get('queryPhrase')
    y = list(table[rank_attribute])
    y_rank = np.array(y)
    index = np.argsort(y_rank)
    Y = []
    for i in range(len(index)):
      Y.append(y[index[i]])
    x_attributes=[]
    table_attributes = table.columns
    for attribute in table_attributes:
      if attribute.lower() in utils.time:
        x_attributes.append(attribute)
      elif is_string_dtype(table[attribute]) or attribute.lower() in utils.time:
        x_attributes.append(attribute)
    X=[]
    for attribute in x_attributes:
      X.append(list(table[attribute]))
    if len(X)==0:
      for i in range(len(Y)):
        X.append(i+1)
      answer = ""
      answer += "In " + y_label + ": " + "the max value is " + str(Y[0]) + ", the min value is " + str(
        Y[len(Y) - 1])
      option=find_rank_render(X, Y, query, table_path,answer)
    else:
      answer = ""
      answer += "In " + y_label + ": " + "the max value is " + str(Y[0]) + ", the min value is " + str(
        Y[len(Y) - 1])
      option=find_rank_render(X[0], Y, query, table_path,answer)
  return {"option":option,"attributes":[y_label],"task":"rank"}