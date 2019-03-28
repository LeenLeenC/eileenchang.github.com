import sys

import Farmer_Fox as Problem

COUNT = None
BACKLINKS = {}

def runBFS():
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH
    COUNT = 0
    BACKLINKS = {}
    MAX_OPEN_LENGTH = 0
    IterativeBFS(initial_state)
    print(str(COUNT)+" states expaneded.")
    print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))

def IterativeBFS(initial_state):
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH
    OPEN = [initial_state]
    CLOSED = []
    BACKLINKS[initial_state] = None

    while OPEN != []:
      report(OPEN, CLOSED, COUNT)
      if len(OPEN)>MAX_OPEN_LENGTH: MAX_OPEN_LENGTH = len(OPEN)

      S = OPEN.pop(0)
      CLOSED.append(S)

      if Problem.GOAL_TEST(S):
        print(Problem.GOAL_MESSAGE_FUNCTION(S))
        path = backtrace(S)
        print('Length of solution path found: '+str(len(path)-1)+' edges')
        return
      COUNT += 1
      L = []
      for op in Problem.OPERATORS:
        if op.precond(S):
          new_state = op.state_transf(S)
          if not (new_state in CLOSED):
            L.append(new_state)
            BACKLINKS[new_state] = S
      for s2 in L:
          for i in range(len(OPEN)):
              if (s2 == OPEN[i]):
                  del L[i]; break
      OPEN = OPEN + L
      print_state_list("OPEN", OPEN)

def print_state_list(name, lst):
  print(name+" is now: ",end='')
  for s in lst[:-1]:
    print(str(s),end=', ')
  print(str(lst[-1]))

def backtrace(S):
  global BACKLINKS
  path = []
  while S:
    path.append(S)
    S = BACKLINKS[S]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(s)
  return path    
  
def report(open, closed, count):
  print("len(OPEN)="+str(len(open)), end='; ')
  print("len(CLOSED)="+str(len(closed)), end='; ')
  print("COUNT = "+str(count))

if __name__=='__main__':
  runBFS()

