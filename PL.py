import gurobipy as gp
from gurobipy import GRB


def optimal_electricity_supply(centrales, villes, offres, demandes, couts_transport):
    # Create model
    model = gp.Model("Probleme d'electricite")

    # Create variables
    x = model.addVars(centrales, villes, vtype=GRB.CONTINUOUS, name="x")

    # Set objective function
    obj = gp.quicksum(x[c, v] * couts_transport[c, v] for c in centrales for v in villes)
    model.setObjective(obj, GRB.MINIMIZE)

    # Set constraints
    for c in centrales:
        model.addConstr(gp.quicksum(x[c, v] for v in villes) <= offres[c], name=f"Contrainte capacite {c}")

    for v in villes:
        model.addConstr(gp.quicksum(x[c, v] for c in centrales) >= demandes[v], name=f"Contrainte demande {v}")

    # Solve model
    model.optimize()

    # Print solution
    result_str = "Solution optimale :\n"
    for c in centrales:
        for v in villes:
            if x[c, v].x > 0:
                result_str += f"{x[c, v].x:.2f} millions de Kwh de la centrale {c} sont transportes a la ville {v}\n"
    result_str += f"Cout total : {obj.getValue():.2f} millions d'euros"


    return obj.getValue(), result_str
