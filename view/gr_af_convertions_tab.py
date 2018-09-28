import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import functools
sys.path.append('../')
from globals import *
import regular_grammar
import non_deterministic_automaton
from regular_grammar import Grammar, Production
import deterministic_automaton

'''
	Autoria: Adriano Tosetto, Giulio Simão
'''

class ConvertionTab(QWidget):
	updateAF = QtCore.pyqtSignal(non_deterministic_automaton.NDAutomaton)
	updateGR = QtCore.pyqtSignal(Grammar)
	def __init__(self):
		super(QWidget, self).__init__(parent=None)
		self.convert_gr_af_layout = QGridLayout()
		self.convert_af_gr_layout = QGridLayout()
		self.convert_gr_af_panel = QWidget()
		self.convert_af_gr_panel = QWidget()

		self.gr_name = QLineEdit()
		self.af_name = QLineEdit()

		self.gr_convert = QPushButton("Converter para AF")
		self.af_convert = QPushButton("Converter para GR")

		self.main_layout = QGridLayout()

		self.set_click_events()

		self.set_policy_buttons()

		self.set_panels()


	def set_panels(self):
		self.convert_gr_af_layout.addWidget(self.gr_name)
		self.convert_gr_af_layout.addWidget(self.gr_convert)

		self.convert_af_gr_layout.addWidget(self.af_name)
		self.convert_af_gr_layout.addWidget(self.af_convert)

		self.convert_gr_af_panel.setLayout(self.convert_gr_af_layout)
		self.convert_af_gr_panel.setLayout(self.convert_af_gr_layout)

		self.main_layout.addWidget(self.convert_af_gr_panel)
		self.main_layout.addWidget(self.convert_gr_af_panel)

		self.setLayout(self.main_layout)
	def set_policy_buttons(self):
		self.gr_convert.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.af_convert.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.gr_name.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.af_name.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
	def set_click_events(self):
		self.gr_convert.clicked.connect(self.convert_to_af)
		self.af_convert.clicked.connect(self.convert_to_gr)

	def convert_to_af(self):
		a_1 = None
		for a1 in Globals.grammars:
			if a1.name == self.gr_name.text():
				a_1 = a1
		if a_1 != None:
			newA = a_1.convert_to_automaton()
			newA.name = "M"
			while newA in Globals.automata:
				newA.name = newA.name + "'"
			newA.name = newA.name + " | T(" + newA.name + ") = L(" + a_1.name + ")"
			while newA in Globals.automata:
				newA.name = newA.name + "'"
			Globals.automata.append=(newA)
			Globals.selected = newA
			self.updateAF.emit(Globals.selected)
	def convert_to_gr(self):
		a_1 = None
		for a1 in Globals.automata:
			if a1.name == self.af_name.text():
				a_1 = a1
		if type(a_1) != type(deterministic_automaton.Automaton({},{},deterministic_automaton.State(""))):
			if type(a_1) == type(non_deterministic_automaton.NDAutomaton({},{}, non_deterministic_automaton.NDState(""))):
				a_1 = a_1.determinize()
			else:
				return
		if a_1 != None:
			newA = a_1.to_grammar()
			newA.name = "G"
			while newA in Globals.grammars:
				newA.name = newA.name + "'"
			newA.name = newA.name + " | L(" + newA.name + ") = T(" + a_1.name + ")"
			while newA in Globals.grammars:
				newA.name = newA.name + "'"
			Globals.grammars.append=(newA)
			Globals.selected = newA
			#print(newA)
			self.updateGR.emit(Globals.selected)
