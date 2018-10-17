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
            produce[i][j] = solver.NumVar(0, 600, 'produce')
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
        for j in range(3, 5):
            constraint2[i].SetCoefficient(produce[i][j],1)
            
    #production not higher than resources available
    constraint3 = [[0 for x in range(len(data[0]))] for y in range(len(data))]
    for i in range(0, len(produce)):
        for j in range(0, len(produce[0])):
            constraint3[i][j] = solver.Constraint(0, solver.infinity())
            constraint3[i][j].SetCoefficient(produce[i][j], -1)
            constraint3[i][j].SetCoefficient(store[i][j], 1)
            constraint3[i][j].SetCoefficient(buy[i][j], 1)
            
    #storage limited to 500 units
    constraint4 = [[0 for x in range(len(data[0]))] for y in range(len(data))]        
    for i in range(0, len(produce)):
        for j in range(0, len(produce[0])):    
            constraint4[i][j] = solver.Constraint(0, 500)
            constraint4[i][j].SetCoefficient(store[i][j], 1)
            
    #initial storage
    constraint5 = [0]*len(store[0])
    for i in range(0, len(store[0])):
        constraint5[i] = solver.Constraint(500, 500)
        constraint5[i].SetCoefficient(store[0][i],1)
        constraint5[i].SetCoefficient(buy[0][i],-1)
        constraint5[i].SetCoefficient(produce[0][i],1)
    
    #final storage
    constraint6 = [0]*len(store[0])
    for i in range(0, len(store[0])):
        constraint6[i] = solver.Constraint(500, 500)
        constraint6[i].SetCoefficient(store[4][i],1)
        constraint6[i].SetCoefficient(buy[5][i],1)
        constraint6[i].SetCoefficient(produce[5][i],-1)
    
    #linking storage and production
    constraint7 = [[0 for x in range(len(data[0]))] for y in range(len(data))]
    for i in range(1,6):
        for j in range(0,len(data[0])):
            constraint7[i][j] = solver.Constraint(0, 0)
            constraint7[i][j].SetCoefficient(store[i-1][j],1)
            constraint7[i][j].SetCoefficient(store[i][j],-1)
            constraint7[i][j].SetCoefficient(buy[i][j],1)
            constraint7[i][j].SetCoefficient(produce[i][j],-1)
            
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
        
    print '***************'
    print 'Storage Plan'
    print '***************'
    for i in range(0, len(buy)):
        print str(store[i][0].solution_value()) + ' '\
        +  str(store[i][1].solution_value()) + ' '+  \
        str(store[i][2].solution_value()) + ' '+  \
        str(store[i][3].solution_value()) + ' ' +  \
        str(store[i][4].solution_value())
        
    print '***************'
    print 'Purchase Plan'
    print '***************'
    for i in range(0, len(buy)):
        print str(buy[i][0].solution_value()) + ' '\
        +  str(buy[i][1].solution_value()) + ' '+  \
        str(buy[i][2].solution_value()) + ' '+  \
        str(buy[i][3].solution_value()) + ' ' +  \
        str(buy[i][4].solution_value())
        
        
if __name__ == '__main__':
  main()