from pulp import *

shops = ['S1', 'S2', 'S3']
plants = ['F1', 'F2', 'F3']

demand = {
    'S1' : 110,
    'S2' : 90,
    'S3' : 150
}

supply = {
    'F1' : 120,
    'F2' : 150,
    'F3' : 80
}

costs = {
    [4, 1, 2],
    [2, 4, 3],
    [3, 6, 5]
}

prob = LpProblem("Transportation costs", LpMinimize)

routes = [(i, j) for i in shops for j in plants]

route_vars = LpVariable.dicts('Route', (shops, plants), 0, None, LpInteger)

prob += LpSum(amount_vars[i][j]) * costs[i][j] in routes

for j in plants:
    prob += LpSum(amount_vars[i][j] for i in shops) <= demand

for i in shops:
    prob += LpSum(amount_vars[i][j] for i in plants) >= supply

prob.solve()




