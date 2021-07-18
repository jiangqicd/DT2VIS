import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
def genQsents(Query,table_path):
    # 读取表格内容
    table = pd.read_csv(table_path)
    qSents = []  # 生成的结果
    AtrYs = table.columns  # 表格的属性列
    mAtrYs = []  #小写的属性列
    mTime = ''  #表格中的时间属性列
    MTime = ''
    # trend
    time = ['year', 'time', 'date', 'day', 'week', 'month']

    for i in AtrYs:
        j = i.lower()
        mAtrYs.append(j)
    for t in AtrYs:
        if (t.lower() in time):
            mTime = t.lower()
            MTime = t

    objs = []  # 表列为字符串的列属性
    for attribute in AtrYs:
        if is_string_dtype(table[attribute]):
            objs.append(attribute)

    label_objs=[]# 小写 表列为字符串的列属性
    for i in objs:
        label_objs.append(i.lower())

    m_objs=[] # 表列为数字的列属性
    for attribute in AtrYs:
        if is_numeric_dtype(table[attribute]) and attribute.lower() not in time:
            m_objs.append(attribute)

    main_objs=[]# 小写 表列为数字的列属性
    for i in m_objs:
        main_objs.append(i.lower())

    # 识别主语/Label属性列

    # 有效的filter关键词
    filter_keyword_map={
        "in": [("filter", "EQ")],
        "at": [("filter", "EQ")],
        "on": [("filter", "EQ")],
        "about": [("filter", "EQ")],
        "after": [("filter", "GT")],
        "before": [("filter", "LT")],
        "more": [("filter", "GT")],
        "high": [("filter", "GT")],
        "over": [("filter", "GT")],
        "higher": [("filter", "GT")],
        "greater": [("filter", "GT")],
        "larger": [("filter", "GT")],
        "bigger": [("filter", "GT")],
        "under": [("filter", "LT")],
        "less": [("filter", "LT")],
        "lower": [("filter", "LT")],
        "lesser": [("filter", "LT")],
        "smaller": [("filter", "LT")],
        "between": [("filter", "RANGE")],
        "equal": [("filter", "EQ")],
    }
    # 有效的type关键词
    task_keyword_map = {
        "max": [("find_extremum", "MAX")],
        "maximum": [("find_extremum", "MAX")],
        "highest": [("find_extremum", "MAX")],
        "greatest": [("find_extremum", "MAX")],
        "largest": [("find_extremum", "MAX")],
        "biggest": [("find_extremum", "MAX")],
        "most": [("find_extremum", "MAX")],
        "min": [("find_extremum", "MIN")],
        "minimum": [("find_extremum", "MIN")],
        "smallest": [("find_extremum", "MIN")],
        "lowest": [("find_extremum", "MIN")],
        "least": [("find_extremum", "MIN")],  # Todo: dep parser can't detect
        "heaviest": [("find_extremum", "MAX")],
        "lightest": [("find_extremum", "MIN")],
        "best": [("find_extremum", "MAX")],
        "worst": [("find_extremum", "MIN")],
        "value": [("find_value", "find_value")],
        "order": [("rank", "rank")],
        "rank": [("rank", "rank")],
        "ranking": [("rank", "rank")],
        "average": [("derived_value", "AVG")],
        "mean": [("derived_value", "AVG")],
        "sum": [("derived_value", "SUM")],
        "total": [("derived_value", "SUM")],
        "distribution": [("distribution", None)],
        "range": [("distribution", None)],
        "extent": [("distribution", None)],
        "proportion": [("proportion", "proportion")],
        "correlation": [("correlation", None)],
        "correlate": [("correlation", None)],
        "relation": [("correlation", None)],
        "relationship": [("correlation", None)],
        "relate": [("correlation", None)],
        "trend": [("trend", "trend")],
        "difference": [("difference", "difference")]

        # ToDo:- Detect Negations using dependency parsing and/or algorithms !

    }
    tasks = ["find_extremum", "trend", "find_value", "correlation", "difference", "distribution", "rank", "proportion",
             "derived_value"]
    x = Query.split(" ")  # 输入的关键词


    type = []  # 查询的类型
    AtrX = []  # 辅助？属性
    AtrY = []  # 查询的属性
    atr_filter = []  # 过滤器
    atr_filter_value = []  # 过滤器

    # 判断输入
    for kw in x:
        # if kw.lower() in list(task_keyword_map.keys()):
        #     type.append([kw.lower(),task_keyword_map[kw.lower()]])
        if kw.lower() in tasks:
            type.append(kw.lower())
        elif kw.lower() in main_objs:
            AtrY.append(kw)  #不一定是首字母大小写的区别, MPG & Mpg
        # elif kw.lower() in labal_objs:
        #     AtrX.append(kw.capitalize())
        elif kw.lower() in list(filter_keyword_map):
            atr_filter.append([kw.lower(),filter_keyword_map[kw.lower()]])

    if len(MTime) != 0:
        for kw in x:
            for i in table[MTime]:
                if kw == str(i):
                    atr_filter_value.append(kw)


    # 判断filter
    e_filter = []  # at 1980
    gl_filter = []  # after 1980
    if len(atr_filter) != 0 and len(atr_filter_value) != 0:  # 用户有输入filter
        e_filter.append(" " + atr_filter[0][0] + " " + atr_filter_value[0])
        gl_filter.append(" " + atr_filter[0][0] + " " + atr_filter_value[0])
    else:  # 用户没有或没有输入完整的filter
        if len(MTime) != 0:  # 只有有time属性时才进行补全和推荐
            if len(atr_filter) != 0:
                for i in table[MTime]:
                    e_filter.append(" " + atr_filter[0][0] + " " + str(i))
                    gl_filter.append(" " + atr_filter[0][0] + " " + str(i))
            elif len(atr_filter_value) != 0:
                for i in filter_keyword_map:
                    if filter_keyword_map[i][0][1]=="EQ":
                        e_filter.append(" " + i + " " + atr_filter_value[0])
                    elif filter_keyword_map[i][0][1]=="GT" or filter_keyword_map[i][0][1]=="LT":
                        gl_filter.append(" " + i + " " + atr_filter_value[0])
            else:
                for i in filter_keyword_map:
                    if filter_keyword_map[i][0][1]=="EQ":
                        for j in table[MTime]:
                            e_filter.append(" " + i + " " + str(j))
                    elif filter_keyword_map[i][0][1] == "GT" or filter_keyword_map[i][0][1]=="LT":
                        for j in table[MTime]:
                            gl_filter.append(" " + i + " " + str(j))
        else:
            for i in table.columns:
                if is_string_dtype(table[i]):
                    e_filter.append(list(table[i])[0])
    type=type[0]
    if len(type) != 0:
        if type == "find_extremum":
                qSents.append("What is the  biggest " + AtrY[0] + "?")
                if len(mTime) != 0:
                    qSents.append("Which " + mTime + " has the biggest " + AtrY[0]  + "?")

        elif type == "trend":
                if len(mTime)!=0:
                  qSents.append("What's the trend of " + AtrY[0] + " over the " + mTime + "?")
                qSents.append("What's the trend of " + AtrY[0]  + "?")

        elif type == "find_value":  # filter是必须的
            for f in e_filter:
                qSents.append("What's the value of " + AtrY[0] + f + "?")

        elif type == "correlation":
            if len(AtrY) >= 3:
                qs1 = "What is relation among "
                for i in range(len(AtrY) - 2):
                    qs1 += AtrY[i] + ","
                qSents.append(qs1+AtrY[len(AtrY) - 2] + " and " + AtrY[len(AtrY) - 1]  + "?")
            elif len(AtrY) == 2:
                qSents.append("What's the relation between " + AtrY[0] + " and " + AtrY[1] + "?")
                for i in m_objs:
                    if i.lower() != AtrY[0].lower() and i.lower() != AtrY[1].lower():
                            qSents.append("What's the relation among " + AtrY[0] + ", "+AtrY[1] + " and " + i  + "?")
            elif len(AtrY) == 1:
                for i in range(len(m_objs)):
                    if m_objs[i].lower() != AtrY[0].lower():
                        qSents.append("What's the relation between " + AtrY[0] + " and " + m_objs[i] + "?")
                # for i in range(len(m_objs)-1):
                #     j = i+1
                #     while j in range(len(m_objs)-1):
                #         if m_objs[i].lower() != m_objs[j].lower() and m_objs[i].lower() != AtrY[0].lower() and m_objs[j].lower() != AtrY[0].lower():
                #             for f in gl_filter:
                #                 qSents.append("What's the relation among " + AtrY[0] + ", "+m_objs[i] + " and " + m_objs[j] + f + "?")
                #         j = j+1

        elif type == "difference":
            if len(AtrY) >= 3:
                qs1 = "What is difference among "
                for i in range(len(AtrY) - 2):
                    qs1 += AtrY[i] + ","
                qSents.append(qs1+AtrY[len(AtrY) - 2] + " and " + AtrY[len(AtrY) - 1]  + "?")
            elif len(AtrY) == 2:
                qSents.append("What's the difference between " + AtrY[0] + " and " + AtrY[1] + "?")
                for i in m_objs:
                    if i.lower()!=AtrY[0].lower() and i.lower()!=AtrY[1].lower():
                            qSents.append("What's the difference among " + AtrY[0] + ", "+AtrY[1] + " and " +i + "?")
            elif len(AtrY) == 1:
                # for i in range(len(m_objs) - 1):
                #     j = i + 1
                #     while j in range(len(m_objs) - 1):
                #         if m_objs[i].lower() != m_objs[j].lower() and m_objs[i].lower() != AtrY[0].lower() and m_objs[j].lower() != AtrY[0].lower():
                #                 qSents.append("What's the difference among " + AtrY[0] + ", " + m_objs[i] + " and " + m_objs[j] + "?")
                #         j = j + 1
                for i in range(len(m_objs)):
                    if m_objs[i].lower()!=AtrY[0].lower():
                        qSents.append("What's the difference between " + AtrY[0]  + " and " + m_objs[i] + "?")

        elif type == "distribution":
            qSents.append("What's the distribution of " + AtrY[0] +"?")


        elif type == "rank":
            qSents.append("What's the rank of " + AtrY[0] + "?")


        elif type == "proportion":
            if len(AtrY)==2:
              for i in table.columns:
                if i.lower()==AtrY[0].lower():
                    for j in table.columns:
                        if j.lower()==AtrY[1].lower():
                            if list(table[i])[0]/list(table[j])[0]>=1:
                               qSents.append("What's the proportion of " + AtrY[1] +" in "+AtrY[0]+ "?")
                            else:
                               qSents.append("What's the proportion of " + AtrY[0] +" in "+AtrY[1] + "?")

        elif type == "derived_value":
            qSents.append("What's the mean of " + AtrY[0] + "?")

    return qSents








