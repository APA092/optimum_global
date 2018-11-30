#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):

    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    wip = []
    
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        wip.append((i-1, float(parts[0])/float(parts[1])))
        
    sorted_by_second = sorted(wip, key=lambda tup: tup[1], reverse=True)

    items = []

    for i in range(1, item_count+1):
        line = lines[i] 
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))    
    
    sorted_by_second = sorted(wip, key=lambda tup: tup[1], reverse=True)
    best_value = 0
    
    for n in range(item_count):
        value = 0
        weight = 0
        taken = [0]*len(items)
        
        for i in range(len(sorted_by_second)):
            item_index = sorted_by_second[i][0]
            item = items[item_index]
            if weight + item.weight <= capacity:
                taken[item.index] = 1
                value += item.value
                weight += item.weight
        #print str(n) + ' current best solution ' + str(best_value)
        #print str(n) + ' best solution ' + str(value)
        if best_value < value:
            best_value = value
            best_taken = taken
        del(sorted_by_second[0])

    
    output_data = str(best_value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, best_taken))
    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
            print solve_it(input_data)
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

