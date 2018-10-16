from ortools.linear_solver import pywraplp

def main():
    data = [['January', 110, 120, 130, 110, 115],
            ['February', 130, 130, 110, 90, 115],
            ['March', 110, 140, 130, 100, 95],
            ['April', 120, 110, 120, 120, 125],
            ['May', 100, 120, 150, 110, 105],
            ['June', 90, 100, 140, 80, 135]
        ];
        
    name = ['veg1', 'veg2', 'veg3', 'animal1', 'animal2'];
    solver = pywraplp.Solver('ProductPlanning', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    
    x = [[]]*len(data)
    
    for i in range(0, len(data[0])-1):
        x[i] = solver.NumVar(0, solver.infinity(), name[i])
        
    constraint = solver.Constraint(0,250)
    for i in range(0,len(data[0])-1):
        constraint.SetCoefficient(x[i], data[0][i+1])

    objective = solver.Objective()
    for i in range(0,len(data[0])-1):
        objective.SetCoefficient(x[i], 1)
    objective.SetMaximization()
    
    solver.Solve()
    for i in range(0, 4):
        print x[i]
        print x[i].solution_value()
    
    
if __name__ == '__main__':
  main()