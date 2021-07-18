from parse_query import Parse
from dt2vis.answerAggregation import derived_value_answer
from dt2vis.answerCorrelation import correlation_answer
from dt2vis.answerDifference import difference_answer
from dt2vis.answerDistribution import distribution_answer
from dt2vis.answerExtremum import find_extremum_answer
from dt2vis.answerFindvalue import find_value_answer
from dt2vis.answerProportion import proportion_answer
from dt2vis.answerRank import rank_answer
from dt2vis.answerTrend import trend_answer

def parse(query,table_path):
  parse_instance = Parse(data_url=table_path)
  respon = parse_instance.analyze_query(query)
  taskMap=respon.get('taskMap')
  option={}
  if "proportion" in taskMap.keys():
    option=proportion_answer(query,table_path)
  elif "distribution" in taskMap.keys():
    option=distribution_answer(query,table_path)
  elif "derived_value" in taskMap.keys():
    option=derived_value_answer(query,table_path)
  elif "difference" in taskMap.keys():
    option=difference_answer(query,table_path)
  elif "rank" in taskMap.keys():
    option=rank_answer(query,table_path)
  elif "trend" in taskMap.keys():
    option=trend_answer(query,table_path)
  elif "correlation" in taskMap.keys():
    option=correlation_answer(query,table_path)
  elif "find_value" in taskMap.keys():
    option=find_value_answer(query,table_path)
  elif "find_extremum" in taskMap.keys():
    option=find_extremum_answer(query,table_path)
  return option
