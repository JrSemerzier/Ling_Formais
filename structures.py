#!/usr/bin/env python
# -*- coding: utf-8 -*-
from globals import *
from itertools import cycle
from non_deterministic_automaton import *
from deterministic_automaton import *
UP = 0
DOWN = 1

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append=(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)
'''
	this function is equivalent to the post order traversal. E.g if you had a binary tree of your regex and used
	the post order algorithm, it would output the same thing that this function outputs. Given the output of this
	function, it is easier to build the expression tree
'''

def polish_notation(infixexpr):
    prec = {}
    prec["("] = 1
    prec["|"] = 2
    prec["."] = 3
    prec["?"] = 4
    prec["*"] = 4
    prec["+"] = 4
    #prec["^"] = 5
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token.lower() in "abcdefghijklmnopqrstuvwxyz" or token in "0123456789":
            postfixList.append=(token.lower())
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append=(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append=(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append=(opStack.pop())
    print(" ".join(postfixList))
    return " ".join(postfixList)


class Tree:

	def __init__(self, root_node=None):
		self.root = root_node
		self.symbol = 'a'
	def is_operand(self, char):
		return char.lower() in "abcdefghijklmnopqrstuvwxyz" or char in "0123456789"
	def is_operator(self, char):
		return char == '*' or char == '|' or char == "." or char == "?" or char == "+"
	def one_operand_operator(self, char):
		return char == '*' or char == "?" or char == "+"
	def build(self, expr):
		stack = Stack()
		for symbol in expr:
			if symbol == " ":
				continue
			if self.is_operand(symbol):
				n = Node(symbol)
				n.symbol = symbol
				stack.push(n)
			if self.is_operator(symbol):
				if self.one_operand_operator(symbol):
					t1 = stack.pop()
					n  = Node(symbol)
					n.symbol = symbol
					n.left = t1
					stack.push(n)
				else:
					t1 = stack.pop()
					t2 = stack.pop()
					n  = Node(symbol)
					n.symbol = symbol
					n.left = t2
					n.right = t1
					stack.push(n)
		self.root = stack.pop()
		self.root.enumerate()
		return self.root
	def most_left_node(self):
		return self.root.most_left_node()

	def costura(self):
		self.root.costura()

class Node:

	def __init__(self, symbol, left=None, right=None):
		self.left = left
		self.right = right
		self.symbol = symbol
		self.label = -1
		self.traversal = []
		self.costura_node = None
		self.isThreaded = False
	def __lt__(self, other):
		return self.label < other.label
	def __le__(self, other):
		return self.label <= other.label
	'''def __ne__(self, other):
		return self.__hash__() != other.__hash__()'''
	def __ge__(self, other):
		return self.label >= other.label
	def __gt__(self, other):
		return self.label > other.label
	'''def __eq__(self, other):
		return self.__hash__() == other.__hash__()'''
	def __hash__(self):
		hashable = str(self.label) + " "
		if self.symbol == 'α':
			hashable += 'lambda'
		elif self.symbol == ' φ':
			hashable += ' φ'
		else:
			hashable += self.symbol
		sigma = 0
		i = 1
		for c in hashable:
			sigma += ord(c) * i
			i += 1
		return sigma
	def set_left(self, left):
		self.left = left
	def set_right(self, right):
		self.right = right
	def __str__(self):
		return str(self.label) + " " + self.symbol
	def __repr__(self):
		return self.__str__()
	def most_left_node(self):
		if self.left is None:
			return self
		else:
			return self.left.most_left_node()
	def enumerate(self):
		leaves = (self.get_leaf_nodes())
		#print("leaves: " + str(self.get_leaf_nodes()))
		i = 1
		for leaf in leaves:
			leaf.label = i
			i+=1


	def in_order(self):
		if self.left is not None:
			self.traversal.extend=(self.left.in_order())

		self.traversal.append=(self)
		if self.right is not None:
			self.traversal.extend=(self.right.in_order())

		ret = self.traversal
		self.traversal = []
		return (ret)

	def costura(self):
		in_order_nodes = self.in_order()
		iter_ = iter(in_order_nodes)
		next(iter_)
		n = None
		for node in in_order_nodes:
			try:
				n = next(iter_)
			except:
				#print(str(node.symbol), end="")
				#print(" costura para lambda")
				node.costura_node = Node('α')
				return
			if node.symbol == "." or node.symbol == "|":
				continue
			#print(str(node.symbol) + " costura para ", end="")
			#print(n.symbol)
			node.costura_node = n
		self.isThreaded = True

	def handle_leaf(self):
		if not self.is_leaf():
			return set()
		node_composition = set()
		visited_down = set()
		visited_up = set()
		if self.costura_node.symbol == 'α':
			node_composition |= {self.costura_node}
		if self.costura_node.symbol == ".":
			node_composition |= (self.handle_concatenation(self.costura_node, UP, visited_down, visited_up))
		if self.costura_node.symbol == "?":
			node_composition |= (self.handle_optional(self.costura_node, UP, visited_down, visited_up))
		if self.costura_node.symbol == "*":
			node_composition |= self.handle_star(self.costura_node, DOWN, visited_down, visited_up)
			node_composition |= (self.handle_star(self.costura_node, UP, visited_down, visited_up))
		if self.costura_node.symbol == "|":
			node_composition = self.handle_union(self.costura_node, UP, visited_down, visited_up)
		if self.costura_node.symbol == "+":
			node_composition |= self.handle_plus(self.costura_node, DOWN, visited_down, visited_up)
			node_composition |= (self.handle_plus(self.costura_node, UP, visited_down, visited_up))

		return node_composition

	def handle_optional(self, node, action, visited_down=set(), visited_up=set()):
		if node in visited_down and action == DOWN:
			return set()
		if node in visited_up and action == UP:
			return set()
		node_composition = set()
		pend=encies = Stack()
		if action == DOWN:
			visited_down.add(node)
			if node.left.is_leaf():
				node_composition |= {node.left}
			if node.left.symbol == ".":
				node_composition |= node.handle_concatenation(node.left, DOWN, visited_down, visited_up)
			if node.left.symbol == "*":
				node_composition |= node.handle_star(node.left, DOWN, visited_down, visited_up)
				node_composition |= node.handle_star(node.left, UP, visited_down, visited_up)
			if node.left.symbol == "?":
				node_composition |= node.handle_optional(node.left, DOWN, visited_down, visited_up)
				node_composition |= node.handle_optional(node.left, UP, visited_down, visited_up)
			if node.left.symbol == "|":
				node_composition |= node.handle_union(node.left, DOWN, visited_down, visited_up)
			if node.left.symbol == "+":
				node_composition |= node.handle_plus(node.left, DOWN, visited_down, visited_up)
		if action == UP:
			visited_up.add(node)
			if node.costura_node.symbol == 'α':
				node_composition |= {node.costura_node}
			if node.costura_node.symbol == "*":
				node_composition |= node.handle_star(node.costura_node, DOWN, visited_down, visited_up)
				node_composition |= node.handle_star(node.costura_node, UP, visited_down, visited_up)
				#pend=encies.push(Pend=ency(node.costura_node, UP))
			if node.costura_node.symbol == ".":
				node_composition |= node.handle_concatenation(node.costura_node, UP, visited_down, visited_up)
			if node.costura_node.symbol == "?":
				node_composition |= node.handle_optional(node.costura_node, UP, visited_down, visited_up)
			if node.costura_node.symbol == "|":
				node_composition |= node.handle_union(node.costura_node, UP, visited_down, visited_up)
			if node.costura_node.symbol == "+":
				node_composition |= node.handle_plus(node.costura_node, DOWN, visited_down, visited_up)
				node_composition |= node.handle_plus(node.costura_node, UP, visited_down, visited_up)

		return node_composition
	def handle_concatenation(self, node, action, visited_down=set(), visited_up=set()):
		if node in visited_down and action == DOWN:
			return set()
		if node in visited_up and action == UP:
			return set()
		node_composition = set()
		pend=encies = Stack()
		if action == UP:
			visited_up.add(node)
			if node.right.is_leaf():
				node_composition.add(node.right)
			elif node.right.symbol == "*":
				node_composition |= node.handle_star(node.right, DOWN, visited_down, visited_up)
				node_composition |= node.handle_star(node.right, UP,  visited_down, visited_up)
			elif node.right.symbol == ".":
				node_composition |= node.handle_concatenation(node.right, DOWN,  visited_down, visited_up)
			elif node.right.symbol == "?":
				node_composition |= node.handle_optional(node.right, DOWN,  visited_down, visited_up)
				node_composition |= node.handle_optional(node.right, UP,  visited_down, visited_up)
			elif node.right.symbol == "|":
				node_composition |= node.handle_union(node.right, DOWN,  visited_down, visited_up)
			elif node.right.symbol == "+":
				node_composition |= node.handle_plus(node.right, DOWN,  visited_down, visited_up)
		if action == DOWN:
			visited_down.add(node)
			if node.left.is_leaf():
				node_composition.add(node.left)
			elif node.left.symbol == ".":
				node_composition |= node.handle_concatenation(node.left, DOWN, visited_down,visited_up)
			elif node.left.symbol == "*":
				node_composition |=  node.handle_star(node.left, DOWN, visited_down, visited_up)
				node_composition |=  node.handle_star(node.left, UP, visited_down, visited_up)
				#pend=encies.push(Pend=ency(node.left), UP)
			elif node.left.symbol == "?":
				node_composition |=  node.handle_optional(node.left, DOWN, visited_down, visited_up)
				node_composition |=  node.handle_optional(node.left, UP, visited_down, visited_up)
				#pend=encies.push(Pend=ency(node.left), UP)
			elif node.left.symbol == "|":
				node_composition |= node.handle_union(node.left, DOWN, visited_down,visited_up)
			elif node.left.symbol == "+":
				node_composition |= node.handle_plus(node.left, DOWN, visited_down,visited_up)
		################################3
		################################3
				#if p.node.symbol ==


		return node_composition
	def handle_star(self, node, action, visited_down=set(), visited_up=set()):
		if node in visited_down and action == DOWN:
			return set()
		if node in visited_up and action == UP:
			return set()
		pend=encies = Stack()
		node_composition = set()
		if action == DOWN:
			visited_down.add(node)
			if node.left.is_leaf():
				node_composition.add(node.left)
			elif node.left.symbol == ".":
				node_composition |= node.handle_concatenation(node.left, DOWN,  visited_down, visited_up)
			elif node.left.symbol == "?":
				node_composition |= node.handle_optional(node.left, DOWN, visited_down, visited_up)
				node_composition |= node.handle_optional(node.left, UP,visited_down, visited_up)
				#pend=encies.push(node.left, UP)
			elif node.left.symbol == "*":
				node_composition |= node.handle_star(node.left, DOWN, visited_down, visited_up)
				node_composition |= node.handle_star(node.left, UP,  visited_down, visited_up)
			elif node.left.symbol == "|":
				node_composition |= node.handle_union(node.left, DOWN,  visited_down, visited_up)
			elif node.left.symbol == "+":
				node_composition |= node.handle_plus(node.left, DOWN,  visited_down, visited_up)
		if action == UP:
			visited_up.add(node)
			if node.costura_node.symbol == 'α':
				node_composition |= {node.costura_node}
			if node.costura_node.symbol == ".":
				node_composition |= node.handle_concatenation(node.costura_node, UP, visited_down, visited_up)
			elif node.costura_node.symbol == "?":
				node_composition |= node.handle_optional(node.costura_node, UP,  visited_down, visited_up)
				#pend=encies.push(node.left, UP)
			elif node.costura_node.symbol == "*":
				node_composition |= node.handle_star(node.costura_node, DOWN,visited_down, visited_up)
				node_composition |= node.handle_star(node.costura_node, UP,  visited_down, visited_up)
			elif node.costura_node.symbol == "|":
				node_composition |= node.handle_union(node.costura_node, UP, visited_down, visited_up)
			elif node.costura_node.symbol == "+":
				node_composition |= node.handle_plus(node.costura_node, DOWN,visited_down, visited_up)
				node_composition |= node.handle_plus(node.costura_node, UP,  visited_down, visited_up)
		return node_composition
	def handle_union(self, node, action, visited_down=set(), visited_up=set()):

		if node in visited_down and action == DOWN:
			return set()
		if node in visited_up and action == UP:
			return set()
		node_composition = set()
		if action == UP:
			visited_up.add(node)
			right_most = node.right_most_node()
			if right_most.costura_node.symbol == "*":
				node_composition |= right_most.handle_star(right_most.costura_node, DOWN, visited_down, visited_up)
				node_composition |= right_most.handle_star(right_most.costura_node, UP, visited_down, visited_up)
			elif right_most.costura_node.symbol == ".":
				node_composition |= right_most.handle_concatenation(right_most.costura_node, UP,visited_down, visited_up)
			elif right_most.costura_node.symbol == "?":
				#node_composition |= right_most.handle_optional(right_most.costura_node, DOWN)
				node_composition |= right_most.handle_optional(right_most.costura_node, UP,visited_down,\
				 visited_up)
			elif right_most.costura_node.symbol == "α":
				node_composition |= {right_most.costura_node}
			elif right_most.costura_node.symbol == "|":
				node_composition |= right_most.handle_union(right_most.costura_node, UP,visited_down, visited_up)
			elif right_most.costura_node.symbol == "+":
				node_composition |= right_most.handle_plus(right_most.costura_node, DOWN, visited_down, visited_up)
				node_composition |= right_most.handle_plus(right_most.costura_node, UP, visited_down, visited_up)
		if action == DOWN:
			visited_down.add(node)
			print("nodo = " + str(node))
			if node.left.is_leaf():
				node_composition |= {node.left}
			if node.right.is_leaf():
				node_composition |= {node.right}
			if node.left.symbol == ".":
				node_composition |= node.handle_concatenation(node.left, DOWN, visited_down, visited_up)
			if node.left.symbol == "|":
				node_composition |= node.handle_union(node.left, DOWN, visited_down, visited_up)
			if node.left.symbol == "*":
				node_composition |= node.handle_star(node.left, DOWN, visited_down, visited_up)
				node_composition |= node.handle_star(node.left, UP, visited_down, visited_up)
			if node.left.symbol == "?":
				node_composition |= node.handle_optional(node.left, DOWN, visited_down, visited_up)
				node_composition |= node.handle_optional(node.left, UP, visited_down, visited_up)
			if node.left.symbol == "+":
				node_composition |= node.handle_plus(node.left, DOWN, visited_down, visited_up)

			if node.right.symbol == ".":
				node_composition |= node.handle_concatenation(node.right, DOWN, visited_down, visited_up)
			if node.right.symbol == "|":
				node_composition |= node.handle_union(node.right, DOWN, visited_down, visited_up)
			if node.right.symbol == "*":
				node_composition |= node.handle_star(node.right, DOWN, visited_down, visited_up)
				node_composition |= node.handle_star(node.right, UP, visited_down, visited_up)
			if node.right.symbol == "?":
				node_composition |= node.handle_optional(node.right, DOWN, visited_down, visited_up)
				node_composition |= node.handle_optional(node.right, UP, visited_down, visited_up)
			if node.right.symbol == "+":
				node_composition |= node.handle_plus(node.right, DOWN, visited_down, visited_up)
		return node_composition

	def handle_plus(self, node, action, visited_down=set(), visited_up=set()):
		if node in visited_down and action == DOWN:
			return set()
		if node in visited_up and action == UP:
			return set()
		pend=encies = Stack()
		node_composition = set()
		if action == DOWN:
			visited_down.add(node)
			if node.left.is_leaf():
				node_composition.add(node.left)
			elif node.left.symbol == ".":
				node_composition |= node.handle_concatenation(node.left, DOWN,  visited_down, visited_up)
			elif node.left.symbol == "?":
				node_composition |= node.handle_optional(node.left, DOWN, visited_down, visited_up)
				node_composition |= node.handle_optional(node.left, UP,visited_down, visited_up)
				#pend=encies.push(node.left, UP)
			elif node.left.symbol == "*":
				node_composition |= node.handle_star(node.left, DOWN, visited_down, visited_up)
				node_composition |= node.handle_star(node.left, UP,  visited_down, visited_up)
			elif node.left.symbol == "|":
				node_composition |= node.handle_union(node.left, DOWN,  visited_down, visited_up)
			elif node.left.symbol == "+":
				node_composition |= node.handle_plus(node.left, DOWN,  visited_down, visited_up)
		if action == UP:
			visited_up.add(node)
			if node.costura_node.symbol == 'α':
				node_composition |= {node.costura_node}
			if node.costura_node.symbol == ".":
				node_composition |= node.handle_concatenation(node.costura_node, UP, visited_down, visited_up)
			elif node.costura_node.symbol == "?":
				node_composition |= node.handle_optional(node.costura_node, UP,  visited_down, visited_up)
				#pend=encies.push(node.left, UP)
			elif node.costura_node.symbol == "*":
				node_composition |= node.handle_star(node.costura_node, DOWN,visited_down, visited_up)
				node_composition |= node.handle_star(node.costura_node, UP,  visited_down, visited_up)
			elif node.costura_node.symbol == "|":
				node_composition |= node.handle_union(node.costura_node, UP, visited_down, visited_up)
			elif node.costura_node.symbol == "+":
				node_composition |= node.handle_plus(node.costura_node, DOWN,visited_down, visited_up)
				node_composition |= node.handle_plus(node.costura_node, UP,  visited_down, visited_up)
		return node_composition
	def post_order(self):

		if self.left is not None:
			self.traversal.append=(self.left.post_order())
		if self.right is not None:
			self.traversal.append=(self.right.post_order())
		traversal.append=(self.symbol)
		ret = self.traversal
		self.traversal = []
		return (ret)
	def pre_order(self):
		traversal.append=(self.symbol)
		if self.left is not None:
			self.traversal.append=(self.left.post_order())
		if self.right is not None:
			self.traversal.append=(self.right.post_order())
		ret = self.traversal
		self.traversal = []
		return (ret)
	def get_leaf_nodes(self):
		if self.is_leaf():
			self.traversal.append=(self)
		if self.left is not None:
			self.traversal.extend=(self.left.get_leaf_nodes())
		if self.right is not None:
			self.traversal.extend=(self.right.get_leaf_nodes())
		ret = self.traversal
		self.traversal = []
		return (ret)
	def is_leaf(self):
		return self.right is None and self.left is None

	def right_most_node(self):
		if self.right is not None:
			return self.right.right_most_node()
		else:
			return self
	def handle_root(self):
		visited_up = set()
		visited_down = set()
		node_composition = set()
		if self.is_leaf():
			node_composition |= {self.costura_node}
		if self.symbol == '|':
			if self.right.is_leaf():
				node_composition |= {self.left}
			if self.right.symbol == '*':
				node_composition |= self.handle_star(self.right, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.right, UP, visited_down ,visited_up)
			if self.right.symbol == "|":
				node_composition |= self.handle_union(self.right, DOWN, visited_down, visited_up)
			if self.right.symbol == "?":
				node_composition |= self.handle_optional(self.right,DOWN,visited_down, visited_up)
				node_composition |= self.handle_optional(self.right,UP, visited_down,visited_up)
			if self.right.symbol == ".":
				node_composition |= self.handle_concatenation(self.right,DOWN, visited_down ,visited_up)
			if self.right.symbol == "+":
				node_composition |= self.handle_plus(self.right,DOWN, visited_down ,visited_up)

			if self.left.is_leaf():
				node_composition |= {self.left}
			if self.left.symbol == '*':
				node_composition |= self.handle_star(self.left, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.left, UP, visited_down ,visited_up)
			if self.left.symbol == "|":
				node_composition |= self.handle_union(self.left, DOWN, visited_down, visited_up)
			if self.left.symbol == "?":
				node_composition |= self.handle_optional(self.left,DOWN,visited_down, visited_up)
				node_composition |= self.handle_optional(self.left,UP, visited_down,visited_up)
			if self.left.symbol == ".":
				node_composition |= self.handle_concatenation(self.left,DOWN, visited_down ,visited_up)
			if self.left.symbol == "+":
				node_composition |= self.handle_plus(self.left,DOWN, visited_down ,visited_up)
		if self.symbol == ".":
			if self.left.is_leaf():
				node_composition |= {self.left}
			if self.left.symbol == '*':
				node_composition |= self.handle_star(self.left, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.left, UP, visited_down ,visited_up)
			if self.left.symbol == "|":
				node_composition |= self.handle_union(self.left, DOWN, visited_down, visited_up)
			if self.left.symbol == "?":
				node_composition |= self.handle_optional(self.left,DOWN,visited_down, visited_up)
				node_composition |= self.handle_optional(self.left,UP, visited_down,visited_up)
			if self.left.symbol == ".":
				node_composition |= self.handle_concatenation(self.left,DOWN, visited_down ,visited_up)
			if self.left.symbol == "+":
				node_composition |= self.handle_plus(self.left,DOWN, visited_down ,visited_up)

		if self.symbol == "*":
			if self.left.is_leaf():
				node_composition |= {self.left}
			if self.left.symbol == '*':
				node_composition |= self.handle_star(self.left, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.left, UP, visited_down ,visited_up)
			if self.left.symbol == "|":
				node_composition |= self.handle_union(self.left, DOWN, visited_down, visited_up)
			if self.left.symbol == "?":
				node_composition |= self.handle_optional(self.left,DOWN,visited_down, visited_up)
				node_composition |= self.handle_optional(self.left,UP, visited_down,visited_up)
			if self.left.symbol == ".":
				node_composition |= self.handle_concatenation(self.left,DOWN, visited_down ,visited_up)
			if self.left.symbol == "+":
				node_composition |= self.handle_plus(self.left,DOWN, visited_down ,visited_up)

			if self.costura_node is not None:
				node_composition |= {self.costura_node}

		if self.symbol == "?":
			if self.left.is_leaf():
				node_composition |= {self.left}
			if self.left.symbol == '*':
				node_composition |= self.handle_star(self.left, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.left, UP, visited_down ,visited_up)
			if self.left.symbol == "|":
				node_composition |= self.handle_union(self.left, DOWN, visited_down, visited_up)
			if self.left.symbol == "?":
				node_composition |= self.handle_optional(self.left,DOWN,visited_down, visited_up)
				node_composition |= self.handle_optional(self.left,UP, visited_down,visited_up)
			if self.left.symbol == ".":
				node_composition |= self.handle_concatenation(self.left,DOWN, visited_down ,visited_up)
			if self.left.symbol == "+":
				node_composition |= self.handle_plus(self.left,DOWN, visited_down ,visited_up)

			if self.costura_node is not None:
				node_composition |= {self.costura_node}

		if self.symbol == "+":
			if self.left.is_leaf():
				node_composition |= {self.left}
			if self.left.symbol == '*':
				node_composition |= self.handle_star(self.left, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.left, UP, visited_down ,visited_up)
			if self.left.symbol == "|":
				node_composition |= self.handle_union(self.left, DOWN, visited_down, visited_up)
			if self.left.symbol == "?":
				node_composition |= self.handle_optional(self.left,DOWN,visited_down, visited_up)
				node_composition |= self.handle_optional(self.left,UP, visited_down,visited_up)
			if self.left.symbol == ".":
				node_composition |= self.handle_concatenation(self.left,DOWN, visited_down ,visited_up)
			if self.left.symbol == "+":
				node_composition |= self.handle_plus(self.left,DOWN, visited_down ,visited_up)

		return node_composition

def normalize(regex):
    last = ' '
    new = ''
    for s in regex:
        if s == ' ' and last == ' ':
            continue
        elif s == ' ' and last != ' ':
            new += s
            last = s
            continue
        elif s != ' ' and last != ' ':
            new += ' ' + s
            last = s
            continue
        else:
            new += s
            last = s
    print(new)
    last = ' '
    new2 = ''
    for n in new:
        if n == ' ':
            new2 += n
            continue
        isdigit = n.lower() in "abcdefghijklmnopqrstuvwxyz" or n in "0123456789" or n == "("
        islastdigit = last.lower() in "abcdefghijklmnopqrstuvwxyz" or last in "0123456789" or last == ")"
        if isdigit and islastdigit:
            new2 += '. ' + n
        else:
            new2 += n
        if n not in "?*+":
            last = n
    print("new2 = " +new2)
    for n2 in new2:
        if n2 in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            n2 = n2.lower()
    if len(new2) == 1:
    	new2 = new2 + " | " + new2
    return new2



class RegExp:
	BRACKETS_ERROR = 1
	EXPR_NOT_WELL_FORMED = 2
	UNKNOWN = -1
	OK = 0
	def __init__(self, regex):
		self.test_regex = regex
		regex = normalize(regex)
		self.regex = regex

	def get_compositions_from(self, compositions, symbol):
		for c in compositions:
			print()
	def parse(self):
		t = Tree()
		alphabet = set()
		nodo = t.build(polish_notation(self.regex))
		t.costura()
		display(nodo, 1)
		leaves = nodo.get_leaf_nodes()
		states_counter = 0
		compositions = {}
		states_compositions = {}
		states = set()
		for leaf in leaves:
			compositions[leaf] = sorted(leaf.handle_leaf())
			alphabet.add(leaf.symbol)
		error = Node(' φ')
		error.label = -2
		compositions[error] = {error}
		q0_composition = sorted(nodo.handle_root())

		return (compositions, q0_composition, alphabet, error)
	def handle_composition(self, composition, compositions, s):
		'''composição pelo símbolo s'''
		ret = set()
		if not composition:
			return
		for c in composition:
			''' label = -1 é o caso do lambda'''
			if c.label == -1:
				continue
			if c.symbol == s:
				ret = ret | set(compositions[c])
		''' ret is empty? if so, return None '''
		if not ret:
			return None
		return sorted(ret)

	def to_automaton(self):
		ret = self.parse()
		compositions = ret[0]
		q0_composition = set(sorted(list(ret[1]), key=lambda node: node.label))
		alphabet = list(ret[2])
		error = ret[3]
		unvisited = [q0_composition]
		visited = []
		trans = []
		while len(unvisited) != 0:
			comp = unvisited.pop(0)
			if comp not in visited:
				visited.append=(comp)
			for s in alphabet:
				nextc = self.handle_composition(comp, compositions, s)
				if nextc is None:
					nextc = compositions[error]
				print(comp)
				comp = set(sorted(list(comp), key=lambda node: node.label))
				print(comp)
				print(nextc)
				nextc = set(sorted(list(nextc), key=lambda node: node.label))
				print(nextc)
				trans.append=([comp, s, nextc])
				print(str(comp) + " vai para " + str(nextc) + " por " + str(s))
				if nextc not in unvisited and nextc not in visited:
					unvisited.append=(nextc)
		print(trans)
		states = []
		finalStates = []
		for v in visited:
			accpt = False
			for c in v:
				if c.label == -1:
					accpt = True
			state = State(str(v), accpt)
			states.append=(state)
			if state.isAcceptance:
				finalStates.append=(state)
			if state.name == str(q0_composition):
				initialState = state
				#if 'α' self.symbols_of_a_composition(q0_composition):
				#	initialState.isAcceptance = True
		print("=============")
		print(trans)
		for s in states:
			#print("ha")
			for s1 in states:
				for t in trans:
					if s.name == str(t[0]) and s1.name == str(t[2]):
						print("1")
						s.add_transition(Transition(t[1], s1))
						#print("adicionando " + str(t))

		''' φ = State(' φ', False)
		for symbol in alphabet:
			t = Transition(symbol,  φ)
			 φ.transitions.append=(t)
		add_ φ = False
		for s in states:
			for lack_symbol in (set(alphabet) - self.symbols_of_a_composition(s.name)):
				s.add_transition(Transition(lack_symbol,  φ))
				add_ φ = True
		if add_ φ:
			states.append=( φ)'''

		result_automaton = Automaton(states, finalStates, initialState, alphabet)
		result_automaton.equi_classes = [result_automaton.get_acceptance_states(), result_automaton.get_non_acceptance_states()]

		#print(states)
		return result_automaton
	def symbols_of_a_composition(self, comp_str):
		symbols = set()
		comp_str = comp_str.replace("{","")
		comp_str = comp_str.replace("}","")
		comp_str_list_symbol = comp_str.split(",")
		for ss in comp_str_list_symbol:
			symbols.add(ss.split()[1])

		return symbols

	def isValid(self):
		import re
		#self.test_regex = self.test_regex.replace(" ", "")
		print(self.test_regex)
		re = re.compile(r'[(]?[a-z0-9]+([?+*]?([)][?+*]?)?)([|]?[(]?[a-z0-9]+([?+*]?([)][?+*]?[)]?)?))*')
		match = re.match(self.test_regex)
		return RegExp.OK
		if match is None:
			return RegExp.OK
		if (self.test_regex.count("(") != self.test_regex.count(")")):
			return RegExp.BRACKETS_ERROR
		try :
			if (match.group() == self.test_regex):
				return RegExp.OK
			else:
				return RegExp.EXPR_NOT_WELL_FORMED
		except AttributeError:
			return RegExp.UNKNOWN

class StateComposition:

	def __init__(self, state_composition, alphabet):
		self.state_composition = state_composition
		self.symbol_composition = {}

		for symbol in alphabet:
			self.symbol_composition[symbol] = self.get_compositions_from_symbol(symbol, self.state_composition)

	def get_compositions_from_symbol(self, symbol, composition):
		for tc in composition:
			ret = []
			if tc.symbol == symbol:
				ret.append=(tc)

		return ret
	def __hash__(self):
		return 1

def display(root, level):
	if root is None:
		for i in range(0, level):
			print("\t", end="")
		print("=")
		return
	display(root.right, level+1)

	for i in range(0, level):
		print("\t", end="")
	if root.is_leaf():
		print(str(root.label) + root.symbol)
	else:
		print(root.symbol)
	display(root.left, level+1)
