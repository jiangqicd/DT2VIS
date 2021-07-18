from parse_query import Parse
import pandas as pd
import utils
from vis.Aggregation import find_aggregation_render
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from builtins import list

def derived_value_answer(query,table_path):
  #Answer questions about derived_value
  option={}
  table=pd.read_csv(table_path)
  Parse_instance = Parse(data_url=table_path)
  respon = Parse_instance.analyze_query(query)
  taskMap = respon.get('taskMap')
  y_label = taskMap.get('derived_value')[0].get('attributes')[0]
  if len(taskMap) >= 2:
    x_label = ""
    Filter = taskMap.get('filter')
    derived_operator = taskMap.get('derived_value')[0].get('operator')
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
    answer=""
    if derived_operator == 'AVG':
      flag = "mean"
      answer+="The mean of "+y_label+" is "+str(round(sum(y)/len(y),2))+" "+F
      option = find_aggregation_render(x, y, flag, query, table_path,answer,y_label)

    elif derived_operator == 'SUM':
      flag = "sum"
      answer+="The sum of "+y_label+" is "+str(round(sum(y),2))+" "+F+"\n"+"and in "+y_label+", "+"the Max is "+str(max(y))+', '+"the Min is "+str(min(y))
      option = find_aggregation_render(x, y, flag, query, table_path,answer,y_label)

  elif len(list(taskMap.keys()))==1:
    derived_value_attribute = taskMap.get('derived_value')[0].get('attributes')[0]
    derived_operator = taskMap.get('derived_value')[0].get('operator')
    derived_queryPhrase = taskMap.get('derived_value')[0].get('queryPhrase')
    y = list(table[derived_value_attribute])
    Label = []
    x=[]
    x_label=""
    answer=""
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
    if derived_operator == 'AVG':
      flag = "mean"
      answer += "The mean of " + y_label + " is " + str(round(sum(y) / len(y), 2))
      option=find_aggregation_render(x, y, flag, query, table_path,answer,y_label)

    elif derived_operator == 'SUM':
      flag = "sum"
      answer += "The mean of " + y_label + " is " + str(round(sum(y) / len(y), 2))+"\n"+"and in "+y_label+", "+"the Max is "+str(max(y))+', '+"the Min is "+str(min(y))
      option=find_aggregation_render(x, y, flag, query, table_path,answer,y_label)

  return {"option":option,"attributes":[y_label],"task":"derived_value"}