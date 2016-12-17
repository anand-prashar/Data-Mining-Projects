#Minimize
#  +2 v1 +3 v2 +1 v3 +2 v4
#Subject to
#  v1 + v2 >= 1
#  v1 + v3 >= 1
#  v2 + v3 >= 1
 # v3 + v4 >= 1
#Binary
 # v1 v2 v3 v4
#End

from gurobipy import *
try:

    # Create a new model
    m = Model("mip1")

    # Create variables
    v1 = m.addVar(vtype=GRB.BINARY, name="v1")
    v2 = m.addVar(vtype=GRB.BINARY, name="v2")
    v3 = m.addVar(vtype=GRB.BINARY, name="v3")
    v4 = m.addVar(vtype=GRB.BINARY, name="v4")
    v5 = m.addVar(vtype=GRB.BINARY, name="v5")
    v6 = m.addVar(vtype=GRB.BINARY, name="v6")
    v7 = m.addVar(vtype=GRB.BINARY, name="v7")
    # Set objective
    m.setObjective( 5 * v1 + 2 * v2 + v3 + v4 + 3 * v5 + 8 * v6 + 4 * v7, GRB.MINIMIZE)

    # Add constraint: x + 2 y + 3 z <= 4
    m.addConstr(v1 + v4 >=1, "c0")

    # Add constraint: x + y >= 1
    m.addConstr(v1 + v3 >=1, "c1")
    
    m.addConstr(v2 + v6 >=1, "c2")
    
    m.addConstr(v4 + v7 >=1, "c3")
    m.addConstr(v2 + v5 >=1, "c4")
    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')
