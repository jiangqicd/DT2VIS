from parse_query import Parse
import pandas as pd
import utils
import numpy as np
from vis.Trend import TREND_render
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from builtins import list

def trend_answer(query,table_path):
  #Answer questions about trend
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