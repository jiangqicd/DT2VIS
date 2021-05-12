from parse_query import Parse
import re
from itertools import combinations
import json
import pandas as pd
import utils
import numpy as np
from vis.Extremum import find_extremum_render
from vis.Distribution import find_distribution_render
from vis.Trend import TREND_render
from vis.Rank import find_rank_render
from vis.Aggregation import find_aggregation_render
from vis.Find_value import find_value_render
from vis.Correlation import find_correlation_render
from vis.Difference import find_difference_render
from vis.Proportion import find_proportion_render
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import scipy.stats as stats
from builtins import list
import math
# table_path_find_extremum='../table/cars-w-year.csv'
table_path_test='economic.csv'
table_path_test1='cars-w-year.csv'
# table_path_find_value="../table/data_1.csv"

def function(query,table_path):
  parse_instance = Parse(data_url=table_path)
  respon = parse_instance.analyze_query(query)
  print(respon.get('taskMap'),'\n',respon.get('attributeMap'))

def parse(query,table_path):
  parse_instance = Parse(data_url=table_path)
  respon = parse_instance.analyze_query(query)
  taskMap=respon.get('taskMap')
  option={}
  if "proportion" in taskMap.keys():
    option=proportion_vis(query,table_path)
  elif "distribution" in taskMap.keys():
    option=distribution_vis(query,table_path)
  elif "derived_value" in taskMap.keys():
    option=derived_value_vis(query,table_path)
  elif "difference" in taskMap.keys():
    option=difference_vis(query,table_path)
  elif "rank" in taskMap.keys():
    option=rank_vis(query,table_path)
  elif "trend" in taskMap.keys():
    option=trend_vis(query,table_path)
  elif "correlation" in taskMap.keys():
    option=correlation_vis(query,table_path)
  elif "find_value" in taskMap.keys():
    option=find_value_vis(query,table_path)
  elif "find_extremum" in taskMap.keys():
    option=find_extremum_vis(query,table_path)
  return option


def proportion_vis(query,table_path):
  #Visualization of answering questions about proportion
  option={}
  table=pd.read_csv(table_path)
  Parse_instance = Parse(data_url=table_path)
  respon = Parse_instance.analyze_query(query)
  taskMap = respon.get('taskMap')
  proportion_attribute = taskMap.get('proportion')[0].get('attributes')[0]
  proportion_main_attribute=""
  if len(taskMap) >= 2:
    x_label = ""
    Filter = taskMap.get('filter')
    p_filter = []
    F = ""
    for filter in Filter:
      flag = "true"
      for column in table.columns:
        if filter.get('values') == column.lower():
          p_filter.append(filter)
          flag = "flase"
      filter_Phrase = filter.get("queryPhrase")
      filter_opertaor = filter.get("operator")
      values = filter.get("values")
      filter_attributes = filter.get("attributes")[0]
      if filter_opertaor == "EQ" and is_string_dtype(table[filter_attributes]) and flag == "true":
        table[filter_attributes] = table[filter_attributes].str.lower()
        table = table[table[filter_attributes].str.contains(values.lower())]
        F = F + filter_Phrase + " " + values + " " + filter_attributes
      elif filter_opertaor == "EQ" and is_numeric_dtype(table[filter_attributes]) and flag == "true":
        table[filter_attributes] = table[filter_attributes].astype(int)
        table = table[table[filter_attributes] == int(values)]
        F = F + filter_Phrase + " " + values + " " + filter_attributes
        x_label = filter_attributes
      elif filter_opertaor == "LT" and is_numeric_dtype(table[filter_attributes]) and flag == "true":
        table[filter_attributes] = table[filter_attributes].astype(int)
        table = table[table[filter_attributes] <= int(values)]
        F = F + filter_Phrase + " " + values + " " + filter_attributes
        x_label = filter_attributes
      elif filter_opertaor == "GT" and is_numeric_dtype(
              table[filter_attributes]) and filter_Phrase != "over" and flag == "true":
        table[filter_attributes] = table[filter_attributes].astype(int)
        table = table[table[filter_attributes] >= int(values)]
        F = F + filter_Phrase + " " + values + " " + filter_attributes
        x_label = filter_attributes
      elif filter_Phrase == "over" and flag == "true":
        x_label = filter_attributes
      elif filter_attributes == "RANGE" and is_numeric_dtype(table[filter_attributes]) and flag == "true":
        table[filter_attributes] = table[filter_attributes].astype(int)
        table = table[
          (table[filter_attributes] <= int(values[0])) & (table[filter_attributes] >= int(values[1]))]
        F = F + filter_Phrase + " " + values[0] + " and " + values[1] + " " + filter_attributes
        x_label = filter_attributes
    proportion_main_attribute=p_filter[0].get('attributes')[0]
    x = []
    y = list(table[proportion_attribute])
    z = list(table[p_filter[0].get('attributes')[0]])
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
    proportion=[]
    for i in range(len(y)):
      proportion.append(round(y[i]/z[i],2))
    answer=""
    if len(proportion)==1:
      answer+="The proportion of "+proportion_attribute+" in "+p_filter[0].get('attributes')[0]+" "+F+" is "+str(proportion[0])
    elif len(proportion)>1:
      Max=max(proportion)
      Min=min(proportion)
      trend=""
      if (proportion[len(proportion)-1]-proportion[0])>=0:
        trend+="increased"
      else:
        trend+="decreased"
      answer+="In the proportion of "+proportion_attribute+" in "+p_filter[0].get('attributes')[0]+" "+F+", MAx is "+str(Max)+",  Min is "+str(Min)
    option = find_proportion_render(x, y, z, proportion_attribute, p_filter[0].get('attributes')[0], query, table_path,answer)
      # Todo Add visualation (distribution)
  elif len(filter)==1:
    proportion_main_attribute=taskMap.get('filter')[0].get('attributes')[0]
    x=[]
    y = list(table[proportion_attribute])
    z = list(table[proportion_main_attribute])
    Label = []
    x_label = ""
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
    proportion = []
    for i in range(len(y)):
      proportion.append(round(y[i] / z[i]), 2)
    answer = ""
    Max = max(proportion)
    Min = min(proportion)
    trend = ""
    if (proportion(len(proportion) - 1) - proportion[0]) >= 0:
      trend += "increased"
    else:
      trend += "decreased"
    answer += "In the proportion of " + proportion_attribute + " in " + proportion_main_attribute +"\n" + "the Max is " + str(Max) + ", the Min is " + str(Min) + "\n"+" the overall trend is " + trend
    option = find_proportion_render(x, y, z, proportion_attribute, proportion_main_attribute, query, table_path,answer)
  return {"option":option,"attributes":[proportion_attribute,proportion_main_attribute],"task":"proportion"}

def distribution_vis(query,table_path):
  #Visualization of answering questions about distribution
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
      # Todo Add visualation (distribution)
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
    # Todo Add visualation (distribution)
  return {"option":option,"attributes":y_label,"task":"distribution"}

def derived_value_vis(query,table_path):
  #Visualization of answering questions about derived_value
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
      # Todo Add visualation (avg)
    elif derived_operator == 'SUM':
      flag = "sum"
      answer+="The sum of "+y_label+" is "+str(round(sum(y),2))+" "+F+"\n"+"and in "+y_label+", "+"the Max is "+str(max(y))+', '+"the Min is "+str(min(y))
      option = find_aggregation_render(x, y, flag, query, table_path,answer,y_label)
         # Todo Add visualation (sum)
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
      # Todo Add visualation (avg)
    elif derived_operator == 'SUM':
      flag = "sum"
      answer += "The mean of " + y_label + " is " + str(round(sum(y) / len(y), 2))+"\n"+"and in "+y_label+", "+"the Max is "+str(max(y))+', '+"the Min is "+str(min(y))
      option=find_aggregation_render(x, y, flag, query, table_path,answer,y_label)
      # Todo Add visualation (sum)
  return {"option":option,"attributes":[y_label],"task":"derived_value"}

def difference_vis(query,table_path):
  #Visualization of answering questions about difference
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


def rank_vis(query,table_path):
  #Visualization of answering questions about rank
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
       # Todo Add visualation (rank)
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
    # Todo Add visualation (rank)

def trend_vis(query,table_path):
  #Visualization of answering questions about trend
  option={}
  table=pd.read_csv(table_path)
  Parse_instance = Parse(data_url=table_path)
  respon = Parse_instance.analyze_query(query)
  taskMap = respon.get('taskMap')
  y_label = taskMap.get('trend')[0].get('attributes')[0]
  if len(taskMap) >= 2:
      x_label = ""
      F = ""
      Filter = taskMap.get('filter')
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
      y_up = []
      y_down = []
      up_count = 0
      down_count = 0
      for i in range(len(y)):
          if i == 0:
              y_up.append('-')
              y_down.append('-')
          else:
              if (y[i] - y[i - 1]) > 0:
                  y_up.append(round(y[i] - y[i - 1],2))
                  y_down.append('-')
                  up_count += 1
              else:
                  y_up.append('-')
                  y_down.append(round(y[i - 1] - y[i],2))
                  down_count += 1
      flag = ''
      if (y[len(y) - 1] - y[0]) >= 0:
          flag = "increase"
      else:
          flag = "decrease"
      Y_up = []
      Y_down = []
      for i in y_up:
          if i == '-':
              Y_up.append(0)
          else:
              Y_up.append(i)
      for i in y_down:
          if i == '-':
              Y_down.append(0)
          else:
              Y_down.append(i)
      max_index = np.argmax(Y_up, axis=0)
      min_index = np.argmax(Y_down, axis=0)
      z = []
      for i in range(len(y)):
          z.append(int(y[i] / 20))
      answer = ' the count of ' + y_label + " increase is " + str(up_count) + ', ' + ' the count of ' + y_label + " decrease is " + str(down_count) + "\n" + "the overall trend of " + y_label + " is " + flag+" "+F
      option=TREND_render(x, y, z, y_up, y_down, max_index, min_index, x_label, y_label, query,answer)
  elif len(taskMap)==1:
      # only query 1 attribute trend without a label_attribute
      # e.g."What is the trend of GDP?"
      # the trend attribute queried : GDP
      # label_attribute : None
      trend_attribute = taskMap.get('trend')[0].get('attributes')[0]
      y=list(table[trend_attribute])
      x=[]
      x_label=""
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
      y_up = []
      y_down = []
      up_count = 0
      down_count = 0
      for i in range(len(y)):
        if i == 0:
          y_up.append('-')
          y_down.append('-')
        else:
          if (y[i] - y[i - 1]) > 0:
            y_up.append(round(y[i] - y[i - 1],2))
            y_down.append('-')
            up_count += 1
          else:
            y_up.append('-')
            y_down.append(round(y[i - 1] - y[i],2))
            down_count += 1
      flag=''
      if (y[len(y) - 1] - y[0]) >= 0:
        flag = "increase"
      else:
        flag = "decrease"
      Y_up = []
      Y_down = []
      for i in y_up:
        if i == '-':
          Y_up.append(0)
        else:
          Y_up.append(i)
      for i in y_down:
        if i == '-':
          Y_down.append(0)
        else:
          Y_down.append(i)
      max_index = np.argmax(Y_up, axis=0)
      min_index = np.argmax(Y_down, axis=0)
      z = []
      for i in range(len(y)):
        z.append(int(y[i] / 20))
      answer = ' the count of ' + trend_attribute + " increase is " + str(up_count) + ', ' + ' the count of ' +trend_attribute + " decrease is " + str(
        down_count) + "\n"+"\n" + "     the overall trend of " + trend_attribute + " is " + flag
      option=TREND_render(x, y, z, y_up, y_down, max_index, min_index, x_label, trend_attribute, query, answer)
  return {"option":option,"attributes":[y_label],"task":"trend"}

def correlation_vis(query,table_path):
  #Visualization of answering questions about correlation
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
  # Todo Add visualation (find correlation, e.g. "what is relation among GDP, Service, Architecture and Industry ?" )

def find_value_vis(query,table_path):
  #Visualization of answering questions about find_value
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

def find_extremum_vis(query,table_path):
  #Visualization of answering questions about find_extremum
  option={}
  table=pd.read_csv(table_path)
  Parse_instance = Parse(data_url=table_path)
  respon = Parse_instance.analyze_query(query)
  taskMap=respon.get('taskMap')
  attributes=taskMap.get('find_extremum')[0].get('attributes')
  operator=taskMap.get('find_extremum')[0].get('operator')
  queryPhrase=taskMap.get('find_extremum')[0].get('queryPhrase')
  attributeMap=respon.get('attributeMap')
  Attributes=list(attributeMap.keys())
  if len(attributes)==2:
    # in query “Which year has the largest gdp?”
    # y=gdp
    # x=year
    if len(taskMap)==1:
      y_label=attributes[0]
      x_label=attributes[1]
      y=list(table[attributes[0]])
      x=list(table[attributes[1]])
      min_index=y.index(min(y))
      max_index=y.index(max(y))
      answer=""
      if operator=="MAX":
        answer += str(x[max_index]) + " has the " + queryPhrase + " " + y_label.lower() + ": " + str(max(y))
      else:
        answer += str(x[min_index]) + " has the " + queryPhrase + " " + y_label.lower() + ": " + str(min(y))
      option=find_extremum_render(x,y,x_label,y_label,query,operator,answer)
    else:
        x_label = ""
        F = ""
        Filter = taskMap.get('filter')
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
        y = list(table[attributes[0]])
        if len(x_label) == 0:
            Label = []
            for attribute in table.columns:
                if attribute.lower() in utils.time:
                    Label.append(attribute)
            for attribute in table.columns:
                if attribute.lower() not in utils.time and is_string_dtype(table[attribute]):
                    Label.append(attribute)
            if len(Label) != 0:
                x_label = Label[0]
                x = list(table[x_label])
            else:
                x_label = "Serial"
                for i in range(len(y)):
                    x.append(i + 1)
        else:
          x=list(table[x_label])
        min_index = y.index(min(y))
        max_index = y.index(max(y))
        answer=""
        if operator == "MAX":
          answer += str(x[max_index]) + " has the " + queryPhrase + " " + attributes[0].lower()+" "+ F+ ": " + str(max(y))
        else:
          answer += str(x[min_index]) + " has the " + queryPhrase + " " + attributes[0].lower()+" "+F + ": " + str(min(y))
        option = find_extremum_render(x, y, x_label, attributes[0], query, operator,answer)
  elif len(attributes)==1:
    #have 2 explicit attributes
    if len(taskMap) >= 2:
        x_label = ""
        F = ""
        Filter = taskMap.get('filter')
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
        y = list(table[attributes[0]])
        if len(x_label) == 0:
            Label = []
            for attribute in table.columns:
                if attribute.lower() in utils.time:
                    Label.append(attribute)
            for attribute in table.columns:
                if attribute.lower() not in utils.time and is_string_dtype(table[attribute]):
                    Label.append(attribute)
            if len(Label) != 0:
                x_label = Label[0]
                x = list(table[x_label])
            else:
                x_label = "Serial"
                for i in range(len(y)):
                    x.append(i + 1)
        else:
          x=list(table[x_label])
        answer = ""
        if operator == "MAX":
          answer += "The " + queryPhrase + " " + attributes[0].lower() + " " + F + " is " + str(max(y))
        else:
          answer += "The " + queryPhrase + " " + attributes[0].lower() + " " + F + " is " + str(min(y))
        option=find_extremum_render(x, y,x_label, attributes[0], query, operator,answer)
    else:
        Label = []
        x_label=""
        x=[]
        y=list(table[attributes[0]])
        for attribute in table.columns:
            if attribute.lower() in utils.time:
                Label.append(attribute)
        for attribute in table.columns:
            if attribute.lower() not in utils.time and is_string_dtype(table[attribute]):
                Label.append(attribute)
        if len(Label) != 0:
            x_label = Label[0]
            x = list(table[x_label])
        else:
            x_label = "Serial"
            for i in range(len(y)):
                x.append(i + 1)
        answer = ""
        if operator == "MAX":
          answer += "The " + queryPhrase + " " + attributes[0].lower() + " is " + str(max(y))
        else:
          answer += "The " + queryPhrase + " " + attributes[0].lower() + " is " + str(min(y))
        option=find_extremum_render(x, y,x_label, attributes[0], query, operator,answer)

  return {"option":option,"attributes":[attributes[0]],"task":"find_extremum"}

if __name__ == '__main__':
  query_find_extremum="Which year has the largest gdp in US?"
  query_trend="What is the trend of GDP over the years in US?"
  query_find_value="what is the value of GDP in 2019 in US?"
  query_find_correlation="what is relation among GDP, Service, Architecture and Industry ?"
  query_find_difference="what is the difference among GDP, Service and Architecture after 2015?"
  query_find_distribution = "what is the distribution of GDP, Service and Architecture over the years in US?"
  query_find_rank = "what is the order of GDP after 2015 in US?"
  query_find_proportion = "what is the proportion of Service in GDP after 2015?"
  query_find_aggregation="what is the average of GDP between 2015 and 2019?"
  query_find_extremum1="Which year has the largest gdp?"
  query_trend1="What is the trend of GDP over the years?"
  query_find_value1="what is the value of GDP in 2019?"
  query_find_correlation1="what is relation among GDP, Service, Architecture and Industry ?"
  query_find_difference1="what is the difference among GDP, Service and Architecture after 2015?"
  query_find_distribution1 = "what is the distribution of GDP, Service and Architecture over the years?"
  query_find_rank1 = "what is the order of GDP after 2015?"
  query_find_proportion1 = "what is the proportion of Service in GDP after 2015?"
  query_find_aggregation1="what is the average of GDP between 2015 and 2019?"
  Query=[query_find_proportion,query_find_distribution,query_find_aggregation,query_find_difference,query_find_rank,query_trend,query_find_correlation,query_find_value,query_find_extremum,
         query_find_proportion1, query_find_distribution1, query_find_aggregation1, query_find_difference1, query_find_rank1,
         query_trend1, query_find_correlation1, query_find_value1, query_find_extremum1]
  Query1=[ query_find_proportion1, query_find_distribution1, query_find_aggregation1, query_find_difference1, query_find_rank1,
         query_trend1, query_find_correlation1, query_find_value1, query_find_extremum1]
  # function("what is the biggest mpg in europe ?",table_path_test1)
  # for query in Query1:
  #   print(query)
  #   option=parse(query,table_path_test)
  #   print(option.get("attributes"))
  # a=parse("what is the distribution of cost?","case2.csv")
  # function("what is the value of GDP in US?",table_path_test)
  function("What is the distribution of Deaths by state?","COVID19_state.csv")
  # print(parse("what is the average of HappinessScore in WesternEurope ?","2015.csv"))
  # a=parse("what is the trend of food ?","case2.csv")
  # function(query_find_extremum,table_path_test)
  # print(parse(query_find_difference,table_path_test))
  # function(query_find_extremum,table_path_test)
  # correlation_vis(query_find_correlation,table_path_test)
  # proportion_vis(query_find_proportion,table_path_test)
  # difference_vis(query_find_difference,table_path_test)
  # parse(query_find_distribution,table_path_test)
  # table=pd.read_csv(table_path_test)
  # for col in table.columns:
  #   print(is_numeric_dtype(table[col]))
  # print(trend_vis(query_trend,table_path_test))