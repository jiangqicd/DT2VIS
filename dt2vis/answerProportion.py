from parse_query import Parse
import pandas as pd
import utils
from vis.Proportion import find_proportion_render
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from builtins import list

def proportion_answer(query,table_path):
  #answer questions about proportion
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