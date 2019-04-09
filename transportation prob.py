from pulp import *

# listy wszystkich odbioróców i producentów
shops = ['S1', 'S2', 'S3', 'S4']
plants = ['P1', 'P2', 'P3']

# Zapotrzebowanie i podaż
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

# Koszty jednostkowe
costs = [
    [3, 6, 8, 4],
    [6, 1, 2, 5],
    [7, 8, 3, 9]
]

# Deklaracja problemu optymalizacji - szukanie minima
prob = LpProblem("Transportation costs", LpMinimize)

# Połączenia między dostawcami a sklepami - każdy z każdym
routes = [(plant, shop) for shop in shops for plant in plants]

# Stworzenie nazw zmiennych do optymalizacji - np. Route_P1_S4 - liczba przetransportowanych towarów w zakresie od 0 do inf, liczba całkowita
route_vars = LpVariable.dicts('Route', (plants, shops), 0, None, LpInteger)

# Deklarowanie funkcji celu do zoptymalizowania
tmp = []
for i, shop in enumerate(shops):
    for j, plant in enumerate(plants):
        tmp.append(route_vars[plant][shop] * costs[j][i])
prob += lpSum(tmp)

# Definiowanie ograniczeń ( == demand[shop] jest warunkiem do spełnienia)
for shop in shops:
    prob += lpSum(route_vars[plant][shop] for plant in plants) == demand[shop]

for plant in plants:
    prob += lpSum(route_vars[plant][shop] for shop in shops) == supply[plant]

# Odpalenie solvera
prob.solve()

# Wyświetl problem
print(prob)

# Wyświetl status
print("Status:", LpStatus[prob.status])

# Wyświetl przetransportowanie ilości dla każdego połączenia
for v in prob.variables():
    print(v.name, "=", v.varValue)

# Koszt całkowity
print("Total Cost of Transportation = ", value(prob.objective))

