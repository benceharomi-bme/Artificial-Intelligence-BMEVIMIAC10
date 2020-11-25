import sys
from functools import reduce
from copy import copy

def read_input():
    nodes = []
    number_of_nodes = int(input())
    children = []

    for a in range(number_of_nodes):
        input_line = input()
        tab_splitted = list(input_line.split('\t'))
        k = int(tab_splitted.pop(0))
        number_of_parents = int(tab_splitted.pop(0))
        parents = []
        if(number_of_parents == 0):
            dictionary = {}
            comma_splitted = tab_splitted.pop(0).split(',')
            for i in range(k):
                dictionary[i] = float(comma_splitted[i])
            nodes.append(Node(is_discrete = True, distribution = dictionary, parents = parents, k = k, id = a))
        else:
            array = []
            for i in range(number_of_parents):
                parent_index = int(tab_splitted.pop(0))
                parents.append(nodes[parent_index])
                children.append([parent_index, a])
                
            for i in range(len(tab_splitted)):
                colon_splitted = tab_splitted.pop(0).split(':')
                comma_splitted_first = colon_splitted[0].split(',')
                comma_splitted_second = colon_splitted[1].split(',')
                for j in range(k):
                    inner_array = []
                    for z in range(number_of_parents):
                        inner_array.append(int(comma_splitted_first[z]))
                    inner_array.append(int(j))
                    inner_array.append(float(comma_splitted_second[j]))
                    array.append(inner_array)
            
            node = Node(is_discrete = False, probability_table =  array, parents = parents, k = k, id = a)
            nodes.append(node)

    for item in children:
      l = copy(nodes[item[0]].children)
      l.append(item[1])
      nodes[item[0]].children = l


    

    number_of_known = int(input())
    for a in range(number_of_known):
        input_line = input()
        tab_splitted = list(input_line.split('\t'))
        index = int(tab_splitted[0])
        value = int(tab_splitted[1])
        nodes[index].value = value
    wanted_node_index = int(input())

    return nodes, wanted_node_index

class Node():
  def __init__(self, k, is_discrete, id: int, parents: list = [], distribution = {}, probability_table: list = [], value: int = None, children: list = []):
    self.is_discrete = is_discrete
    self.parents = parents
    self.distribution = distribution
    self.probability_table = probability_table
    self.value = value
    self.k = k
    self.children = children
    self.id = id

def calculate(node: Node):
  if(node.value != None):
    table = filterTable(node.probability_table, -2, node.value)
  else:
    table = node.probability_table
  parent_probabilities = []
  for parent in node.parents:
    if(parent.value != None):
      table = filterTable(table, node.parents.index(parent), parent.value)
    if(parent.is_discrete):
      parent_probabilities.append(parent.distribution)
    else:
      parent_probabilities.append(calculate(parent))
  return calculateProbabilities(table, parent_probabilities)  
  
def filterTable(table: list, column: int, value:int):
  return list(filter(lambda row: row[column] == value, table))

def calculateProbabilities(table: list, parent_probabilities: list):
  dictionary = {}
  sum = 0
  for row in table:
    multiplier = 1
    for index in range(len(parent_probabilities)):
      multiplier *= parent_probabilities[index].get(row[index])
    multiplier *= row[-1]
    if(dictionary.get(row[-2])):
      dictionary[row[-2]] += multiplier
    else:
      dictionary[row[-2]] = multiplier
  return dictionary
    
def calculateChildren(nodes, node, calculated):
  for child in node.children:
      if(nodes[child].value != None):
        table = filterTable(nodes[child].probability_table, 0, nodes[nodes.index(node)].value)
        table = filterTable(table, -2, nodes[child].value)
        calculated = calculated * table[0][-1]
  return calculated

def main():
  fd = open('input.txt', 'r')
  sys.stdin = fd

  nodes, wanted_node_index = read_input()

  array = []
  for i in range(nodes[wanted_node_index].k):
    nodes[wanted_node_index].value = i
    calculated = calculate(nodes[wanted_node_index]).get(i)
    calculated = calculateChildren(nodes, nodes[wanted_node_index], calculated)
    array.append(calculated)
  
  sum = reduce(lambda a,b: a+b, array)
  alfa = 1 / sum
  last = list(map(lambda a: a*alfa,  array))
  for i in last:
    print(i)

if __name__ == '__main__':
    main()
