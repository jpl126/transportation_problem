from pulp import *

shops = ['S1', 'S2', 'S3', 'S4']
plants = ['P1', 'P2', 'P3']

demand = {
    'S1': 15,
    'S2': 19,
    'S3': 13,
    'S4': 18,
}

supply = {
    'P1': 20,
    'P2': 28,
    'P3': 17
}

# {'key': 'value'} - słownik, {'value1', 'value2'} - zbiór - http://thomas-cokelaer.info/tutorials/python/sets.html#id3
# nie możesz używać w zbiorze list ani tupli (wszystkiego co może mieć ileś elementów)
costs = [
    [3, 6, 8, 4],
    [6, 1, 2, 5],
    [7, 8, 3, 9]
]

# W sumie to nie musisz tutaj podawać ani nazwy (jest tylko dla Ciebie) ani LpMinimize - jest domyślne.
# Możesz zostawić żeby było czytelniej - będzie git.
# https://www.coin-or.org/PuLP/pulp.html#the-lpproblem-class
prob = LpProblem("Transportation costs", LpMinimize)

# W ich poradniku shop i plant są odwrotnie jak u Ciebie
routes = [(plant, shop) for shop in shops for plant in plants]

route_vars = LpVariable.dicts('Route', (plants, shops), 0, None, LpInteger)

# Troche pomieszałeś indexy 'i', 'j' wraz z 'w', 'b'
# łatwiej będzie rozbic to na stworzenie macierzy kosztów i zastosowanie funkcji lpSum

#1. 'w', 'b' to trzeba przeroobić  costs tak
# tmp = [route_vars[plant][shop] * costs[plant][shop] for (plant, shop) in routes]

tmp = []
for i, shop in enumerate(shops):
    for j, plant in enumerate(plants):
        tmp.append(route_vars[plant][shop] * costs[j][i])
prob += lpSum(tmp)

for shop in shops:
    prob += lpSum(route_vars[plant][shop] for plant in plants) == demand[shop]

for plant in plants:
    prob += lpSum(route_vars[plant][shop] for shop in shops) == supply[plant]

prob.solve()
print(prob)
# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("Total Cost of Transportation = ", value(prob.objective))

