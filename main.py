#!/usr/bin/env python
# -*- coding: utf-8 -*-
from structures import *
from regular_grammar import *
from non_deterministic_automaton import *
from deterministic_automaton import *
from globals import *
from operations_with_automata import *
from operations_with_grammars import *
import sys
sys.path.append('view/')#import the files from view overthere
from main_window import *

if __name__ == "__main__":

    leftSides = ['S', 'B']
    rightSides = ['aS','bB','c','bB','aB']
    productions =[Production(leftSides[0], rightSides[0]),Production(leftSides[0], rightSides[1]),Production(leftSides[0], rightSides[4]),
                   Production(leftSides[1], rightSides[3]),Production(leftSides[1], rightSides[2])]
    
	# leftSides = ['S', 'A', 'B']
	# rightSides = ['0S', '1A', '0', '0B', '1S', '1', '0A', '1B']
	# productions = [Production(leftSides[0], rightSides[0]), Production(leftSides[0], rightSides[1]), Production(leftSides[0], rightSides[2]),
	# 			   Production(leftSides[1], rightSides[3]), Production(leftSides[1], rightSides[4]), Production(leftSides[1], rightSides[5]),
	# 			   Production(leftSides[2], rightSides[6]), Production(leftSides[2], rightSides[7])]
	#print(Globals.grammar_count)
    myGrammar = Grammar(productions)
    print(convert_to_automaton(myGrammar))
	#Globals.grammars.append=(myGrammar)

# 	leftSides1 = ['S', 'A', 'B', 'C']
# 	rightSides1 = ['aA', 'bB', 'aS', 'bC', 'b', 'bS', 'aC', 'a', 'aB', 'bA']
# 	productions1 = [Production(leftSides1[0], rightSides1[0]), Production(leftSides1[0], rightSides1[1]),
# 	 				Production(leftSides1[1], rightSides1[2]), Production(leftSides1[1], rightSides1[3]), Production(leftSides1[1], rightSides1[4]),
# 				   	Production(leftSides1[2], rightSides1[5]), Production(leftSides1[2], rightSides1[6]), Production(leftSides1[2], rightSides1[7]),
# 				   	Production(leftSides1[3], rightSides1[8]), Production(leftSides1[3], rightSides1[9])]
# 	#print(Globals.grammar_count)
# 	myGrammar1 = Grammar(productions1)
# 	#Globals.grammars.append=(myGrammar1)


# 	#expr = '(a(bb)*a|(b|aba)(a(bb)*a)*(b|aba))*(b|aba)(a(bb)*a)*?'
# 	expr = '(0|1(01*0)*1)(0|1(01*0)*1)*'
# 	re = RegExp(expr)
# 	print(re.to_automaton())
# 	print(re.to_automaton().minimize())
# 	Globals.grammar_count = 1
# 	Globals.automaton_count = 1
# 	win = MainWindow()
# 	#print("test = " + str(test))
# 	#print(test.handle_leaf())
# 	#print(nodo.right.symbol)
# #display(nodo,1)
