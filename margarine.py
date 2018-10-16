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
    print len(buy)
    
if __name__ == '__main__':
  main()