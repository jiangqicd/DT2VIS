from parse_query import Parse
from itertools import combinations
import pandas as pd
import utils
from vis.Difference import find_difference_render
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from builtins import list

def difference_answer(query,table_path):
  #Answer questions about difference
  option={}
  table=pd.read_csv(table_path)
  Parse_instance = Parse(data_url=table_path)
  respon = Parse_instance.analyze_query(query)
  taskMap = respon.get('taskMap')
  difference_attributes=taskMap.get('difference')[0].get('attributes')
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
    y = list(table[difference_attributes[0]])
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
    DATA=[]
    X=[]
    for attribute in difference_attributes:
      DATA.append([attribute,list(table[attribute])])
    X.append(x_label)
    X.append(x)
    answer=""
    if len(DATA)==2:
      z_count=0
      f_count=0
      difference=[]
      for i in range(len(DATA[0][1])):
        difference.append(abs(DATA[0][1][i]-DATA[1][1][i]))
        if (DATA[0][1][i]-DATA[1][1][i])>=0:
          z_count+=1
        else:
          f_count+=1
      flag=""
      if z_count>=f_count:
        flag+="bigger"
      else:
        flag+="smaller"
      answer+=F+", the max difference between "+DATA[0][0]+" and "+DATA[1][0]+" is "+str(max(difference))+"\n"+"\n"+"      the min difference between " +DATA[0][0]+" and "+DATA[1][0]+" is "+str(min(difference))+"\n"+"\n"+"In the all, "+DATA[0][0]+" is "+flag+" than "+DATA[1][0]
    elif len(DATA)>2:
      C=list(combinations(DATA,2))
      MAX=0
      MIN=99999999
      MAX_pair=[]
      MIN_pair=[]
      for i in C:
        for j in range(len(i[0][1])):
          if abs(i[0][1][j]-i[1][1][j])>=MAX:
            MAX_pair = []
            MAX=abs(i[0][1][j]-i[1][1][j])
            MAX_pair.append(i[0][0])
            MAX_pair.append(i[1][0])
          elif abs(i[0][1][j]-i[1][1][j])<=MIN:
            MIN_pair=[]
            MIN=abs(i[0][1][j]-i[1][1][j])
            MIN_pair.append(i[0][0])
            MIN_pair.append(i[1][0])
      answer += F+", the max difference is between " + MAX_pair[0] + " and " + MAX_pair[1] + ",the value is " + str(
        MAX) + "\n"+"\n"+"the min difference is between " + MIN_pair[0] + " and " + MIN_pair[1] + ", the value is " + str(
        MIN)
    option = find_difference_render(DATA, X, query, table_path,answer)
  elif len(taskMap)==1:
    DATA=[]
    for attribute in difference_attributes:
      DATA.append([attribute,list(table[attribute])])
    x_attributes = []
    table_attributes = table.columns
    for attribute in table_attributes:
      if attribute.lower() in utils.time:
        x_attributes.append(attribute)
      elif is_string_dtype(table[attribute]):
        x_attributes.append(attribute)
    X = []
    for attribute in x_attributes:
      X.append([attribute,list(table[attribute])])
    answer = ""
    if len(DATA) == 2:
      z_count = 0
      f_count = 0
      difference = []
      for i in range(len(DATA[0][1])):
        difference.append(abs(DATA[0][1][i] - DATA[1][1][i]))
        if (DATA[0][1][i] - DATA[1][1][i]) >= 0:
          z_count += 1
        else:
          f_count += 1
      flag = ""
      if z_count >= f_count:
        flag += "bigger"
      else:
        flag += "smaller"
      answer +="Max difference is " + str(max(difference)) + ", min difference is " + str(
        min(difference)) + "\n"+"\n"+"      In the all, " + DATA[0][0] + " is " + flag + " than " + DATA[1][0]+"."
    elif len(DATA) > 2:
      C = list(combinations(DATA, 2))
      MAX = 0
      MIN = 99999999
      MAX_pair = []
      MIN_pair = []
      for i in C:
        for j in range(len(i[0][1])):
          if abs(i[0][1][j] - i[1][1][j]) >= MAX:
            MAX_pair = []
            MAX = abs(i[0][1][j] - i[1][1][j])
            MAX_pair.append(i[0][0])
            MAX_pair.append(i[1][0])
          elif abs(i[0][1][j] - i[1][1][j]) <= MIN:
            MIN_pair = []
            MIN = abs(i[0][1][j] - i[1][1][j])
            MIN_pair.append(i[0][0])
            MIN_pair.append(i[1][0])
      answer += "The max difference is between " + MAX_pair[0] + " and " + MAX_pair[1] + ",the value is " + str(
        MAX) + "\n"+"\n"+"  the min difference is between " + MIN_pair[0] + " and " + MIN_pair[1] + ", the value is " + str(
        MIN)
    if len(X) == 0:
      z=[]
      z.append("Serial")
      t=[]
      for i in range(len(DATA[0][1])):
        t.append(i + 1)
      z.append(t)
      X.append(z)
      option=find_difference_render(DATA,X,query,table_path,answer)
    else:
      option=find_difference_render(DATA,X[0],query,table_path,answer)
  return {"option":option,"attributes":difference_attributes,"task":"difference"}