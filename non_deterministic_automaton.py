# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
import deterministic_automaton
from deterministic_automaton import State, Transition, Automaton
from globals import *
import copy

class NDTransition:
	def __init__(self,Term, symbol, target_states):#for cada target_state=aB; symbol=a
		self.target_states = target_states
		self.symbol = symbol
		self.originState=Term
	def get_symbol(self):
		return self.symbol
	def get_next_states(self):
		return self.target_states

	def setOriginState(self, state):
		self.originState = state

	def __str__(self):
		ret = "δ(" + str(self.originState) + "," + str(self.symbol) + ") = ["
		ret = ret + ",".join(s.__str__() for s in self.target_states)
		ret = ret + "]"
		return ret
	def __repr__(self):
		return self.__str__()

class NDState:
	def __init__(self, name, isAcceptance = False):
		self.name = name
		self.ndtransitions = list()
		self.isAcceptance = isAcceptance

	def get_symbols(self):
		symb = set()
		trans = self.ndtransitions
		if trans == None:
			trans = []
		for t in trans:
			symb.add(t.symbol)
		return symb

	def __str__(self):
		return self.name
	def __repr__(self):
		return self.__str__()
	def next_states(self, symbol):
		for t in self.ndtransitions:
			if t.get_symbol() == symbol:
				return t.get_next_states()
		return None

	def next_states(self, symbol, already_visited=set()):
		if self.ndtransitions == None:
			return set()
		next_states = set()
		for t in self.ndtransitions:
			if t.get_symbol() == symbol:
				next_states = set(t.get_next_states()) - already_visited
				already_visited = already_visited | next_states
				for s in next_states:
					already_visited = already_visited | s.next_states('&', already_visited)

		return already_visited
	def next_states_no_epsilon(self, symbol):
		next_states = set()
		if symbol == "&":
			return
	def next_states_str(self, symbol):
		for t in self.ndtransitions:
			if t.get_symbol() == symbol:
				return t.__str__()
		return None
	def add_transition(self, t):
		if self.ndtransitions == None:
			self.ndtransitions = [t]
		else:
			self.ndtransitions.append(t)
		t.setOriginState(self)

	def __hash__(self):
		hashable = self.name
		if self.name == 'α':
			hashable ='lambda'
		elif self.name == ' φ':
			hashable = ' φ'
		sigma = 0
		i = 1
		for c in hashable:
			sigma += ord(c) * i
			i += 1
		return sigma

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()

	def has_epsilon_transition(self):
		for t in self.ndtransitions:
			if t.symbol == '&':
				return True
		return False


class NDAutomaton:
	def __init__(self, states, finalStates, initialState, alphabet=['0','1'], name = None, add = False):
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
		self.currentStates = {initialState} | initialState.next_states('&')
		if len(alphabet) == 0:
			self.alphabet = ['0','1']
		else:
			self.alphabet = alphabet
		if self not in Globals.automata and add:
			Globals.automata.append(self)

	def __hash__(self):
		hashable = self.name
		if self.name == 'α':
			hashable ='lambda'
		elif self.name == ' φ':
			hashable = ' φ'
		sigma = 0
		i = 1
		for c in hashable:
			sigma += ord(c) * i
			i += 1
		return sigma

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()

	def process_input(self, input):
		if input == "&" and (self.initialState.isAcceptance or self.initialState in self.finalStates):
			return True
		for symbol in input:
			ns = set()
			for cs in self.currentStates:
				ns = ns | cs.next_states(symbol)
			self.currentStates = ns
			#print(self.currentStates)
			if self.currentStates is set():
				self.currentStates = {self.initialState} | self.initialState.next_states('&')
				return False
		output = False
		for s in self.currentStates:
			if s.isAcceptance or s in self.finalStates:
				output = True
		self.currentStates = {self.initialState} | self.initialState.next_states('&')
		return output
	def n_first_sentences_accepted(self, n):
		from itertools import product
		a = self.alphabet
		ni_sentences = []
		ni_sentences_accepted = []
		for i in range(0,n+1):
			for t in list(product(a, repeat=i)):
				s = "".join(t)
				if self.process_input(s):
					if s == "":
						s = '&'
					ni_sentences_accepted.append(s)
		return ni_sentences_accepted
	def n_size_sentences_accepted(self, n):
		from itertools import product
		a = self.alphabet
		ni_sentences = []
		ni_sentences_accepted = []
		for t in list(product(a, repeat=n)):
			s = "".join(t)
			if self.process_input(s):
				if s == "":
					s = '&'
				ni_sentences_accepted.append=(s)
		return ni_sentences_accepted
	def next_states(self, symbol, go_ahead=True):
		temp = []
		for state in self.currentStates:
			s = state.next_states(symbol)
			if s is not None:
				temp.extend=(s)
		#remove duplicated states
		temp = list(set(temp))
		if go_ahead:
			self.currentStates = temp
			return self.currentStates
		else:
			return temp

	def transition_table(self):
		already_visited = []
		alphabet = ['0','1']

	def __str__(self):
		stringerson = "   δ"
		hasEpsilon = False
		for s in self.states:
			trans = s.ndtransitions
			if trans == None:
				trans = []
			for t in trans:
				if t.symbol == '&':
					hasEpsilon = True
		alphabet = sorted(self.alphabet)
		if hasEpsilon and '&' not in alphabet:
			alphabet += ['&']
		for alphabet in alphabet:
			stringerson = stringerson + " |  " + alphabet + " "
		stringerson = stringerson + "\n"
		for s in self.states:
			if s == self.initialState:
				stringerson = stringerson + "->"
			else:
				stringerson = stringerson + "  "
			if s in self.finalStates:
				stringerson = stringerson + "*"
			else:
				stringerson = stringerson + " "
			stringerson = stringerson + s.__str__()
			for alphabet in alphabet:
				if alphabet in s.get_symbols():
					stringerson = stringerson + " | " + s.next_states(alphabet).__str__()
				else:
					stringerson = stringerson + " |  - "
			stringerson	= stringerson + "\n"
		return stringerson

	def __repr__(self):
		return str(self)

	def remove_epsilon_transition(self):
		newStates = set()
		newFinalStates = set()
		for s in self.states:
			#print("s = " + str(s))
			news = copy.deepcopy(s)
			news.isAcceptance = s.isAcceptance
			if s == self.initialState:
				newInitial = news
			next_states_by_s = s.next_states('&')
			for ts in next_states_by_s:
				if ts.isAcceptance:
					news.isAcceptance = True
			for symbol in self.alphabet:
				trans = copy.deepcopy(news.ndtransitions)
				if trans == None:
					trans = []
				target_states = list()
				for ns in next_states_by_s:
					#print("ns = " + str(ns))
					target_states += ns.next_states(symbol)
				for t in trans:
					#print(trans)
					#print("t = " + str(t))
					#print("target_states = " + str(target_states))
					if t.symbol == "&":
						news.ndtransitions = trans[:].remove(t)
				if len(target_states) > 0:
					news.add_transition(NDTransition(symbol, set(target_states)))
			newStates.add(news)
			if news.isAcceptance:
				newFinalStates.add(news)
		return NDAutomaton(newStates, newFinalStates, newInitial, self.alphabet)


	'''
		determinization functions:
	'''

	def determinize_states(self, states, finalStates, newStates, determinizedStates):
		if len(states) == 1:
			oldState = list(states)[0]
			newState = State(oldState.name, oldState.isAcceptance)
			if newState in determinizedStates:
				return newState
			determinizedStates.add(newState)
			for s in self.alphabet:
				nextStates = set()
				trans = oldState.ndtransitions
				if trans == None:
					trans = []
				for t in trans:
					if t.symbol == s:
						nextStates = nextStates | set(t.target_states)
				if len(nextStates) != 0:
					newT = Transition(s, self.determinize_states(nextStates, finalStates, newStates, determinizedStates))
					newState.add_transition(newT)
					#print(str(newState) + " + " + str(newT))
			if newState in determinizedStates:
				determinizedStates.remove(newState)
				determinizedStates.add(newState)
			if newState in newStates:
				newStates.remove(newState)
			newStates.add(newState)
			if oldState in self.finalStates:
				finalStates.add(newState)
			return newState
		accpt = False
		for s in states:
			accpt = accpt or s.isAcceptance
		newState = State(states.__str__(), accpt)
		if newState in determinizedStates:
			return newState
		determinizedStates.add(newState)
		for a in self.alphabet:
			nextStates = set()
			for s in states:
				trans = s.ndtransitions
				if trans == None:
					trans = []
				for t in trans:
					if t.symbol == a:
						nextStates = nextStates | set(t.target_states)
			if len(nextStates) != 0:
				newState.add_transition(Transition(a, self.determinize_states(nextStates, finalStates, newStates, determinizedStates)))
		if newState in determinizedStates:
			determinizedStates.remove(newState)
			determinizedStates.add(newState)
		if any(s in self.finalStates for s in states):
			finalStates.add(newState)
		if newState in newStates:
			newStates.remove(newState)
		if newState.name != "set()":
			newStates.add(newState)
		if newState in finalStates:
			finalStates.remove(newState)
		if newState.isAcceptance:
			finalStates.add(newState)
		return newState

	def determinize(self):
		newA = self.remove_epsilon_transition()
		print(newA)
		newStates = set()
		finalStates = set()
		determinized = set()
		for s in newA.states:
			newState = State(s.name, s.isAcceptance)
			if s.name != "":
				newStates.add(newState)
			if s == newA.initialState:
				newInitialState = newState
		for s in newStates:
			if s.isAcceptance:
				finalStates.add(s)
		for s in newA.states:
			newState = State(s.name, s.isAcceptance)
			trans = s.ndtransitions
			if trans == None:
				trans = []
			for sym in self.alphabet:
				nextStates = set()
				for t in trans:
					if t.symbol == sym:
						nextStates = nextStates | set(t.target_states)
				if len(nextStates) != 0:
					newState.add_transition(Transition(sym, newA.determinize_states(nextStates, finalStates, newStates, determinized)))
			if newState in newStates:
				newStates.remove(newState)
			if newState.name != "set()":
				newStates.add(newState)
			if newState in finalStates:
				finalStates.remove(newState)
			if newState.isAcceptance:
				finalStates.add(newState)
		for s in newStates:
			if s == newInitialState:
				newInitialState = s
		for s in newStates:
			for t in s.transitions:
				for os in newStates:
					if t.target_state == os:
						s.remove_transition(t)
						s.add_transition(Transition(t.symbol, os))
		return Automaton(set(newStates), set(finalStates), newInitialState, self.alphabet)

class EpsilonAutomaton(NDAutomaton):
	def __init__(self, states, finalStates, initialState, alphabet=['0','1']):
		NDAutomaton.__init__(self,states, finalStates, initialState, alphabet)

	def next_states(self, symbol, go_ahead=True):
		temp = []
		for state in self.currentStates:
			s = state.next_states(symbol)
			if s is not None:
				temp.extend=(s)
		#remove duplicated states
		temp = list(set(temp))
		if go_ahead:
			self.currentStates = temp
			return self.currentStates
		else:
			return temp
