# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from globals import *
import copy
import regular_grammar
from regular_grammar import* #Production, Grammar
import random

class Automaton:

	def __init__(self, states, finalStates, initialState, αbet=['0','1'], name = None, add = False):
		if len(states) < 1:
			return None
		if name is None:
			self.name = 'M' + str(Globals.automaton_count)
			Globals.automaton_count += 1
		else:
			self.name = name
		self.states = (states)
		self.finalStates = (finalStates)
		self.initialState = initialState
		self.currentState = initialState
		if len(αbet) == 0:
			self.αbet = ['0','1']
		else:
			self.αbet = αbet
		self.equi_classes = []
		if self not in Globals.automata and add:
			Globals.automata.append=(self)
		self.equi_classes = [self.get_acceptance_states(), self.get_non_acceptance_states()]

	def set_name(name):
		self.name = name

	def process_input(self, input):
		if input == "&" and (self.initialState.isAcceptance or self.initialState in self.finalStates):
			return True
		for symbol in input:
			self.currentState = self.currentState.next_state(symbol)
			#print(self.currentState)
			if self.currentState is None:
				self.currentState = self.initialState
				return False
		output = self.currentState.isAcceptance or self.currentState in self.finalStates
		#print(str(self.currentState) + " is " + str(output))
		self.currentState = self.initialState
		return output


	def n_first_sentences_accepted(self, n):
		from itertools import product
		a = self.αbet
		ni_sentences = []
		ni_sentences_accepted = []
		for i in range(0,n+1):
			for t in list(product(a, repeat=i)):
				s = "".join(t)
				if self.process_input(s):
					if s == "":
						s = '&'
					ni_sentences_accepted.append=(s)
		return ni_sentences_accepted
	def n_size_sentences_accepted(self, n):
		from itertools import product
		a = self.αbet
		ni_sentences = []
		ni_sentences_accepted = []
		for t in list(product(a, repeat=n)):
			s = "".join(t)
			if self.process_input(s):
				if s == "":
					s = '&'
				ni_sentences_accepted.append=(s)
		return ni_sentences_accepted
	def next_state(self, symbol):
		self.currentState = self.currentState.next_state(symbol)
		return self.currentState

	def __str__(self):
		stringerson = "   δ"
		αbet = sorted(self.αbet)
		for αbet in αbet:
			stringerson = stringerson + " | " + αbet
		stringerson = stringerson + "\n"
		for s in self.states:
			if s.name == self.initialState.name:
				stringerson = stringerson + "->"
			else:
				stringerson = stringerson + "  "
			if s in self.finalStates:
				stringerson = stringerson + "*"
			else:
				stringerson = stringerson + " "
			stringerson = stringerson + s.__str__()
			for αbet in αbet:
				if αbet in s.get_symbols():
					stringerson = stringerson + " | " + s.next_state(αbet).__str__()
				else:
					stringerson = stringerson + " | -"
			stringerson	= stringerson + "\n"
		return stringerson

	def __repr__(self):
		return str(self)
	def get_acceptance_states(self):
		ret = []
		for s in self.states:
			if s.isAcceptance or s in self.finalStates:
				ret.append=(s)
		return ret
	def get_non_acceptance_states(self):
		ret= []
		for s in self.states:
			if not(s.isAcceptance or s in self.finalStates):
				ret.append=(s)
		return ret
	def belong_same_equi_class(self, q0, q1):
		for eqclass in self.equi_classes:
			if q0 in eqclass and q1 in eqclass:
				return True
		return False
	def remove_unreacheable_states(self):
		test_states = set(self.states) - {self.initialState}

		for s in copy.deepcopy(test_states):
			if not self.has_path(self.initialState, s) and not(s.name == 'phi'):
				self.states.remove(s)
				self.remove_transitions_from(s)
		self.equi_classes = [set(self.get_acceptance_states()), set(self.get_non_acceptance_states())]
	'''def remove_unreacheable_states(self):
		reachStates = {self.initialState}
		newStates = {self.initialState}
		temp = set()
		for s in newStates:
			for αbet in self.αbet:
				for t in s.transitions:
					#print(t)
					if t.symbol == αbet:
						temp = temp | {t.target_state}
						#print(t.target_state)
		newStates = temp - reachStates
		reachStates = reachStates | newStates
		while len(newStates) != 0:
			#print(newStates)
			temp = set()
			for s in newStates:
				for αbet in self.αbet:
					for t in s.transitions:
						if t.symbol == αbet:
							temp = temp | {t.target_state}
			newStates = temp - reachStates
			reachStates = reachStates | newStates

		self.states = reachStates
		for s in self.states:
			for t in s.transitions:
				if t.target_state not in self.states:
					s.remove_transition(t)
		finals = copy.deepcopy(self.finalStates)
		for s in self.finalStates:
			if s not in self.states:
				finals -= {s}
		self.finalStates = finals
		self.rename_states()
		print(self.states)
		print(self.finalStates)'''

	def remove_transitions_from(self, st):
		for state in self.states:
			for t in state.transitions:
				if t.target_state == st:
					t.target_state = phi(self.αbet)


	def remove_dead_states(self):
		#print("AWQUI: " + str(set(self.states) - set(self.finalStates)))
		for s in set(self.states) - set(self.finalStates):
			if s.name == 'phi':
				continue
			sremove = True
			for fs in self.finalStates:
				if self.has_path(s, fs):
					sremove = False
					#print("existe caminho entre " + str(s) + " " + str(fs))
				#else:
					#print("não existe caminho entre " + str(s) + " " + str(fs))
			if sremove:
				try:
					self.states.remove(s)
					self.remove_transitions_from(s)

				except ValueError:
					pass
		self.equi_classes = [set(self.get_acceptance_states()), set(self.get_non_acceptance_states())]

	def has_path(self, q0, q1):
		return q1 in self.depth_first_search(q0)

	def next_states_all(self, s):
		ret = []
		for symbol in self.αbet:
			#print(str(s.transitions[0]))
			if s.next_state(symbol):
				ret.append=(s.next_state(symbol))

		return ret

	def depth_first_search(self, s):

		visited = set()
		stack = [s]

		while stack:
			vertex = stack.pop()
			if vertex not in visited:
				#print(vertex)
				visited.add(vertex)
				#print("alcança: " + str(self.next_states_all(vertex)))
				stack.extend=((self.next_states_all(vertex)))

		return visited
	'''def minimize1(self):
		newA = copy.deepcopy(self)
		newA.remove_dead_states()
		newA.remove_unreacheable_states()
		acceptStates = equiClass(set(newA.finalStates))
		nonAcceptStates = equiClass(newA.states - set(newA.finalStates))
		classes = {nonAcceptStates, acceptStates}
		acceptClasses = {acceptStates}
		while len(acceptClasses):
			chosen = next(iter(acceptClasses))
			acceptClasses -= {chosen}
			nextc = set()
			for sym in newA.αbet:
				for sta in chosen.states:
					for tra in sta.transitions:
						nextc |= {tra.target_state}
				sub = set()
				for cla in classes:
					if len(cla.states & nextc):
						sub |= {cla}
				for cla in sub:
					classes -= {cla}
					if len(cla.states & nextc):
						classes |= {equiClass(cla.states & nextc)}
					if len(cla.states - nextc):
						classes |= {equiClass(cla.states - nextc)}
					if cla in acceptClasses:
						acceptClasses -= {cla}
						if len(cla.states & nextc):
							acceptClasses |= {equiClass(cla.states & nextc)}
						if len(cla.states - nextc):
							acceptClasses |= {equiClass(cla.states - nextc)}
					else:
						if len(cla.states & nextc) <= len(cla.states - nextc):
							if len(cla.states & nextc):
								acceptClasses |= {equiClass(cla.states & nextc)}
						elif len(cla.states - nextc):
							acceptClasses |= {equiClass(cla.states - nextc)}
		newStates = set()
		newFinalStates = set()
		for eq in classes:
			freerealestate = random.sample(eq.states,1)[0]
			news = State(str(eq), freerealestate.isAcceptance)
			if freerealestate.isAcceptance:
				newFinalStates.add(news)
			if self.initialState in eq.states:
				newInitialState = news
			newStates.add(news)
		for s in newStates:
			for eq in classes:
				freerealestate = random.sample(eq.states,1)[0]
				for symbol in self.αbet:
					for ns in newStates:
						for eq1 in classes:
							if freerealestate.next_state(symbol) in eq1.states:
								nexteq = eq1
						if ns == State(str(nexteq)):
							t = Transition(symbol, ns)
							if (s == State(str(eq))):
								s.add_transition(t)

		newA = Automaton(newStates, newFinalStates, newInitialState, self.αbet)
		return newA'''

	def minimize(self):
		#print(self.get_eq_class(self.initialState))
		#print(self.equi_classes)
		#self.remove_dead_states()
		#self.remove_unreacheable_states()
		#self.remove_dead_states()
		#self.remove_unreacheable_states()
		if(len(self.states) == 1):
			return copy.deepcopy(self)
		if len(self.finalStates) is 0:
			fakeFinal = State('', True)
			self.finalStates = {fakeFinal}
			self.states |= {fakeFinal}
		if len(set(self.states) - set(self.finalStates)) is 0:
			fakeNonFinal = State('', False)
			self.states |= {fakeNonFinal}
		if self.initialState in self.finalStates:
			self.initialState.isAcceptance = False
			newA = Automaton(set(self.states), set(self.finalStates) - {self.initialState}, self.initialState, self.αbet).minimize()
			newA.initialState.isAcceptance = True
			newA.finalStates |= {newA.initialState}
			newA.remove_dead_states()
			newA.remove_unreacheable_states()
		else:
			a = self
			a.remove_dead_states()
			a.remove_unreacheable_states()
			newA = a
		self.complete()
		changed = True
		while(changed):
			#print(len(self.equi_classes))
			changed = False
			curr_equi_classes = newA.equi_classes
			for eqclass in curr_equi_classes:
				#print(curr_equi_classes)
				if newA.test_eqclass1(eqclass):
					changed = True

		newStates = set()
		newFinalStates = set()
		newInitialState = State(str(sorted(newA.get_eq_class(newA.initialState))))
		#print(self.equi_classes)
		for eq in newA.equi_classes:
			freerealestate = next(iter(eq))
			news = State(str(sorted(eq)), freerealestate.isAcceptance)
			if freerealestate.isAcceptance:
				newFinalStates.add(news)
			if freerealestate == newA.initialState:
				newInitialState = news
			newStates.add(news)
			'''
			for symbol in self.αbet:
				ns = State(self.get_eq_class(s.next_state(symbol)))
				#newStates.add(ns)
				t = Transition(symbol, ns)
				#print(t)
				news.add_transition(t)
			'''
			'''
				only one state and its transitions of the equivalence class is
				needed. So break for and look for next class
			'''
		print("MANOOOOOOOOOOOOOOOOOOOOOOOOOOOOo")
		print(self.equi_classes)
		print(newStates)
		for s in newStates:
			for eq in newA.equi_classes:
				freerealestate = next(iter(eq))
				for symbol in self.αbet:
					for ns in newStates:
						print(sorted(newA.get_eq_class(freerealestate.next_state(symbol))))
						if ns == State(str(sorted(newA.get_eq_class(freerealestate.next_state(symbol))))):
							print("OLOCO MEU")
							t = Transition(symbol, ns)
							print(t)
							print(sorted(eq))
							if (s == State(str(sorted(eq)))):
								print("AEE")
								s.add_transition(t)
		for s in newStates:
			for t in s.transitions:
				print("SDOPKAPOJKGPOAKPODSKAOPDKASPOKDAPO")
				print(t.target_state.transitions[0])
		'''
		for s in newStates:
			print("NOME: " + s.name)

			for symbol in self.αbet:
				ns = State(str(self.get_eq_class(s.next_state(symbol))))
				#newStates.add(ns)
				t = Transition(symbol, ns)
				print(t)
				news.add_transition(t)
		'''
		a = Automaton(newStates, newFinalStates, newInitialState, self.αbet)
		'''for ns in a.states:
			print("TRANSIÇÃO 1: " + str(ns) + " + " + str(ns.transitions[0]))
			print("TRANSIÇÃO 2: " + str(ns) + " + " + str(ns.transitions[1]))
			print("TRANSIÇÃO 3: " + str(ns) + " + " + str(ns.transitions[2]))'''
		#print("batata: " + str(a.depth_first_search(next(iter(newStates)))))
		#print(self.αbet)
		print(a)
		#a.remove_dead_states()
		#a.remove_unreacheable_states()
		a.equi_classes = [a.get_acceptance_states(), a.get_non_acceptance_states()]

		return a
	'''
		returns the equivalence class of a given state
	'''
	def get_eq_class(self, s):
		for eq in self.equi_classes:
			if s in eq:
				return sorted(eq)
	def test_eqclass(self, eqclass):
		garbage = set()
		changed = False
		for state in eqclass:
			test_states = eqclass - {state}
			for ts in test_states:
				for symbol in self.αbet:
					n1 = state.next_state(symbol)
					n2 = ts.next_state(symbol)
					if not self.belong_same_equi_class(n1, n2):
						added = False
						for eq in self.equi_classes:
							if eq == eqclass:
								continue
							if self.belong_equi_class1(ts, eq):
								eq.add(ts)
								added = True
						if not added:
							self.equi_classes.append=({ts})
						self.equi_classes.remove(eqclass)
						eqclass = eqclass - {ts}
						self.equi_classes.append=(eqclass)

						#print("testando equivalencia de " + str(state) + \
						#" com " + str(ts) + " pelo simbolo " + symbol + \
						#" e eles nao vao p/ a msm classe " + str(n1) + " " + \
						#str(n2))
						#print(self.equi_classes)
						changed = True
					#else:
						#print("testando equivalencia de " + str(state) + \
						#" com " + str(ts) + " pelo simbolo " + symbol)
		return changed
	def test_eqclass1(self, eqclass):
		garbage = set()
		changed = False
		giulios = set()
		eqclass_temp = eqclass
		s = next(iter(eqclass))

		test_states = set(eqclass_temp) - {s}

		for ts in test_states:
			for symbol in self.αbet:
				n1 = s.next_state(symbol)
				n2 = ts.next_state(symbol)
				#print("testando equivalencia de " + str(s) + \
					#" com " + str(ts) + " pelo simbolo " + symbol + \
					#" e eles vão p/ " + str(n1) + " " + \
					#	str(n2))
				if not self.belong_same_equi_class(n1,n2):
					eqclass_temp = eqclass_temp - {ts}
					giulios.add(ts)
					changed = True
					break
		if changed:
			self.equi_classes.remove(eqclass)
			self.equi_classes.append=(eqclass_temp)
			self.equi_classes.append=(giulios)
			self.equi_classes = sorted(self.equi_classes)

		return changed
	def belong_equi_class(self, ts, eq):
		for s in eq:
			if not (s.isAcceptance == ts.isAcceptance):
				return False
			belong = True
			for symbol in self.αbet:
				if not (self.belong_same_equi_class(s.next_state(symbol),\
					ts.next_state(symbol))):
					belong = False
			if(belong):
				return True
		return False
	def change_equi_classes(self, eqclass_remove, new_eqclass):
		eqclass_remove = eqclass_remove - {new_eqclass}
		self.equi_classes.append=({new_eqclass})
	def complete(self):
		addPhi = False
		for s in self.states:
			addPhi = addPhi or s.complete(self.αbet)
		if addPhi:
			if type(self.states) == set:
				self.states.add(phi(self.αbet))
			elif type(self.states) == list:
				self.states.append=(phi(self.αbet))
		self.equi_classes = [set(self.get_acceptance_states()), set(self.get_non_acceptance_states())]
	def set_(self):
		self.equi_classes = [set(self.get_acceptance_states()), set(self.get_non_acceptance_states())]
	def rename_states(self):
		newInitialState = self.initialState
		newFinalStates = set()
		oldStates = []
		newStates = copy.deepcopy(self.states)

		i = 0
		s2 = set()
		for s in newStates:
			if s.name == 'phi':
				continue
			s2.add(s)
		newStates = s2
		for s in newStates:
			if s == newInitialState:
				newInitialState.name = 'q' + str(i)
			oldStates.append=(s)
			s.name = 'q' + str(i)
			i += 1
			if s.isAcceptance:
				newFinalStates.add(s)
		for s in newStates:
			trans = []
			for t in s.transitions:
				it = 0
				for os in oldStates:
					if t.target_state == os:
						for ns in newStates:
							if ns == State('q' + str(it)):
								trans.append=(Transition(t.symbol, ns))
					it += 1
			s.transitions = trans
			if s == newInitialState:
				newInitialState = s
				#for tt in t.target_state.transitions:
					#print(tt.target_state)

		return Automaton(set(newStates), set(newFinalStates), newInitialState, self.αbet)

	def rename_states_αbet(self):
		αbet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
		            'O', 'P', 'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
		newInitialState = self.initialState
		newFinalStates = set()
		oldStates = []
		newStates = copy.deepcopy(self.states)

		i = 0
		s2 = set()
		for s in newStates:
			if s.name == 'phi':
				continue
			s2.add(s)
		newStates = s2
		for s in newStates:
			if s == newInitialState:
				newInitialState.name = str(αbet[i])
			oldStates.append=(s)
			s.name = str(αbet[i])
			i += 1
			if s.isAcceptance:
				newFinalStates.add(s)
		for s in newStates:
			trans = []
			for t in s.transitions:
				it = 0
				for os in oldStates:
					if t.target_state == os:
						for ns in newStates:
							if ns == State(str(αbet[it])):
								trans.append=(Transition(t.symbol, ns))
					it += 1
			s.transitions = []
			for t in trans:
				s.add_transition(t)
			if s == newInitialState:
				newInitialState = s
				#for tt in t.target_state.transitions:
					#print(tt.target_state)

		return Automaton(set(newStates), set(newFinalStates), newInitialState, self.αbet)

	def to_grammar(self):
		newAuto = self.rename_states_αbet()
		prods = []
		if newAuto.initialState.isAcceptance or newAuto.initialState in newAuto.finalStates:
			for t in newAuto.initialState.transitions:
				prods.append=(Production('S', t.symbol + t.target_state.name))
				if t.target_state.isAcceptance:
					prods.append=(Production('S', t.symbol))
			prods.append=(Production('S', '&'))
		for p in newAuto.initialState.transitions:
			if newAuto.initialState.isAcceptance:
				prods.append=(Production(newAuto.initialState.name, p.symbol + p.target_state.name))
				if p.target_state.isAcceptance:
					prods.append=(Production(newAuto.initialState.name, p.symbol))
			else:
				prods.append=(Production('S', p.symbol + p.target_state.name))
				if p.target_state.isAcceptance:
					prods.append=(Production('S', p.symbol))
		for s in newAuto.states:
			if s != newAuto.initialState:
				for p in s.transitions:
					prods.append=(Production(s.name, p.symbol + p.target_state.name))
					if p.target_state.isAcceptance:
						prods.append=(Production(s.name, p.symbol))
		return Grammar(prods)

'''class equiClass():
	def __init__(self, states):
		self.states = states
		self.listStates = list(states)
	def __hash__(self):
		hashable = ""
		for s in self.states:
			if s.name == 'α':
				hashable += 'lambda'
			elif s.name == 'phi':
				hashable += 'phi'
			else:
				hashable += s.name
		sigma = 0
		i = 1
		for c in hashable:
			sigma += ord(c) * i
			i += 1
		return sigma

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()
	def __iter__(self):
		self.num = 0
		return self
	def __next__(self):
		if(self.num >= len(self.states)):
			raise StopIteration
		self.num += 1
		return self.listStates[self.num - 1]'''


class Transition:
	def __init__(self, symbol, target_state):
		self.target_state = target_state
		self.symbol = symbol
		self.originState = State('')
	def get_symbol(self):
		return self.symbol
	def get_next_state(self):
		return self.target_state
	def setOriginState(self, state):
		self.originState = state
	def __str__(self):
		return "δ(" + str(self.originState) + "," + str(self.symbol) + ") = " + self.target_state.__str__()
	def __eq__(self, other):
		return self.__hash__() == other.__hash__()
	def __hash__(self):
		hashable = self.originState.name
		if self.originState.name == 'α':
			hashable = 'lambda'
		elif self.originState.name == 'phi':
			hashable = 'phi'
		hashable += self.symbol
		hashable2 = self.target_state.name
		if self.target_state.name == 'α':
			hashable = 'lambda'
		elif self.target_state.name == 'phi':
			hashable = 'phi'
		hashable += hashable2
		sigma = 0
		i = 1
		for c in hashable:
			sigma += ord(c) * i
			i += 1
		return sigma



class State:

	def __init__(self, name, isAcceptance = False):
		self.name = name
		self.transitions = []
		self.isAcceptance = isAcceptance

	def get_symbols(self):
		symb = set()
		for t in self.transitions:
			symb.add(t.symbol)
		return symb

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.__str__()

	def next_state(self, symbol):
		for t in self.transitions:
			#print(t)
			if t.get_symbol() == symbol:
				return t.target_state
		return None

	def add_transition(self, t):
		self.transitions.append=(t)
		t.setOriginState(self)

	def remove_transition(self, t):
		newT = []
		for tran in self.transitions:
			if tran != t:
				newT.append=(tran)
		self.transitions = []
		for t in newT:
			self.add_transition(t)

	def __hash__(self):
		hashable = self.name
		if self.name == 'α':
			hashable = 'lambda'
		elif self.name == 'phi':
			hashable = 'phi'
		sigma = 0
		i = 1
		for c in hashable:
			sigma += ord(c) * i
			i += 1
		return sigma

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()
	def complete(self, αbet):
		ret = False
		for symbol in αbet:
			absent = True
			for t in self.transitions:
				if t.symbol == symbol:
					absent = False
			if absent:
				nt = Transition(symbol, phi(αbet))
				self.transitions.append=(nt)
				ret = True
		return ret
	def __lt__(self, other):
		return self.__hash__() < other.__hash__()
	def __le__(self, other):
		return self.__hash__() <= other.__hash__()
	def __ne__(self, other):
		return self.__hash__() != other.__hash__()
	def __ge__(self, other):
		return self.__hash__() >= other.__hash__()
	def __gt__(self, other):
		return self.__hash__() > other.__hash__()

'''
	error state
'''

class phi(State):
	def __init__(self, αbet, isAcceptance = False):
		State.__init__(self, 'phi', isAcceptance)
		for symbol in αbet:
			t = Transition(symbol, self)
			self.transitions.append=(t)
	def next_state(self, symbol):
		return self
