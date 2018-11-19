from ortools.linear_solver import pywraplp

def main():
#shipping rates per mt, direct delivery and delivery through hub
    to_hub = [[0.5,99999],
    [0.5,0.3],
    [1,0.5],
    [0.2,0.2]
    ];
    
    factory = ['Liverpool', 'Brighton'];
    whs = ['Newcastle', 'Birmingham', 'London', 'Exeter'];
    locations = factory + whs

    to_cust = [[1,2,99999,1,99999,99999],
    [99999,99999,1.5,0.5,1.5,99999],
    [1.5,99999,0.5,0.5,2,0.2],
    [2,99999,1.5,1,99999,1.5],
    [99999,99999,99999,0.5,0.5,0.5],
    [1,99999,1,99999,1.5,1.5]
    ];

#customers demand    
    demand = [50000, 10000, 40000, 35000, 60000, 20000];
    
#terminal throughput
    transit = [70000, 50000, 100000, 40000];
    
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
    constraint2 = solver.Constraint(0, 200000)
    for i in range(len(hub)):
        constraint2.SetCoefficient(hub[i][1],1)
    for j in range(len(cust)):
        constraint2.SetCoefficient(cust[i][1],1)
    
    #customers demand respected
    constraint3 = [0]*len(demand)
    for i in range(len(demand)):
        constraint3[i] = solver.Constraint(demand[i], solver.infinity())
        for j in range(len(to_cust[0])):
            constraint3[i].SetCoefficient(cust[i][j],1)
            
    #terminals throughput respected
    constraint4 = [0]*len(transit)
    for i in range(len(transit)):
        constraint4[i] = solver.Constraint(0, transit[i])
        for j in range(len(hub[0])):
            constraint4[i].SetCoefficient(hub[i][j],1)
            
    #terminal in, terminal out
    constraint5 = [0]*len(transit)
    for i in range(len(transit)):
        constraint5[i] = solver.Constraint(0,0)
        for j in range(len(hub[0])):
            constraint5[i].SetCoefficient(hub[i][j],1)
        for t in range(len(cust)):
            constraint5[i].SetCoefficient(cust[t][i+2],-1)
            
    solver.Solve()

    for i in range(len(cust)):
        print '*********************'
        for j in range(len(cust[0])):
            print 'From ' + locations[i] + ' ' + 'to Customer' + str(j+1) + ' ' +  str(cust[j][i].solution_value())
            
    for i in range(len(hub)):
        print '*********************'
        for j in range(len(hub[0])):
            print 'From ' + factory[j] + ' ' + 'to Hub ' + whs[i] + ' ' +  str(hub[i][j].solution_value())
    print '*********************'         
    print 'Total cost: ' + str(solver.Objective().Value())
    
if __name__ == '__main__':
    main()