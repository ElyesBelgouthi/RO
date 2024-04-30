import gurobipy as gp
from gurobipy import GRB

def solve_knapsack(values, weights, capacity):
    # Create model
    model = gp.Model("Knapsack Problem")

    # Create variables
    num_items = len(values)
    x = model.addVars(num_items, vtype=GRB.BINARY, name="x")

    # Set objective function
    obj = gp.quicksum(values[i] * x[i] for i in range(num_items))
    model.setObjective(obj, GRB.MAXIMIZE)

    # Set constraint for capacity
    model.addConstr(gp.quicksum(weights[i] * x[i] for i in range(num_items)) <= capacity, name="Capacity")

    # Solve model
    model.optimize()

    # Extract solution
    selected_items = [i for i in range(num_items) if x[i].x > 0.5]
    total_value = sum(values[i] for i in selected_items)

    return total_value, selected_items
