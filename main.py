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

 #    leftSides1 =['S', 'A', 'B', 'C']
	# rightSides1 =['aA', 'bB', 'aS', 'bC', 'b', 'bS', 'aC', 'a', 'aB', 'bA']
	# productions =[Production(leftSides1[0], rightSides1[0]), Production(leftSides1[0], rightSides1[1]),
	# 	 		Production(leftSides1[1], rightSides1[2]), Production(leftSides1[1], rightSides1[3]), Production(leftSides1[1], rightSides1[4]),
	# 			Production(leftSides1[2], rightSides1[5]), Production(leftSides1[2], rightSides1[6]), Production(leftSides1[2], rightSides1[7]),
	# 		    Production(leftSides1[3], rightSides1[8]), Production(leftSides1[3], rightSides1[9])]

#GRAMATICA TO AUMATICO

    # leftSides = ['S', 'B']
    # rightSides = ['aS','bB','c','bB','aB']
    # productions =[Production(leftSides[0], rightSides[0]),Production(leftSides[0], rightSides[1]),Production(leftSides[0], rightSides[4]),
    #                Production(leftSides[1], rightSides[3]),Production(leftSides[1], rightSides[2])]
    
	leftSides = ['S', 'A', 'B']
	rightSides = ['0S', '1A', '0', '0B', '1S', '1', '0A', '1B']
	productions = [Production(leftSides[0], rightSides[0]), Production(leftSides[0], rightSides[1]), Production(leftSides[0], rightSides[2]),
				   Production(leftSides[1], rightSides[3]), Production(leftSides[1], rightSides[4]), Production(leftSides[1], rightSides[5]),
				   Production(leftSides[2], rightSides[6]), Production(leftSides[2], rightSides[7])]
	#print(Globals.grammar_count)
	myGrammar = Grammar(productions)
	#for elem in convert_to_automaton(myGrammar):
		#print(elem)
	#print(convert_to_automaton(myGrammar)[0])
#================================================================
#AUTOMATICO TO GRAMATICA @(A,b)=B
#Transitions[0][0][0]
	alfabeto=['a','b']
	estados=['S','A','B','C']
	estadoInicial='S'
	estadoFinal=['S']
	#Our table has:
	#a tuple with a set of states
	# a set of states
	Tabela=[myTransition(estados[0],alfabeto[0],'-'),
				 myTransition(estados[0],alfabeto[1],[estados[2]]),
				 myTransition(estados[1],alfabeto[0],[estadoFinal[0]]),
				 myTransition(estados[1],alfabeto[1],[estados[3]]),
				 myTransition(estados[2],alfabeto[0],[estados[3]]),
				 myTransition(estados[2],alfabeto[1],[estadoFinal[0]]),
				 myTransition(estados[3],alfabeto[0],[estados[2]]),
				 myTransition(estados[3],alfabeto[1],[estados[1]])]
	# for elem in Tabela: 
	# 	print(elem.getSecondtSet())
	# 	print(elem.getSymbole())
	for elem in AutToGram(Tabela,estadoFinal,estadoInicial):
		print(elem)
#==============================================================

    #		AFND TO AFD


	# alfabeto=['a','b']
	# estados=['S','A','B','C']
	# estadoInicial='S'
	# estadoFinal=['C']
	# #Our table has:
	# #a tuple with a set of states
	# # a set of states
	# Tabela=[myTransition(estados[0],alfabeto[0],[estados[1],estados[0]]),
	# 			 myTransition(estados[0],alfabeto[1],[estados[0]]),
	# 			 myTransition(estados[1],alfabeto[0],'-'),
	# 			 myTransition(estados[1],alfabeto[1],[estados[2]]),
	# 			 myTransition(estados[2],alfabeto[0],'-'),
	# 			 myTransition(estados[2],alfabeto[1],[estados[3]]),
	# 			 myTransition(estados[3],alfabeto[0],'-'),
	# 			 myTransition(estados[3],alfabeto[1],'-')]
	# for elem in Tabela: 


	#Gram=AutToGrammar(convert_to_automaton(myGrammar))

	#Globals.grammars.append=(myGrammar)

# 	leftSides1 = ['S', 'A', 'B', 'C']
# 	rightSides1 = ['aA', 'bB', 'aS', 'bC', 'b', 'bS', 'aC', 'a', 'aB', 'bA']
# 	productions1 = [Production(leftSides1[0], rightSides1[0]), Production(leftSides1[0], rightSides1[1]),
# 	 				Production(leftSides1[1], rightSides1[2]), Production(leftSides1[1], rightSides1[3]), Production(leftSides1[1], rightSides1[4]),
# 				   	Production(leftSides1[2], rightSides1[5]), Production(leftSides1[2], rightSides1[6]), Production(leftSides1[2], rightSides1[7]),
# 				   	Production(leftSides1[3], rightSides1[8]), Production(leftSides1[3], rightSides1[9])]
# 	#print(Globals.grammar_count)
# 	myGrammar1 = Grammar(productions1)
# 	#Globals.grammars.append=(myGrammar1