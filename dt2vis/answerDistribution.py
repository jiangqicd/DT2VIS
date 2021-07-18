from parse_query import Parse
import pandas as pd
import utils
from vis.Distribution import find_distribution_render
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from builtins import list

def distribution_answer(query,table_path):
  #Answer questions about distribution
  option={}
  table = pd.read_csv(table_path)
  Parse_instance = Parse(data_url=table_path)
  respon = Parse_instance.analyze_query(query)
  taskMap = respon.get('taskMap')
  y_label = taskMap.get('distribution')[0].get('attributes')
  replace=[]
  if len(taskMap) >= 2:
    x_label = ""
    Filter = taskMap.get('filter')
    F = ""
    for filter in Filter:
      filter_Phrase = filter.get("queryPhrase")
      filter_opertaor = filter.get("operator")
      values = filter.get("values")
      filter_attributes = filter.get("attributes")[0]
      replace.append(filter_attributes)
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
      elif filter_Phrase == "over":
        x_label = filter_attributes
      elif filter_attributes == "RANGE" and is_numeric_dtype(table[filter_attributes]):
        table[filter_attributes] = table[filter_attributes].astype(int)
        table = table[
          (table[filter_attributes] <= int(values[0])) & (table[filter_attributes] >= int(values[1]))]
        F = F + filter_Phrase + " " + values[0] + " and " + values[1] + " " + filter_attributes
        x_label = filter_attributes
    x = []
    y = list(table[y_label[0]])
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
    Y = []
    answer=""
    answer+="Under the filter conditions: "+F+"\n"
    for attribute in y_label:
      if attribute!=x_label:
        data=list(table[attribute])
        Max=max(list(table[attribute]))
        Min=min(list(table[attribute]))
        trend=""
        if (data[len(data)-1]-data[0])>=0:
          trend+="increased"
        else:
          trend+="decreased"
        answer+=" In "+attribute+": "+"the max is "+str(Max)+", "+"the min is "+str(Min)
                # +", "+"the overall trend is "+trend
        Y.append([attribute, list(table[attribute])])
    option=find_distribution_render(x, Y, x_label, query, table_path,answer)
    for i in y_label:
      if i in replace:
        y_label.remove(i)
  elif len(list(taskMap.keys())) ==1:
    Y = []
    answer=""
    for attribute in y_label:
      data = list(table[attribute])
      Max = max(list(table[attribute]))
      Min = min(list(table[attribute]))
      trend = ""
      if (data[len(data) - 1] - data[0]) >= 0:
        trend += "increased"
      else:
        trend += "decreased"
      answer += " In " + attribute + ": " + "the max is " + str(Max) + ", " + "the min is " + str(Min)
                # + "\n" + "the overall trend is " + trend
      Y.append([attribute, list(table[attribute])])
    x_attributes=[]
    table_attributes = table.columns
    for attribute in table_attributes:
      if attribute.lower() in utils.time:
        x_attributes.append(attribute)
      elif is_string_dtype(table[attribute]) or attribute.lower() in utils.time:
        x_attributes.append(attribute)
    X=[]
    for attribute in x_attributes:
      X.append([attribute,list(table[attribute])])
    if len(X)==0:
      for i in range(len(Y)):
        X.append(i+1)
      option=find_distribution_render(X, Y, "Serial", query, table_path,answer)
    else:
      option=find_distribution_render(X[0][1], Y, X[0][0], query, table_path,answer)
  return {"option":option,"attributes":y_label,"task":"distribution"}