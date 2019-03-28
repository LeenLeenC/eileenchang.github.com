'''yuc15_Farmer_Fox.py
by Yu-Ling Chang

Assignment 2, in CSE 415, Winter 2019

This file contains my problem formulation for the problem
of the Farmer, Fox, Chicken, and Grain.'''

PROBLEM_DESC=\
 '''A farmer needs to take a fox, chicken and sack of grain across a river using a small
boat. He can only take one of the three items in the boat with him at one time. The
fox must never be left alone with the chicken, and the chicken must never be left alone
with the grain. '''

#<METADATA>
SOLUZION_VERSION = "2.0"
PROBLEM_NAME = "Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "2.0"
PROBLEM_AUTHORS = ['Yu-Ling Chang']
PROBLEM_CREATION_DATE = "23-JAN-2018"

#<COMMON_CODE>
LEFT = 0
RIGHT = 1
F = 0
C = 1
G = 2


class State():

    def __init__(self, d=None):
        if d == None:
           d = {'Animal_And_Food':[[0,0],[0,0],[0,0]],
                'Farmer': LEFT}
        self.d = d

    def __eq__(self, s2):
        for prop in ['Animal_And_Food', 'Farmer']:
            if self.d[prop] != s2.d[prop]: return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        p = self.d['Animal_And_Food']
        txt = "\n F on left:"+str(p[F][LEFT])+"\n"
        txt += " C on left:"+str(p[C][LEFT])+"\n"
        txt += " G on left:"+str(p[G][LEFT])+"\n"
        txt += " F on right:"+str(p[F][RIGHT])+"\n"
        txt += " C on right:"+str(p[C][RIGHT])+"\n"
        txt += " G on right:"+str(p[G][RIGHT])+"\n"
        side = 'left'
        if self.d['Farmer'] == 1: side = 'right'
        txt += "Farmer is on the "+side+".\n"
        return txt                   

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy (self):
        #Performs an appropriately deep copy of a state,
        #for use by operators in creating new states.
        news = State({})
        news.d['Animal_And_Food'] = [self.d['Animal_And_Food'][F_or_C_or_G][::] for F_or_C_or_G in [F,C,G]]
        news.d['Farmer'] = self.d['Farmer']
        return news

    def can_move(self, f, c, g):
        '''Tests whether it's legal to move the farmer and take f fox, c chicken, and g grain.'''
        side = self.d['Farmer'] # Where the farmer is.
        p = self.d['Animal_And_Food']
        f_available = p[F][side]
        c_available = p[C][side]
        g_available = p[G][side]
        if f_available < f: return False
        if c_available < c: return False
        if g_available < g: return False
        f_remaining = p[F][side]-f
        c_remaining = p[C][side]-c
        g_remaining = p[G][side]-g
        if f_remaining == c_remaining == 1: return False
        if c_remaining == g_remaining == 1: return False
        if p[F][1-side] == 1 and p[C][1-side] == 1: return False
        if p[C][1-side] == 1 and p[G][1-side] == 1: return False
        return True

    def move(self, f, c, g):
        '''Assuming it's legal to make the move, this computes the new state resulting from moving farmer
         carrying f fox, c chicken, and g grain.'''
        news = self.copy()
        side = self.d['Farmer']
        p = news.d['Animal_And_Food']
        p[F][side] = p[F][side]-f
        p[C][side] = p[C][side]-c
        p[G][side] = p[G][side]-g
        p[F][1-side] = p[F][1-side]+f
        p[C][1-side] = p[C][1-side]+c
        p[G][1-side] = p[G][1-side]+g
        news.d['Farmer'] = 1-side
        return news

def goal_test(s):
        '''If fox, chicken, and grain are on the right, then s is a goal state.'''
        p = s.d['Animal_And_Food']
        return (p[F][RIGHT] ==1 and p[C][RIGHT] ==1 and p[G][RIGHT] ==1)

def goal_message(s):
        return "Congratulations on successfully guiding the fox, chicken, and grain across the river!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d = {'Animal_And_Food':[[1,0], [1,0], [1,0]], 'Farmer': LEFT})

#<OPERATORS>
FFCG_combinations = [(1,0,0), (0,1,0), (0,0,1), (0,0,0)]

OPERATORS = [Operator(
    "Cross the river with "+str(f)+" Fox, "+str(c)+" Chicken, or "+str(g)+" Grain",
    lambda s, f1=f, c1=c, g1=g: s.can_move(f1,c1,g1),
    lambda s, f1=f, c1=c, g1=g: s.move(f1,c1,g1) )
    for (f,c,g) in FFCG_combinations]

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)       
         
                   
