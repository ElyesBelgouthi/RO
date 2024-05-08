import gurobipy as gp
from gurobipy import GRB


def optimal_transportation_supply(centrales, villes, offres, demandes, couts_transport, matiere, unite_matiere, monnaie):
    model = gp.Model("Probleme de transport")

    x = model.addVars(centrales, villes, vtype=GRB.CONTINUOUS, name="x")

    obj = gp.quicksum(x[c, v] * couts_transport[c, v] for c in centrales for v in villes)
    model.setObjective(obj, GRB.MINIMIZE)

    for c in centrales:
        model.addConstr(gp.quicksum(x[c, v] for v in villes) <= offres[c], name=f"Contrainte capacite {c}")

    for v in villes:
        model.addConstr(gp.quicksum(x[c, v] for c in centrales) >= demandes[v], name=f"Contrainte demande {v}")

    model.optimize()

    result_str = "Solution optimale :\n"
    for c in centrales:
        for v in villes:
            if x[c, v].x > 0:
                result_str += f"{x[c, v].x:.2f} {unite_matiere} de {matiere} de la centrale {c} sont transportes a la ville {v}\n"
    result_str += f"Cout total : {obj.getValue():.2f} {monnaie}"


    return obj.getValue(), result_str
