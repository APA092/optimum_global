from ortools.linear_solver import pywraplp

def main():
#shipping rates per mt, direct delivery and delivery through hub
    to_hub = [[0.5,99999],
    [0.5,0.3],
    [1,0.5],
    [0.2,0.2]
    ];
    
    to_cust = [[1,2,99999,1,99999,99999],
    [99999,99999,1.5,0.5,1.5,99999],
    [1.5,99999,0.5,0.5,2,0.2],
    [2,99999,1.5,1,99999,1.5],
    [99999,99999,99999,0.5,0.5,0.5],
    [1,99999,1,99999,1.5,1.5]
    ];
    
    solver = pywraplp.Solver('Linear_test', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
#set variables
    hub = [[0 for x in range(len(to_hub[0]))] for y in range(len(to_hub))];
    cust = [[0 for x in range(len(to_cust[0]))] for y in range(len(to_cust))];
    
    for i in range(len(to_hub)):
        for j in range(len(to_hub[0])):
            hub[i][j] = solver.NumVar(0, solver.infinity(), 'Hub')
            
    for i in range(len(to_cust)):
        for j in range(len(to_cust[0])):
            cust[i][j] = solver.NumVar(0, solver.infinity(), 'Customer')
            
    
#set objective function
    objective = solver.Objective()
    for i in range(0, len(to_hub)):
        for j in range(0, len(to_hub[0])):
            objective.SetCoefficient(hub[i][j], to_hub[i][j])
    for i in range(0, len(to_cust)):
        for j in range(0, len(to_cust[0])):
            objective.SetCoefficient(cust[i][j], to_cust[i][j])
    objective.SetMinimization()
    
#create constraints
    #production not higher than capacity of factory in Liverpool
    constraint1 = solver.Constraint(0, 150000)
    for i in range(len(hub)):
        constraint1.SetCoefficient(hub[i][0],1)
    for j in range(len(cust)):
        constraint1.SetCoefficient(cust[i][0],1)
        
    #production not higher than capacity of factory in Brighton
    constraint1 = solver.Constraint(0, 150000)
    for i in range(len(hub)):
        constraint1.SetCoefficient(hub[i][1],1)
    for j in range(len(cust)):
        constraint1.SetCoefficient(cust[i][1],1)
    
    solver.Solve()
    
    for i in range(len(hub)):
        for j in range(len(hub[0])):
            print hub[i][j].solution_value()

if __name__ == '__main__':
    main()