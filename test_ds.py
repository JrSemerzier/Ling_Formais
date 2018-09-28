from structures import *
from regular_grammar import *
from non_deterministic_automaton import *
from deterministic_automaton import *
from globals import *
from operations_with_automata import *
from functools import *

'''
	Autoria: Adriano Tosetto, Giulio Simão
'''

def find_key(value, dictionary):
    return reduce(lambda x, y: x if x is not None else y,
                  map(lambda x: x[0] if x[1] == value else None,
                      dictionary.items()))

if __name__ == "__main__":
	#expr = '( 1 | 0 ) ? . ( ( 1 . 0 ) * . ( 0 . 1 ) ) * . ( 1 | 0 ) ?'
	#expr = ' ( ( C . D * ) * ) ? . B'
	#expr = '( ( C * | ( A . D ) ? ) . ( A . B ) * ) ?'
	#expr = '( A * ) *'
	#expr = '( A . B . C ) * | ( C . B . A ) *'
	expr = '(0|1(01*0)*1)+'
	re = RegExp(expr)
	print(re.to_automaton())
	'''q0 = State('q0')
	q1 = State('q1', True)

	t0 = Transition('a', q1)
	t1 = Transition('b', q1)

	t2 = Transition('a', q0)
	t3 = Transition('b', q0)

	q0.add_transition(t0)
	q0.add_transition(t1)

	q1.add_transition(t2)
	q1.add_transition(t3)

	a = Automaton(set([q0,q1]),set([q0]),q0,['a','b'], add = True)
	print(a.n_first_sentences_accepted(5))'''
