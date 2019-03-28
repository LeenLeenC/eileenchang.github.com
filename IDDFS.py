'''yuc15_IDDFS.py
by Yu-Ling Chang

Iterative Deepening Depth-First Search of a problem space.
Version 0.4, January 23 2019.

Assignment 2, in CSE 415, Winter 2019

This file contains Iterative Deepening DFS.'''

import sys

if sys.argv==[''] or len(sys.argv)<2:
#  import EightPuzzle as Problem
  import yuc15_Farmer_Fox as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to IDDFS")
COUNT = None
OPEN = []
BACKLINKS = {}


def IDDFS():
    '''Iteratively search greater depths of the search tree to find the goal state.'''
    print('Initial State:')
    initial_state = Problem.CREATE_INITIAL_STATE()
    print(initial_state)
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH, OPEN
    BACKLINKS = {}
    MAX_OPEN_LENGTH = 0
    for depth in range(1, sys.maxsize):
        COUNT = 0
        OPEN = [initial_state]
        BACKLINKS[initial_state] = None
        print('---------------------------' +str(depth))
        if IterativeDFS(OPEN, depth) == True:
           print(str(COUNT)+" states expaneded.")
           print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))
           return
        

def IterativeDFS(OPEN, limit):
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH
  while OPEN != []:
    report(OPEN, COUNT)
    if len(OPEN)>MAX_OPEN_LENGTH: MAX_OPEN_LENGTH = len(OPEN)

    S = OPEN.pop(0)

    if Problem.GOAL_TEST(S):
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      path = backtrace(S)
      print('Length of solution path found: '+str(len(path)-1)+' edges')
      return True
    
    elif limit == 0:
      COUNT = COUNT - 1
      return 'cutoff'

    L = []
    for op in Problem.OPERATORS:
      if op.precond(S):
        COUNT += 1
        new_state = op.state_transf(S)
        L.append(new_state)
        if (new_state in BACKLINKS) == False:
          BACKLINKS[new_state] = S
        result = IterativeDFS(L, limit - 1)
        if result == True:
          return True

def print_state_list(name, lst):
  print(name+" is now: ",end='')
  for s in lst[:-1]:
    print(str(s),end=', ')
  print(str(lst[-1]))     

   

def backtrace(s):
  global BACKLINKS
  path = []
  while s:
    path.append(s)
    s = BACKLINKS[s]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(s)
  return path


def report(open, count):
  print("len(OPEN)="+str(len(open)), end='; ')
  print("COUNT = "+str(count))

if __name__=='__main__':
    IDDFS()

        
            
                

    
    
    


