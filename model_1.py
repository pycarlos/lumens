import pandas as pd
import gurobipy as grb
import matplotlib.pyplot as plt


def model_5m(model_ready_data, overlap):
    cost = pd.DataFrame(model_ready_data['cost'])

    test = []
    length = len(cost.index)
    for i in range(length):
        test.append('x_{}'.format(i))
    cost['time'] = test

    r = grb.Model("Integer Model")

    obj = pd.Series(cost.cost.values, index=cost.time).to_dict()

    x = {}
    for i in obj:
        x[i] = r.addVar(vtype=grb.GRB.BINARY, obj=obj[i])

    r.modelSense = grb.GRB.MINIMIZE

    if not overlap:
        r.addConstr(sum(list(x.values())[0:287]) >= 96, name='day1')
        r.addConstr(sum(list(x.values())[288:575]) >= 96, name='day2')
        r.addConstr(sum(list(x.values())[576:863]) >= 96, name='day3')
        r.addConstr(sum(list(x.values())[864:1151]) >= 96, name='day4')
        r.addConstr(sum(list(x.values())[1152:1439]) >= 96, name='day5')
        r.addConstr(sum(list(x.values())[1440:1727]) >= 96, name='day6')
        r.addConstr(sum(list(x.values())[1728:2015]) >= 96, name='day7')
    elif overlap:
        r.addConstr(sum(list(x.values())[0:311]) >= 96, name='day1')
        r.addConstr(sum(list(x.values())[264:599]) >= 96, name='day2')
        r.addConstr(sum(list(x.values())[552:887]) >= 96, name='day3')
        r.addConstr(sum(list(x.values())[840:1175]) >= 96, name='day4')
        r.addConstr(sum(list(x.values())[1128:1463]) >= 96, name='day5')
        r.addConstr(sum(list(x.values())[1416:1751]) >= 96, name='day6')
        r.addConstr(sum(list(x.values())[1704:2015]) >= 96, name='day7')

    r.optimize()

    index = model_ready_data.index
    schedule = []
    for k, v in obj.items():
        schedule.append('{}'.format(x[k].x))
    print('----------------------------------')
    print('Schedule:')
    print(pd.Series(schedule, index=index))
    print('Total cost: ${}'.format(round(r.objVal, 2)))
    print('----------------------------------')
    print(schedule * -1)
    print(index)

    s = pd.Series(schedule, index=index)
    s.to_csv('C:\\Users\\USER\\UTS\\Carlos Capstone - Capstone\\shared_folder\\plot\\schedule.csv')

# ignore
# print('ignore')
# dict_values = x.keys()
# sum_values = list(dict_values)[0:287]
# print(sum_values)
# print(x)
# print(obj.items())
