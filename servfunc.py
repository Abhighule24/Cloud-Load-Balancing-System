# Libraries for functions
import time
import pickle
import pandas as pd
import numpy as np
import scipy.stats as stats
import json

def AgentWork(c, addr, report_card):
    while True:
        ReportObj = pickle.dumps(report_card)
        c.send(ReportObj)
        time.sleep(15)
        
def sping(params):
        return str(params)

def dataset(params):
    data = pd.read_csv('datasets/iris.csv')
    df_dict = data.to_dict('list')
    return str(df_dict)

def standard_deviation(params): # parameter can be a dataset and column name output is a value
    ans = np.std(json.loads(params).get("values"))
    return str(ans)

def Euclidean_distance(params): # parameter can be a dataset and column name output is a value
    main_list = json.loads(params).get("values")
    lst_1 = np.array(main_list[0])
    lst_2 = np.array(main_list[1])
    sum_sq = np.sum(np.square(lst_1 - lst_2)) 
    result = np.sqrt(sum_sq)
    return str(result)

def cumulative_freq(params):  # need a list or a dataset as parameter  output is a list
    x = pd.Series(json.loads(params).get("values"))
    print(x.cumsum()[0])
    return str(x.cumsum())#"This function calculates Cumulative Frequency"

def anova(params): # need a set of data with multiple columns, output is the results of ANOVA or specific values like F value P value etc.
    main_list = json.loads(params).get("values")
    lst_1 = np.array(main_list[0])
    lst_2 = np.array(main_list[1])
    fvalue, pvalue = stats.f_oneway(lst_1, lst_2)
    return str(str(fvalue)+" "+str(pvalue))

#print(Euclidean_distance([[1,2,3,4,5],[4,5,6,7,8]]))
#print(dataset(0))