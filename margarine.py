from ortools.linear_solver import pywraplp

def main():
    data = [[110, 120, 130, 110, 115],
            [130, 130, 110, 90, 115],
            [110, 140, 130, 100, 95],
            [120, 110, 120, 120, 125],
            [100, 120, 150, 110, 105],
            [90, 100, 140, 80, 135]
        ];
        
    solver = pywraplp.Solver('Linear_test', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
        
#create variables
    buy = [[0 for x in range(len(data[0]))] for y in range(len(data))] 
    produce = [[0 for x in range(len(data[0]))] for y in range(len(data))] 
    store = [[0 for x in range(len(data[0]))] for y in range(len(data))] 
  
    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            buy[i][j] = solver.NumVar(0, solver.infinity(), 'buy')
            produce[i][j] = solver.NumVar(0, solver.infinity(), 'produce')
            store[i][j] = solver.NumVar(0, solver.infinity(), 'store')
   
#create objective
    objective = solver.Objective()
    for i in range(0, len(buy)):
        for j in range(0, len(buy[0])):
            objective.SetCoefficient(buy[i][j], data[i][j]*(-1))
            objective.SetCoefficient(produce[i][j], 150)
            objective.SetCoefficient(store[i][j], -5)
    objective.SetMaximization()
    
#create constraints
    #production not higher than capacity of machine 1
    constraint1 = [0]*len(produce)
    
    for i in range(0, 6):
        constraint1[i] = solver.Constraint(0, 250)
        for j in range(0, 3):
            constraint1[i].SetCoefficient(produce[i][j],1)
    
    #production not higher than capacity of machine 2
    constraint2 = [0]*len(produce)
    for i in range(0, 6):
        constraint2[i] = solver.Constraint(0, 200)
        for j in range(4, 5):
            constraint2[i].SetCoefficient(produce[i][j],1)
            
    solver.Solve()
    
    print '***************'
    print 'Production Plan'
    print '***************'
    for i in range(0, len(buy)):
        print str(produce[i][0].solution_value()) + ' '\
        +  str(produce[i][1].solution_value()) + ' '+  \
        str(produce[i][2].solution_value()) + ' '+  \
        str(produce[i][3].solution_value()) + ' ' +  \
        str(produce[i][4].solution_value())
        
        
if __name__ == '__main__':
  main()