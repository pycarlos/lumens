import pandas as pd
import gurobipy as grb


def model_2h(model_ready_data, overlap):
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
        r.addConstr(sum(list(x.values())[0:11]) >= 4, name='day1')
        r.addConstr(sum(list(x.values())[12:23]) >= 4, name='day2')
        r.addConstr(sum(list(x.values())[24:35]) >= 4, name='day3')
        r.addConstr(sum(list(x.values())[36:47]) >= 4, name='day4')
        r.addConstr(sum(list(x.values())[48:59]) >= 4, name='day5')
        r.addConstr(sum(list(x.values())[60:71]) >= 4, name='day6')
        r.addConstr(sum(list(x.values())[72:84]) >= 4, name='day7')
    elif overlap:
        r.addConstr(sum(list(x.values())[0:12]) >= 4, name='day1')
        r.addConstr(sum(list(x.values())[11:24]) >= 4, name='day2')
        r.addConstr(sum(list(x.values())[23:36]) >= 4, name='day3')
        r.addConstr(sum(list(x.values())[34:48]) >= 4, name='day4')
        r.addConstr(sum(list(x.values())[47:60]) >= 4, name='day5')
        r.addConstr(sum(list(x.values())[59:72]) >= 4, name='day6')
        r.addConstr(sum(list(x.values())[71:84]) >= 4, name='day7')

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
