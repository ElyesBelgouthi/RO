import gurobipy as gp
from gurobipy import GRB


def optimal_electricity_supply(centrales, villes, offres, demandes, couts_transport, penalites):
    # Create model

    model = gp.Model("Probleme d'electricite")

    # Create variables
    x = model.addVars(centrales, villes, vtype=GRB.CONTINUOUS, name="x")

    # Set objective function
    obj = gp.quicksum(x[c, v] * couts_transport[c, v] for c in centrales for v in villes)
    obj += gp.quicksum((demandes[v] - gp.quicksum(x[c, v] for c in centrales)) * penalites[v] for v in villes)
    model.setObjective(obj, GRB.MINIMIZE)

    # Set constraints
    for c in centrales:
        model.addConstr(gp.quicksum(x[c, v] for v in villes) <= offres[c], name=f"Contrainte capacite {c}")

    for v in villes:
        model.addConstr(gp.quicksum(x[c, v] for c in centrales) >= demandes[v], name=f"Contrainte demande {v}")
    for c in centrales:
        for v in villes:
            model.addConstr(x[c, v] >= 0, name=f"Non-negativity constraint for x[{c}, {v}]")

    # Solve model
    model.optimize()
    # Print solution
    result_str = "Solution optimale :\n"
    for c in centrales:
        for v in villes:
            if x[c, v].x > 0:
                result_str += f"{x[c, v].x:.2f} millions de Kwh de la centrale {c} sont transportes a la ville {v}\n"
    result_str += f"Cout total : {obj.getValue():.2f} millions d'euros"

    unsatisfied_demand = {v: demandes[v] - sum(x[c, v].x for c in centrales) for v in villes}
    print("Demande insatisfaite :")
    for v in villes:
        if unsatisfied_demand[v] > 0:
            print(f"Il manque {unsatisfied_demand[v]:.2f} millions de Kwh a la ville {v}")

    return obj.getValue(), unsatisfied_demand, result_str

