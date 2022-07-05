import pandas as pd
import gurobipy as grb


def model_30m(model_ready_data, overlap):
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
        r.addConstr(sum(list(x.values())[0:47]) >= 16, name='day1')
        r.addConstr(sum(list(x.values())[48:95]) >= 16, name='day2')
        r.addConstr(sum(list(x.values())[96:143]) >= 16, name='day3')
        r.addConstr(sum(list(x.values())[144:191]) >= 16, name='day4')
        r.addConstr(sum(list(x.values())[192:239]) >= 16, name='day5')
        r.addConstr(sum(list(x.values())[240:287]) >= 16, name='day6')
        r.addConstr(sum(list(x.values())[288:336]) >= 16, name='day7')
    elif overlap:
        r.addConstr(sum(list(x.values())[0:51]) >= 16, name='day1')
        r.addConstr(sum(list(x.values())[44:99]) >= 16, name='day2')
        r.addConstr(sum(list(x.values())[92:147]) >= 16, name='day3')
        r.addConstr(sum(list(x.values())[140:195]) >= 16, name='day4')
        r.addConstr(sum(list(x.values())[188:244]) >= 16, name='day5')
        r.addConstr(sum(list(x.values())[236:291]) >= 16, name='day6')
        r.addConstr(sum(list(x.values())[284:336]) >= 16, name='day7')

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
