from parse_query import Parse
import pandas as pd
import utils
from vis.Extremum import find_extremum_render
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from builtins import list

def find_extremum_answer(query,table_path):
  #Answer questions about find_extremum
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