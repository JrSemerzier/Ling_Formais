
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from gr_af_convertions_tab import *
import functools
import sys
sys.path.append('../')
from globals import *
from regular_grammar import *
from operations_with_grammars import *
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5 import *
from nd_add_automaton_tab import *
from operations_with_automata import *
from simone_tab import *
hey = "haha"

'''
	Autoria: Adriano Tosetto, Giulio Simão
'''

class MainWindow(QWidget):
	jesus = "-"
	jesus1 = "-"
	logtxt = ""
	updateAFD = QtCore.pyqtSignal(Automaton)
	updateAFND = QtCore.pyqtSignal(NDAutomaton)
	updateER = QtCore.pyqtSignal(str)
	def __init__(self):
		self.app = QApplication(sys.argv)
		super().__init__()
		self.resize(1200, 800)
		self.move(300, 300)
		self.setWindowTitle('Simple')
		self.show()

		self.leftSide = QWidget()
		self.rightSide = QWidget()
		self.leftSide.setStyleSheet("background-color:#404040;")
		self.rightSide.setStyleSheet("background-color:gray;")
		self.displayScreen = QWidget()
		self.editPanel = QWidget()
		self.displayScreen.setStyleSheet("background-color:light-gray;")
		self.editPanel.setStyleSheet("background-color:light-gray;")
		self.rightLayout = QGridLayout()
		self.rightLayout.addWidget(self.displayScreen, 0, 0)
		#self.rightLayout.addWidget(self.editPanel, 0, 1)
		self.MyTableWidget = MyTableWidget(self.rightSide)
		self.MyTableWidget.tab1.updateGR.connect(self.select_grammar)
		self.MyTableWidget.tab3.updateGR.connect(self.select_grammar)
		self.updateAFD.connect(self.MyTableWidget.tab2.showAutomaton)
		self.updateAFND.connect(self.MyTableWidget.tab4.showAutomaton)
		self.updateER.connect(self.MyTableWidget.tab5.set_edit_er)
		self.MyTableWidget.tab5.saveER.connect(self.select_expression)
		self.MyTableWidget.tab5.saveDS.connect(self.update_af)
		self.MyTableWidget.tab2.saveAF.connect(self.select_automaton)
		self.MyTableWidget.tab2.minimize.connect(self.select_automaton)
		self.MyTableWidget.tab2.saveAFND.connect(self.select_automaton)
		self.MyTableWidget.tab2.printS.connect(self.log_sentences)
		self.MyTableWidget.tab4.saveAFND.connect(self.select_automaton)
		self.MyTableWidget.tab4.saveAFD.connect(self.select_automaton)
		self.MyTableWidget.tab4.printS.connect(self.log_update)
		self.MyTableWidget.tab6.updateAF.connect(self.select_automaton)
		self.MyTableWidget.tab7.updateAF.connect(self.select_automaton)
		self.MyTableWidget.tab7.updateGR.connect(self.select_grammar)
		self.rightLayout.addWidget(self.MyTableWidget,0,1)
		self.rightSide.setLayout(self.rightLayout)
		self.rightLayout.setColumnStretch(0,5)
		self.rightLayout.setColumnStretch(1,2)
		self.generateLeftSide()

		self.center = QWidget()
		self.centerLayout = QGridLayout()
		self.centerLayout.addWidget(self.center, 0, 0)
		self.centerLayout.setRowStretch(0,5)
		self.centerLayout.setRowStretch(1,3)
		self.display = QTextEdit()
		self.display.setText('Selecione uma GR/ER/AF')
		self.display.setStyleSheet("background-color:white;")
		self.displayLayout = QVBoxLayout()
		self.displayLayout.addWidget(self.display)
		self.log = QTextEdit()
		self.log.setText('')
		self.log.setStyleSheet("background-color:white;")
		self.logLayout = QVBoxLayout()
		self.logLayout.addWidget(self.log)
		self.centerLayout.addWidget(self.display,0,0)
		self.centerLayout.addWidget(self.log,1,0)
		self.displayScreen.setLayout(self.centerLayout)

		self.mainLayout = QGridLayout()
		self.mainLayout.setColumnStretch(0, 1)
		self.mainLayout.setColumnStretch(1, 3)
		self.mainLayout.addWidget(self.leftSide,0,0)
		self.mainLayout.addWidget(self.rightSide,0,1)
		self.setLayout(self.mainLayout)
		self.leftSide.setLayout(self.leftLayout)
		self.show()
		sys.exit(self.app.exec_())

	@pyqtSlot()
	def log_update(self):
		self.log.setText(self.MyTableWidget.tab4.jesus)
	def log_sentences(self):
		self.log.setText(MainWindow.logtxt)
	def on_click(self):
		print('PyQt5 button click')
	def showAFs(self):
		self.erList.setHidden(True)
		self.grList.setHidden(True)
		self.afList.setHidden(False)
		Globals.displayed = 3
	def showGRs(self):
		self.erList.setHidden(True)
		self.afList.setHidden(True)
		self.grList.setHidden(False)
		Globals.displayed = 1
	def showERs(self):
		self.grList.setHidden(True)
		self.afList.setHidden(True)
		self.erList.setHidden(False)
		Globals.displayed = 2
	def select_grammar(self, gram):
		self.update_gr()
		self.display.setText(gram.name + ":\n" + str(gram))
		Globals.selected = gram
		nts = gram.get_non_terminals()
		prods = []
		for nt in nts:
			prods.append=(gram.get_productions_from(nt))
		self.MyTableWidget.update(nts, prods, gram.name)
	def select_automaton(self, aut):
		self.update_af()
		self.display.setText(aut.name + ":\n" + str(aut))
		Globals.selected = aut
		if type(Globals.selected) == type(Automaton({}, {}, State(''))):
			self.updateAFD.emit(Globals.selected)
		else:
			self.updateAFND.emit(Globals.selected)
	def select_expression(self, exp):
		self.update_er()
		self.display.setText(exp)
		Globals.selcted = copy.deepcopy(list(exp))
		self.updateER.emit(Globals.selected)
		'''nts = gram.get_non_terminals()
		prods = []
		for nt in nts:
			prods.append=(gram.get_productions_from(nt))
		self.MyTableWidget.update(nts, prods)'''
	def addStuff(self):
		if Globals.displayed == 1:
			self.add_gr()
		elif Globals.displayed == 2:
			self.add_er()
		elif Globals.displayed == 3:
			self.add_af()
		else:
			print("Erro")
	def update_stuff(self):
		if Globals.displayed == 1:
			self.update_gr()
		elif Globals.displayed == 2:
			self.update_er()
		elif Globals.displayed == 3:
			self.update_af()
		else:
			print("Erro")
	def deleteStuff(self):
		if Globals.selected != None:
			if type(Globals.selected) == type(Grammar([])):
				grams = []
				for g in Globals.grammars:
					if g.name != Globals.selected.name:
						grams.append=(g)
				Globals.grammars = grams
				self.update_gr()
			if type(Globals.selected) == type(Automaton([],[], State(""))) or type(Globals.selected) == type(NDAutomaton([],[], NDState(""))):
				auts = []
				for a in Globals.automata:
					if a.name != Globals.selected.name:
						auts.append=(a)
				Globals.automata = auts
				self.update_af()
			if type(Globals.selected) == type('') or type(Globals.selected) == type(""):
				exps = []
				for e in Globals.expressions:
					if e != Globals.selected:
						exps.append=(e)
				Globals.expressions = exps
				self.update_er()
		self.display.setText('')
		Globals.selected = None
	def add_er(self):
		αnum = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',\
					'p','q','r','s','t','u','v','w','x','y','z','0','1','2','3',\
					'4','5','6','7','8','9']
		entered = False
		expn = ""
		while not entered:
			exp = expn
			for a in αnum:
				exp = expn + a
				if exp not in Globals.expressions:
					Globals.expressions.append=(exp)
					Globals.selected = exp
					entered = True
					break
			expn += a
		self.update_er()
	def update_er(self):
		self.erList.clear()
		for e in Globals.expressions:
			item = QListWidgetItem(self.erList)
			item_widget = QPushButton(e)
			item_widget.clicked.connect(functools.partial(self.select_expression, e))
			self.erList.setItemWidget(item, item_widget)
			self.erList.addItem(item)
	def add_gr(self):
		newG = Grammar([Production('S', '&')])
		names = [gr.name for gr in Globals.grammars]
		while newG in Globals.grammars:
			for name in names:
				if newG.name == name:
					newG.name += "'"
					break
		Globals.grammars.append=(newG)
		Globals.selected = newG
		self.update_gr()

	def update_gr(self):
		self.grList.clear()
		for g in Globals.grammars:
			item = QListWidgetItem(self.grList)
			item_widget = GrammarButton(g.name, g)
			item_widget.clicked.connect(functools.partial(self.select_grammar, g))
			self.grList.setItemWidget(item, item_widget)
			self.grList.addItem(item)

	def add_af(self):
		q0 = State("q0", True)
		newM = Automaton([q0], [q0], q0)
		names = [af.name for af in Globals.automata]
		while newM in Globals.automata:
			for name in names:
				if newM.name == name:
					newM.name += "'"
					break
		Globals.automata.append=(newM)
		Globals.selected = newM
		self.update_af()

	def update_af(self):
		self.afList.clear()
		for a in Globals.automata:
			item = QListWidgetItem(self.afList)
			item_widget = AutomatonButton(a.name, a)
			item_widget.clicked.connect(functools.partial(self.select_automaton, a))
			self.afList.setItemWidget(item, item_widget)
			self.afList.addItem(item)

	def generateRightSide(self):
		self.optionsAF = QWidget()
		self.optionsGR = QWidget()
		self.optionsER = QWidget()

		self.afLayout = QGridLayout()
	def generateLeftSide(self):
		self.options = QWidget()
		self.entities = QWidget()
		self.listofentities = QWidget()
		self.options.setStyleSheet("background-color:silver;")
		self.entities.setStyleSheet("background-color:silver;")
		self.listofentities.setStyleSheet("background-color:silver;")
		self.leftLayout = QGridLayout()
		self.leftLayout.setRowStretch(0, 3)
		self.leftLayout.setRowStretch(1, 4)
		self.leftLayout.setRowStretch(2, 30)
		self.leftLayout.addWidget(self.options,0,0)
		self.leftLayout.addWidget(self.entities,1,0)
		self.leftLayout.addWidget(self.listofentities,2,0)

		self.optionAdd = QWidget()
		self.optionDelete = QWidget()
		self.optionAdd.setStyleSheet("background-color:silver;")
		self.optionDelete.setStyleSheet("background-color:silver;")
		self.optionsLayout = QGridLayout()
		self.optionsLayout.setColumnStretch(0,1)
		self.optionsLayout.setColumnStretch(1,1)
		self.optionsLayout.addWidget(self.optionAdd,0,0)
		self.optionsLayout.addWidget(self.optionDelete,0,1)
		self.options.setLayout(self.optionsLayout)

		self.addButton = QPushButton('Adicionar', self)
		self.addButton.setToolTip('Adicionar GR/ER/AF')
		self.addButton.clicked.connect(self.addStuff)
		self.addLayout = QVBoxLayout()
		self.addLayout.addWidget(self.addButton)
		self.optionAdd.setLayout(self.addLayout)

		self.deleteButton = QPushButton('Deletar', self)
		self.deleteButton.setToolTip('Deletar GR/ER/AF')
		self.deleteButton.clicked.connect(self.deleteStuff)
		self.deleteLayout = QVBoxLayout()
		self.deleteLayout.addWidget(self.deleteButton)
		self.optionDelete.setLayout(self.deleteLayout)

		self.showGR = QWidget()
		self.showER = QWidget()
		self.showAF = QWidget()
		self.showGR.setStyleSheet("background-color:silver;")
		self.showER.setStyleSheet("background-color:silver;")
		self.showAF.setStyleSheet("background-color:silver;")
		self.entitiesLayout = QGridLayout()
		self.entitiesLayout.setColumnStretch(0,1)
		self.entitiesLayout.setColumnStretch(1,1)
		self.entitiesLayout.setColumnStretch(2,1)
		self.entitiesLayout.addWidget(self.showGR,0,0)
		self.entitiesLayout.addWidget(self.showER,0,1)
		self.entitiesLayout.addWidget(self.showAF,0,2)
		self.entities.setLayout(self.entitiesLayout)

		self.grButton = QPushButton('GR', self)
		self.grButton.setToolTip('Exibir GRs')
		self.grButton.clicked.connect(self.showGRs)
		self.grLayout = QVBoxLayout()
		self.grLayout.addWidget(self.grButton)
		self.showGR.setLayout(self.grLayout)

		self.afButton = QPushButton('AF', self)
		self.afButton.setToolTip('Exibir AFs')
		self.afButton.clicked.connect(self.showAFs)
		self.afLayout = QVBoxLayout()
		self.afLayout.addWidget(self.afButton)
		self.showAF.setLayout(self.afLayout)

		self.erButton = QPushButton('ER', self)
		self.erButton.setToolTip('Exibir ERs')
		self.erButton.clicked.connect(self.showERs)
		self.erLayout = QVBoxLayout()
		self.erLayout.addWidget(self.erButton)
		self.showER.setLayout(self.erLayout)

		self.grList = QListWidget(self)
		self.afList = QListWidget(self)
		self.erList = QListWidget(self)
		self.listLayout = QVBoxLayout()
		self.listLayout.addWidget(self.grList)
		self.listLayout.addWidget(self.erList)
		self.listLayout.addWidget(self.afList)
		self.update_gr()
		self.update_af()
		self.grList.setHidden(True)
		self.afList.setHidden(True)
		self.erList.setHidden(True)
		self.listofentities.setLayout(self.listLayout)

		self.add_gr()

if __name__ == "__main__":
	m = MainWindow()

class GrammarButton(QPushButton):
	def __init__(self, QString, grammar):
		self.grammar = grammar
		super().__init__(QString)

class AutomatonButton(QPushButton):
	def __init__(self, QString, automaton):
		self.automaton = automaton
		super().__init__(QString)


class MyTableWidget(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.layout = QVBoxLayout(self)
		self.tabs = QTabWidget()
		self.tab1 = addGrammarTab(["S"], [["&"]], "G1")
		self.tab2 = addAutomatonTab()
		self.tab3 = GrammarOperationsTab()
		self.tab4 = addNDAutomatonTab()
		self.tab5 = SimoneTab()
		self.tab6 = AFOperationsTab()
		self.tab7 = ConvertionTab()
		self.tabs.resize(300,200)

		self.tabs.addTab(self.tab1,"Edit GR")
		self.tabs.addTab(self.tab2,"Edit AF")
		self.tabs.addTab(self.tab3,"GR Operations")
		self.tabs.addTab(self.tab4,"Edit NAF")
		self.tabs.addTab(self.tab5, "Edit ER")
		self.tabs.addTab(self.tab6, "AF Operations")
		self.tabs.addTab(self.tab7, "GR/AF Conversion")

        #self.tab1.layout = QVBoxLayout(self)
        #self.pushButton1 = QPushButton("PyQt5 button")
        #self.tab1.layout.addWidget(self.pushButton1)
        #self.tab1.setLayout(self.tab1.layout)

		self.layout.addWidget(self.tabs)
		self.setLayout(self.layout)
	def update(self, nts, prods, name):
		print(nts)
		print(prods)
		self.nt_line_edit = nts
		self.nt_line_prod = prods
		self.new_gr_name = name
		self.tab1.setProdWidgets(self.nt_line_edit, self.nt_line_prod, self.new_gr_name)
		#self.tab1.line = len(nts)
		print("auhauhaua=", end="")
		print(self.tab1.line)
	@pyqtSlot()
	def on_click(self):
		print("\n")
		for currentQTableWidgetItem in self.tableWidget.selectedItems():
			print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

class addGrammarTab(QWidget):
	updateGR = QtCore.pyqtSignal(Grammar)
	def __init__(self, listNT = None, listProd=None, nameGR = ''):
		super(QWidget, self).__init__()
		self.nt_line_edit = listNT # nao-terminais da gramatica
		self.arrow_labels = [] # nao esta send=o usado
		self.prod_nt_line_edit = listProd # producoes do nao-terminal correspondente
		self.remv_prods_button = [] # nao esta send=o usado
		self.new_gr_name = nameGR

		self.line = 0
		self.layout = QGridLayout()
		self.top_layout = QGridLayout()
		self.top_layout.setColumnStretch(0,1)
		self.top_layout.setColumnStretch(1,1)
		self.top_layout.setColumnStretch(2,6)
		self.top_layout.setColumnStretch(3,1)
		self.setProdWidgets(self.nt_line_edit, self.prod_nt_line_edit, self.new_gr_name)
		self.top = QWidget()
		self.top.setLayout(self.top_layout)
		self.sarea = QScrollArea()
		self.sarea.setWidget(self.top)
		self.sarea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.sarea.setWidgetResizable(True)
		self.bottom_layout = QGridLayout()
		self.add_grammar = QPushButton("Save grammar")
		self.add_prod    = QPushButton("Add prod")
		self.add_prod.clicked.connect(self.add_production)
		self.add_grammar.clicked.connect(self.save_grammar)
		self.setPolicyButtons()
		self.bottom_layout.addWidget(self.add_grammar, 0, 0)
		self.bottom_layout.addWidget(self.add_prod, 0, 1)
		self.bottom = QWidget()
		self.bottom.setLayout(self.bottom_layout)
		self.bottom.setStyleSheet("background-color:silver;")

		self.layout.addWidget(self.sarea,0,0)
		self.layout.addWidget(self.bottom,1,0)

		self.layout.setRowStretch(0,9)
		self.layout.setRowStretch(1,1)
		self.setLayout(self.layout)
	def setProdWidgets(self, listNT, listProd, gName):
		if len(listNT) < 1 or len(listProd) < 1:
			return None
		for p in listProd:
			if len(p) < 1:
				return None
		self.nt_line_edit = listNT
		self.prod_nt_line_edit = listProd
		self.new_gr_name = gName
		for i in reversed(range(self.top_layout.count())):
		    self.top_layout.itemAt(i).widget().setParent(None)
		self.top_layout.addWidget(QLabel("Nome:"), 0, 0)
		self.top_layout.addWidget(QLineEdit(gName), 0, 1)
		i = 1
		self.nt_line_edit = listNT
		self.prod_nt_line_edit = listProd
		for nt in listNT:
			p = QLineEdit(nt)
			#p.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
			self.top_layout.addWidget(p, i, 0)

			strProd = ""
			for ii in range(0, len(listProd[i-1]) - 1):
				strProd += listProd[i-1][ii] + "|"
			strProd += listProd[i-1][len(listProd[i-1]) - 1]
			p1 = QLineEdit(strProd)
			#p1.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)

			self.top_layout.addWidget(p1,i, 2)

			label_arrow = QLabel("->")
			self.top_layout.addWidget(label_arrow, i, 1)

			btn_remove = RemoveProdButton("Remover", i)
			print("nt = " + nt + " line " + str(i-1))
			btn_remove.clicked.connect(functools.partial(self.remove_prod_button_clicked, btn_remove.line))
			self.top_layout.addWidget(btn_remove, i, 3)
			i+=1
		self.line = i
		print("linhas " + str(self.line))
	def get_productions(self):
		newNT = []
		newProd = []
		for i in range(1, self.line):
			newNT.append=(self.top_layout.itemAtPosition(i,0).widget().text())
		for i in range(1, self.line):
			prodByNT = []
			prod = ''
			for c in self.top_layout.itemAtPosition(i,2).widget().text():
				if c is '|':
					prodByNT.append=(prod)
					prod = ''
					continue
				elif c is ' ':
					continue
				prod = prod + c
			prodByNT.append=(prod)
			newProd.append=(prodByNT)

		self.nt_line_edit = newNT
		self.prod_nt_line_edit = newProd
	def setPolicyButtons(self):
		self.add_grammar.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.add_prod.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
	def add_production(self):
		self.nt_line_edit.append=("")
		self.prod_nt_line_edit.append=([""])
		for i in reversed(range(self.top_layout.count())):
		    self.top_layout.itemAt(i).widget().setParent(None)
		self.setProdWidgets(self.nt_line_edit, self.prod_nt_line_edit, self.new_gr_name)
		#self.line+=1
	def remove_prod_button_clicked(self, line):
		#if len(Globals.selected.productions) <= 1:
			#return None
		print("linha = " + str(line))
		print(self.nt_line_edit.pop(line))
		print(self.prod_nt_line_edit.pop(line))
		#print(self.nt_line_edit)
		#print(self.prod_nt_line_edit)
		self.setProdWidgets(self.nt_line_edit, self.prod_nt_line_edit, self.new_gr_name)

	def save_grammar(self):
		if len(self.nt_line_edit) != len(self.prod_nt_line_edit):
			return None
		#print(self.nt_line_edit)
		#print(self.prod_nt_line_edit)
		newName = self.top_layout.itemAtPosition(0,1).widget().text()
		self.new_gr_name = newName
		self.get_productions()
		prods = []
		for i in range(0, len(self.nt_line_edit)):
			for p in self.prod_nt_line_edit[i]:
				if len(p) is 2:
					if p[-1] in self.nt_line_edit:
						prods.append=(Production(self.nt_line_edit[i], p))
				else:
					prods.append=(Production(self.nt_line_edit[i], p))
		grams = []
		if Grammar([], newName) in Globals.grammars:
			newG = Grammar(prods, Globals.selected.name)
		else:
			newG = Grammar(prods, newName)
		for g in Globals.grammars:
			if g.name != Globals.selected.name:
				grams.append=(g)
			else:
				grams.append=(newG)
		Globals.grammars = grams
		Globals.selected = newG
		self.updateGR.emit(Globals.selected)
		'''
			aqui voce pega tudo o que esta escrito nas caixas de texto e atualiza o
			self.nt_line_edit e self.nt_line_prod e adiciona a gramatica que foi colocada.
			Precisa do QLineEdit para o nome da gramatica. Pensei em fazer o seguinte: se o nome nao
			estiver na lista de gramaticas, ele salva uma nova. Se estiver, ele atualiza.
			A gramatica seleciona aparece na edição assim que ocorrer o click
		'''
		print('saving')

class RemoveProdButton(QPushButton):
	def __init__(self, text, line):
		super().__init__(text)
		self.line = line


class addAutomatonTab(QWidget):
	saveAFND = QtCore.pyqtSignal(NDAutomaton)
	saveAF = QtCore.pyqtSignal(Automaton)
	minimize = QtCore.pyqtSignal(Automaton)
	printS = QtCore.pyqtSignal()
	def __init__(self):
		super(QWidget,self).__init__()
		self.initial_state_radio_group = QButtonGroup()
		self.transition_table_ui = AutomatonTable() # layout transition table
		self.transition_table = TransitionTable() # real transition table
		self.layout = QGridLayout()
		self.transition_table_ui.setRowCount(1)
		self.transition_table_ui.setColumnCount(0)
		self.transition_table_ui.setAcceptDrops(True)
		self.transition_table_ui.setItem(0,0, StateTableItem("q0"))
		self.complete_button = QPushButton("Completar")
		self.minimize_button = QPushButton("Minimizar")
		self.rename_button = QPushButton("Renomear estados")
		self.rec_button = QPushButton("Reconhecer sentenças")
		self.rec_button.clicked.connect(self.rec_sentences)
		self.n_sentences = QSpinBox()
		self.rename_button.clicked.connect(self.rename_states)
		#self.transition_table_ui.move(0,0)


		self.add_automaton_button = QPushButton("Salvar")
		self.make_non_deterministic_button = \
			QPushButton("Gerar NAF") # botao para criar a tabela com o alfabeto inserido
		self.add_automaton_button.clicked.connect(self.save_automaton)
		self.bottom_layout = QGridLayout()
		self.bottom_layout.addWidget(self.make_non_deterministic_button,0,0)
		self.make_non_deterministic_button.clicked.connect(self.make_non_deterministic)
		self.bottom_layout.addWidget(self.add_automaton_button, 0,2)
		self.bottom_layout.addWidget(self.minimize_button, 0, 1)
		self.bottom_layout.addWidget(self.complete_button, 0, 3)
		self.bottom_layout.addWidget(self.rec_button, 0, 4)
		self.bottom_layout.addWidget(self.n_sentences, 0, 5)
		self.minimize_button.clicked.connect(self.do_minimize)
		self.complete_button.clicked.connect(self.do_complete)
		self.bottom_panel = QWidget()
		self.bottom_panel.setLayout(self.bottom_layout)

		self.top_layout = QGridLayout()
		self.add_remove_state_layout = QGridLayout()
		self.automaton_name = QWidget()
		self.name_layout = QGridLayout()
		self.name_label = QLabel()
		self.name_label.setText("Nome:")
		self.name_edit = QLineEdit()
		self.name_layout.addWidget(self.name_label,0,0)
		self.name_layout.addWidget(self.name_edit,0,1)
		self.add_remove_panel = QWidget()
		self.top_panel = QWidget()
		self.edit_name = QLineEdit()
		self.edit_name.setDragEnabled(True)
		self.edit_alphabet = QLineEdit()
		self.list_symbol  = QListWidget()
		self.remove_symbol_button = QPushButton("Remover símbolo")
		self.remove_symbol_button.clicked.connect(self.remove_symbol)
		self.add_symbol_button = QPushButton("Adicionar símbolo")
		self.add_symbol_button.clicked.connect(self.add_new_symbol)
		self.add_remove_symbol_panel = QWidget()
		self.add_remove_symbol_layout = QGridLayout()
		self.add_remove_symbol_layout.addWidget(self.add_symbol_button, 0,0)
		self.add_remove_symbol_layout.addWidget(self.remove_symbol_button, 1, 0)
		self.add_remove_symbol_panel.setLayout(self.add_remove_symbol_layout)

		self.add_new_state = QPushButton("Adicionar estado")
		self.remove_state_button = QPushButton("Remover estado selecionado")
		self.add_remove_state_layout.addWidget(self.add_new_state, 0,0)
		self.add_remove_state_layout.addWidget(self.remove_state_button, 1, 0)
		self.add_remove_panel.setLayout(self.add_remove_state_layout)
		self.automaton_name.setLayout(self.name_layout)
		self.top_layout.addWidget(self.automaton_name)
		self.top_layout.addWidget(self.add_remove_symbol_panel, 1, 0)
		self.top_layout.addWidget(self.list_symbol, 1, 1)
		self.top_layout.addWidget(self.add_remove_panel, 2,0)
		self.test_sentence_pertinence_button = QPushButton("testar sentença")
		self.test_sentence_pertinence_edit   = QLineEdit()
		self.test_sentence_pertinence_button.clicked.connect(self.pertinence_test)
		self.top_layout.addWidget(self.test_sentence_pertinence_edit, 3, 1)
		self.top_layout.addWidget(self.test_sentence_pertinence_button, 3,0)
		self.setPolicyEdits()
		self.setPolicyButtons()
		self.top_layout.setColumnStretch(0, 1)
		self.top_layout.setColumnStretch(1, 2)


		self.list_states = StateList()
		self.list_states.setDragEnabled(True)
		self.list_states.itemChanged.connect(self.itemChanged)
		self.list_symbol.itemChanged.connect(self.symbol_changed)
		item = StateItem("q0")
		item.setFlags(item.flags() | Qt.ItemIsEditable)
		self.list_states.addItem(item)
		#self.list_states.setCurrentItem(item)

		self.list_states.itemSelectionChanged.connect(self.selectChanged)
		self.top_layout.addWidget(self.list_states, 2,1)
		self.list_states.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.top_panel.setStyleSheet("background:silver;")
		self.top_panel.setLayout(self.top_layout)
		self.layout.setRowStretch(0, 1)
		self.layout.setRowStretch(1, 5)
		self.layout.addWidget(self.top_panel,0,0)
		self.layout.addWidget(self.transition_table_ui, 1, 0)
		self.layout.addWidget(self.bottom_panel, 2, 0)
		self.setLayout(self.layout)
		self.set_button_events()
		self.set_edits_events()
		self.i = 0
		self.last_selected = None
		self.transition_table_ui.setVerticalHeaderItem(0, StateTableItem("q0"))
		self.set_placeholders()
		self.alphabet = []
		#self.showAutomaton(Globals.automata[0])

	def suc(self, msg):
		d = QDialog()
		b1 = QPushButton(msg,d)
		d.setMinimumSize(300, 100)
		d.setWindowTitle(":)")
		d.setWindowModality(Qt.ApplicationModal)
		d.exec_()

	def pertinence_test(self):
		print("hahaha")
		af = Globals.selected
		if type(af) is not Automaton:
			self.error("Selecione um AF :)")
			return
		sentence = self.test_sentence_pertinence_edit.text()
		print(sentence)
		print(af.process_input(sentence))
		resp = ""
		if not(af.process_input(sentence)):
			resp = " não "
		self.suc("A sentença" +resp+" pertence ao conjunto da linguagem")

	def rec_sentences(self):
		if type(Globals.selected) != Automaton:
			self.error("Escolha um automato")
		n = self.n_sentences.value()
		lista = Globals.selected.n_size_sentences_accepted(n)
		MainWindow.logtxt = "Sentenças reconhecidas: \n" + str(lista)
		self.printS.emit()
	def error(self, msg):
		error_dialog = QtWidgets.QErrorMessage()
		error_dialog.showMessage(msg)
		error_dialog.exec_()
	def do_minimize(self):
		af = Globals.selected
		if type(af) != Automaton:
			print("Não pode")
			return
		min_af = af.minimize()
		min_af.name = "minimized_" + af.name
		Globals.automata.append=(min_af)
		Globals.selected = min_af
		self.minimize.emit(Globals.selected)
		self.save_automaton()
	def do_complete(self):
		af = Globals.selected
		if type(af) != Automaton:
			print("Não pode")
			return
		af.complete()
		Globals.selected = af
		self.minimize.emit(Globals.selected)
	def rename_states(self):
		af = Globals.selected
		if type(af) != Automaton:
			print("Não pode")
			return
		raf = af.rename_states()
		raf.name = "renamed_" + af.name
		Globals.automata.append=(raf)
		Globals.selected = raf
		self.minimize.emit(Globals.selected)
	def add_new_symbol(self):
		symbols = [str(self.list_symbol.item(i).text()) for i in range(self.list_symbol.count())]
		c_ord = -1
		for s in symbols:
			if (c_ord < ord(s)):
				c_ord = ord(s)

		new_symbol = chr(c_ord+1)
		item = SymbolItem(new_symbol)
		item.setFlags(item.flags() | Qt.ItemIsEditable)
		self.list_symbol.addItem(item)
		column = self.transition_table_ui.columnCount() - 2
		self.transition_table_ui.insertColumn(column)
		column = self.transition_table_ui.columnCount() - 2
		self.transition_table_ui.setHorizontalHeaderItem(column-1, QTableWidgetItem(new_symbol))

		rowCount = self.transition_table_ui.rowCount()

		for i in range(0, rowCount):
			self.transition_table_ui.setItem(i, column -1, QTableWidgetItem("-"))
	def remove_symbol(self):
		if self.list_symbol.count() == 1:
			return
		item = self.list_symbol.selectedItems()[0]
		print(item.text())
		column_count = self.transition_table_ui.columnCount()

		for i in range(0, column_count):
			if self.transition_table_ui.horizontalHeaderItem(i).text() == item.text():
				self.transition_table_ui.removeColumn(i)
				break
		self.list_symbol.takeItem(self.list_symbol.currentRow())
	def setPolicyEdits(self):
		self.edit_name.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.edit_alphabet.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
	def setPolicyButtons(self):
		self.add_new_state.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.remove_state_button.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
	def set_placeholders(self):
		self.edit_name.setPlaceholderText("Digite o nome do automato")
		self.edit_alphabet.setPlaceholderText("Digite o alfabeto")
	def set_button_events(self):
		self.add_new_state.clicked.connect(self.create_state)
		self.remove_state_button.clicked.connect(self.remove_state)
	def set_edits_events(self):
		self.edit_alphabet.textEdited.connect(self.alphabet_changed)
	def generate_table(self, alphabet, states_names):
		print()

	def create_state(self):
		self.i += 1
		item = StateItem("q" + str(self.i))
		item.setFlags(item.flags() | Qt.ItemIsEditable)
		self.list_states.addItem(item)
		count = self.transition_table_ui.rowCount()
		column_count = self.transition_table_ui.columnCount() - 2
		self.transition_table_ui.setRowCount(count+1)
		self.transition_table_ui.setVerticalHeaderItem(count, StateTableItem("q" + str(self.i)))
		for i in range(0, len(self.alphabet)):
			self.transition_table_ui.setItem(count,i,QTableWidgetItem("-"))

		rb = QRadioButton()
		cb = QCheckBox()
		self.initial_state_radio_group.addButton(rb)
		self.transition_table_ui.setCellWidget(count,column_count,rb)
		self.transition_table_ui.setCellWidget(count,column_count+1,cb)

	def remove_state(self):
		item = self.list_states.takeItem(self.list_states.row(self.list_states.selectedItems()[0]))
		row_count = self.transition_table_ui.rowCount()
		column_count = self.transition_table_ui.columnCount()

		for i in range(0, row_count):
			for j in range(0, column_count - 2):
				try:
					if self.transition_table_ui.item(i, j).text() == item.text():
						self.transition_table_ui.item(i, j).setText("-")
				except:
					print("Problema com " + str((i,j)))
		for i in range(0, row_count):
			if self.transition_table_ui.verticalHeaderItem(i).text() == item.text():
					self.transition_table_ui.removeRow(i)
					return
	def itemChanged(self, item):
		print(item.oldName + " mudou para " + item.text())
		row_count = self.transition_table_ui.rowCount()
		column_count = self.transition_table_ui.columnCount()
		# este for muda o header da tabela
		for i in range(0, row_count):
			try:
				if self.transition_table_ui.verticalHeaderItem(i).text() == item.oldName:
					print("haha")
					self.transition_table_ui.setVerticalHeaderItem(i, StateTableItem(item.text()))
			except:
				pass
		for i in range(0, row_count):
			for j in range(0, column_count):
				try:
					if self.transition_table_ui.item(i, j).text() == item.oldName:
						self.transition_table_ui.item(i,j).setText(item.text())
				except:
					pass


		item.oldName = item.text()
		MainWindow.jesus = item.text()
	def symbol_changed(self, item):
			approval_change = True
			items = [self.list_symbol.item(i) for i in range(self.list_symbol.count())]
			items = list(set(items) - {self.list_symbol.selectedItems()[0]})

			for i in items:
				if item.text() == i.text():
					print("IGUAL")
					approval_change = False
					break
			if approval_change:
				column_count = self.transition_table_ui.columnCount()
				for i in range(0, column_count):
					if self.transition_table_ui.horizontalHeaderItem(i).text() == item.oldName:
						self.transition_table_ui.horizontalHeaderItem(i).setText(item.text())
						print("OFUND")
				item.oldName = item.text()
			else:
				item.setText(item.oldName)
	def selectChanged(self):
		'''
			no momento, este método não tem uso algum
		'''
		print("quem mudou= " + self.list_states.selectedItems()[0].text())
		self.last_selected = self.list_states.selectedItems()[0]
		MainWindow.jesus = self.list_states.selectedItems()[0].text()
		print(MainWindow.jesus)

	def make_non_deterministic(self):
		newAF = make_nondeterministic(Globals.selected)
		newAF.name = Globals.selected.name + " (nondeterministic)"
		names = [af.name for af in Globals.automata]
		while newAF in Globals.automata:
			for name in names:
				if newAF.name == name:
					newAF.name += "'"
					break
		Globals.automata.append=(newAF)
		Globals.selected = newAF
		self.saveAFND.emit(Globals.selected)

	def setColsLabels(self, labels):
		i = 0
		for label in labels:
			self.transition_table_ui.setHorizontalHeaderItem(i, StateTableItem(label))
			#self.transition_table_ui.setColumnWidth(i, 1)
			i+=1

		self.transition_table_ui.setHorizontalHeaderItem(i, StateTableItem("Inicial"))
		self.transition_table_ui.setHorizontalHeaderItem(i+1, StateTableItem("Final"))
	def alphabet_changed(self):
		print(self.alphabet)
		text = self.edit_alphabet.text()

		self.transition_table_ui.insertColumn(1)
		return
		if len(text) == 1:
			return
		if text[len(text)-1] == ",":
			new_text = text[0:len(text)-1]
			old_column_count = self.transition_table_ui.columnCount()
			self.transition_table_ui.setColumnCount(old_column_count - 3)
		else:
			new_text = text[0:len(text) - 1] + "," + text[len(text) - 1]
			old_column_count = self.transition_table_ui.columnCount()
			self.transition_table_ui.setColumnCount(old_column_count - 2)
			self.transition_table_ui.setColumnCount(old_column_count + 1)
			self.setColsLabels(new_text.split(","))
		self.edit_alphabet.setText(new_text)
		#self.showAutomaton(Globals.selected)

	def showAutomaton(self, af):
		self.name_edit.setText(af.name)
		self.list_states.clear()
		self.list_symbol.clear()
		self.edit_alphabet.setText(','.join(map(str, af.alphabet)) )
		self.alphabet = af.alphabet
		self.transition_table_ui.setRowCount(len(af.states))
		self.transition_table_ui.setColumnCount(len(af.alphabet) + 2)
		self.setColsLabels(af.alphabet)
		states_list = list(af.states)
		self.initial_state_radio_group = QButtonGroup()
		for i in range(0, len(af.alphabet)):
			item = SymbolItem(af.alphabet[i])
			item.setFlags(item.flags() | Qt.ItemIsEditable)
			self.list_symbol.addItem(item)
		for i in range(0, len(states_list)):
			s = states_list[i]
			item = StateItem(s.name)
			item.setFlags(item.flags() | Qt.ItemIsEditable)
			self.list_states.addItem(item)
			self.transition_table_ui.setVerticalHeaderItem(i, StateTableItem(s.name))
			cb = QCheckBox()
			rb = QRadioButton()
			self.initial_state_radio_group.addButton(rb)
			if s.isAcceptance:
				cb.setChecked(True)
			if s == af.initialState:
				rb.setChecked(True)
			self.transition_table_ui.setCellWidget(i, len(af.alphabet)+1, cb)
			self.transition_table_ui.setCellWidget(i, len(af.alphabet), rb)

		for i in range(0, len(states_list)):
			s = states_list[i]
			for sym in af.alphabet:
				absent = True
				for t in s.transitions:
					if t.symbol == sym:
						absent = False
						self.set_transition_cell(s.name, t.target_state.name, t.symbol)
				if absent:
					self.set_transition_cell(s.name, "-", sym)

	def set_transition_cell(self, state, target, symbol):
		row = -1
		column = -1
		for i in range(0, self.transition_table_ui.columnCount()):
			if self.transition_table_ui.horizontalHeaderItem(i).text() == symbol:
				print("coluna = " + str(i))
				column = i
		for i in range(0, self.transition_table_ui.rowCount()):
			if self.transition_table_ui.verticalHeaderItem(i).text() == state:
				print("linha = " + str(i))
				row = i
		print((row,column))
		self.transition_table_ui.setItem(row, column, QTableWidgetItem(target))
	def save_automaton(self):
		states = set()
		finalStates = set()
		initialState = None
		newalphabet = []
		for j in range(0, self.transition_table_ui.columnCount() - 2):
			newalphabet.append=(self.transition_table_ui.horizontalHeaderItem(j).text())
		for i in range(0, self.transition_table_ui.rowCount()):
			newS = State(self.transition_table_ui.verticalHeaderItem(i).text(), self.transition_table_ui.cellWidget(i, self.transition_table_ui.columnCount() - 1).checkState() == 2)
			states.add(newS)
			if newS.isAcceptance:
				finalStates.add(newS)
			if self.transition_table_ui.cellWidget(i, len(newalphabet)).isChecked():
				initialState = newS
				print("novo inicial = " + str(newS))
		for i in range(0, self.transition_table_ui.rowCount()):
			for s in states:
				if self.transition_table_ui.verticalHeaderItem(i).text() == s.name:
					for j in range(0, self.transition_table_ui.columnCount() - 2):
						for ns in states:
							if ns.name == self.transition_table_ui.item(i,j).text():
								s.add_transition(Transition(self.transition_table_ui.horizontalHeaderItem(j).text(), ns))

		auts = []
		if Automaton({},{}, State(""), name = self.name_edit.text()) in Globals.automata:
			newA = Automaton(states, finalStates, initialState, newalphabet, Globals.selected.name)
		else:
			newA = Automaton(states, finalStates, initialState, newalphabet, self.name_edit.text())
		for a in Globals.automata:
			if a.name != Globals.selected.name:
				auts.append=(a)
			else:
				auts.append=(newA)
		Globals.automata = auts
		Globals.selected = newA
		self.saveAF.emit(Globals.selected)


class GrammarOperationsTab(QWidget):
	updateGR = QtCore.pyqtSignal(Grammar)
	def __init__(self):
		super(QWidget, self).__init__()

		self.line = 0
		self.layout = QGridLayout()
		self.layout.setRowStretch(0,1)
		self.layout.setRowStretch(1,1)
		self.layout.setRowStretch(2,1)
		self.top = QWidget()
		self.top.setStyleSheet("background-color:silver;")
		self.top_layout = QGridLayout()
		self.top_layout.setRowStretch(0,1)
		self.top_layout.setRowStretch(1,1)
		self.top_layout.setRowStretch(2,1)
		self.top_layout.setRowStretch(3,1)
		self.top_op1 = QWidget()
		self.top_op1.setStyleSheet("background-color:silver;")
		self.top_op1_layout = QGridLayout()
		self.top_op1_layout.setColumnStretch(0,1)
		self.top_op1_layout.setColumnStretch(1,1)
		self.top_op1label = QLabel()
		self.top_op1label.setText("GR 1:")
		self.top_op1edit = QLineEdit()
		self.top_op1_layout.addWidget(self.top_op1label,0,0)
		self.top_op1_layout.addWidget(self.top_op1edit,0,1)
		self.top_op1.setLayout(self.top_op1_layout)
		self.top_op2 = QWidget()
		self.top_op2.setStyleSheet("background-color:silver;")
		self.top_op2_layout = QGridLayout()
		self.top_op2_layout.setColumnStretch(0,1)
		self.top_op2_layout.setColumnStretch(1,1)
		self.top_op2label = QLabel()
		self.top_op2label.setText("GR 2:")
		self.top_op2edit = QLineEdit()
		self.top_op2_layout.addWidget(self.top_op2label,0,0)
		self.top_op2_layout.addWidget(self.top_op2edit,0,1)
		self.top_op2.setLayout(self.top_op2_layout)
		self.top_operation = QLabel()
		self.top_operation.setAlignment(Qt.AlignCenter)
		self.top_operation.setText(".")
		self.top_operation.setStyleSheet("background-color:lightslategrey;")
		self.top_done = QPushButton("Pronto")
		self.top_done.clicked.connect(self.add_concatenation)
		self.top_layout.addWidget(self.top_op1,0,0)
		self.top_layout.addWidget(self.top_op2,2,0)
		self.top_layout.addWidget(self.top_operation,1,0)
		self.top_layout.addWidget(self.top_done,3,0)
		self.top.setLayout(self.top_layout)

		self.mid = QWidget()
		self.mid.setStyleSheet("background-color:silver;")
		self.mid_layout = QGridLayout()
		self.mid_layout.setRowStretch(0,1)
		self.mid_layout.setRowStretch(1,1)
		self.mid_layout.setRowStretch(2,1)
		self.mid_layout.setRowStretch(3,1)
		self.mid_op1 = QWidget()
		self.mid_op1.setStyleSheet("background-color:silver;")
		self.mid_op1_layout = QGridLayout()
		self.mid_op1_layout.setColumnStretch(0,1)
		self.mid_op1_layout.setColumnStretch(1,1)
		self.mid_op1label = QLabel()
		self.mid_op1label.setText("GR 1:")
		self.mid_op1edit = QLineEdit()
		self.mid_op1_layout.addWidget(self.mid_op1label,0,0)
		self.mid_op1_layout.addWidget(self.mid_op1edit,0,1)
		self.mid_op1.setLayout(self.mid_op1_layout)
		self.mid_op2 = QWidget()
		self.mid_op2.setStyleSheet("background-color:silver;")
		self.mid_op2_layout = QGridLayout()
		self.mid_op2_layout.setColumnStretch(0,1)
		self.mid_op2_layout.setColumnStretch(1,1)
		self.mid_op2label = QLabel()
		self.mid_op2label.setText("GR 2:")
		self.mid_op2edit = QLineEdit()
		self.mid_op2_layout.addWidget(self.mid_op2label,0,0)
		self.mid_op2_layout.addWidget(self.mid_op2edit,0,1)
		self.mid_op2.setLayout(self.mid_op2_layout)
		self.mid_operation = QLabel()
		self.mid_operation.setAlignment(Qt.AlignCenter)
		self.mid_operation.setText("∪")
		self.mid_operation.setStyleSheet("background-color:lightslategrey;")
		self.mid_done = QPushButton("Pronto")
		self.mid_done.clicked.connect(self.add_union)
		self.mid_layout.addWidget(self.mid_op1,0,0)
		self.mid_layout.addWidget(self.mid_op2,2,0)
		self.mid_layout.addWidget(self.mid_operation,1,0)
		self.mid_layout.addWidget(self.mid_done,3,0)
		self.mid.setLayout(self.mid_layout)

		self.bot = QWidget()
		self.bot.setStyleSheet("background-color:silver;")
		self.bot_layout = QGridLayout()
		self.bot_layout.setRowStretch(0,1)
		self.bot_layout.setRowStretch(1,1)
		self.bot_layout.setRowStretch(2,1)
		self.bot_op1 = QWidget()
		self.bot_op1.setStyleSheet("background-color:silver;")
		self.bot_op1_layout = QGridLayout()
		self.bot_op1_layout.setColumnStretch(0,1)
		self.bot_op1_layout.setColumnStretch(1,1)
		self.bot_op1label = QLabel()
		self.bot_op1label.setText("GR:")
		self.bot_op1edit = QLineEdit()
		self.bot_op1_layout.addWidget(self.bot_op1label,0,0)
		self.bot_op1_layout.addWidget(self.bot_op1edit,0,1)
		self.bot_op1.setLayout(self.bot_op1_layout)
		self.bot_operation = QLabel()
		self.bot_operation.setAlignment(Qt.AlignCenter)
		self.bot_operation.setText("*")
		self.bot_operation.setStyleSheet("background-color:lightslategrey;")
		self.bot_done = QPushButton("Pronto")
		self.bot_done.clicked.connect(self.add_kleene)
		self.bot_layout.addWidget(self.bot_op1,0,0)
		self.bot_layout.addWidget(self.bot_operation,1,0)
		self.bot_layout.addWidget(self.bot_done,2,0)
		self.bot.setLayout(self.bot_layout)

		self.layout.addWidget(self.top,0,0)
		self.layout.addWidget(self.mid,1,0)
		self.layout.addWidget(self.bot,2,0)

		self.setLayout(self.layout)
	def add_concatenation(self):
		g_1 = None
		g_2 = None
		for g1 in Globals.grammars:
			if g1.name == self.top_op1edit.text():
				g_1 = g1
		for g2 in Globals.grammars:
			if g2.name == self.top_op2edit.text():
				g_2 = g2
		if g_1 != None and g_2 != None:
			newG = grammar_concatenation(g_1, g_2)
			while newG in Globals.grammars:
				newG.name = newG.name + "'"
			Globals.grammars.append=(newG)
			Globals.selected = newG
			self.updateGR.emit(Globals.selected)

	def add_union(self):
		g_1 = None
		g_2 = None
		for g1 in Globals.grammars:
			if g1.name == self.mid_op1edit.text():
				g_1 = g1
		for g2 in Globals.grammars:
			if g2.name == self.mid_op2edit.text():
				g_2 = g2
		if g_1 != None and g_2 != None:
			newG = grammar_union(g_1, g_2)
			while newG in Globals.grammars:
				newG.name = newG.name + "'"
			Globals.grammars.append=(newG)
			Globals.selected = newG
			self.updateGR.emit(Globals.selected)
	def add_kleene(self):
		g_1 = None
		for g1 in Globals.grammars:
			if g1.name == self.bot_op1edit.text():
				g_1 = g1
		if g_1 != None:
			newG = grammar_kleene_star(g_1)
			while newG in Globals.grammars:
				newG.name = newG.name + "'"
			Globals.grammars.append=(newG)
			Globals.selected = newG
			self.updateGR.emit(Globals.selected)


class StateList(QListWidget):
	def __init__(self):
		super(QListWidget, self).__init__()
class StateItem(QListWidgetItem):
	def __init__(self, text):
		super().__init__(text)
		self.oldName = text
class SymbolItem(QListWidgetItem):
	def __init__(self, text):
		super().__init__(text)
		self.oldName = text
	def __hash__(self):
		return id(self)

class StateTableItem(QTableWidgetItem):
	def __init__(self, text):
		super(QTableWidgetItem, self).__init__(text)
	def dropEvent(self, event):
		print("misc")

class AutomatonTable(QTableWidget):
	def __init__(self):
		super(QTableWidget, self).__init__()
		self.setAcceptDrops(True)
	def dropEvent(self, event):
		position = event.pos()
		x = self.rowAt(position.y())
		y = self.columnAt(position.x())
		self.item(x,y).setText(MainWindow.jesus)
		event.accept()
	def dragEnterEvent(self, event):
		print('end=er')
		event.accept()
	def keyPressEvent(self, event):
		print("deletado")
class TransitionTable:
	def __init__(self):
		print('something')


class AutomataOperationsTab(QWidget):
	def __init__(self, parent=None):
		super(QWidget, self).__init__(parent)
		self.layout = QVBoxLayout(self)
		self.tabs = QTabWidget()
		self.tab1 = QWidget()
		self.tab2 = QWidget()
		self.tabs.resize(300,200)

		self.tabs.addTab(self.tab1,"Union")
		self.tabs.addTab(self.tab2,"Concatenation")

		self.tab1.layout = QVBoxLayout(self)
		self.pushButton1 = QPushButton("PyQt5 button")
		self.tab1.layout.addWidget(self.pushButton1)
		self.tab1.setLayout(self.tab1.layout)

		self.layout.addWidget(self.tabs)
		self.setLayout(self.layout)
	@pyqtSlot()
	def on_click(self):
		print("\n")
		for currentQTableWidgetItem in self.tableWidget.selectedItems():
			print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

class UnionTab(QWidget):
	def __init__(self):
		super(QWidget,self).__init__()
		self.top_panel = QWidget()
		self.bottom_panel = QWidget()
		self.button_af1 = QPushButton()
		self.button_af2 = QPushButton()
		self.top_layout = QGridLayout()
		self.bottom_layout = QGridLayout()
		self.set_top_panel()
	def set_top_panel(self):
		self.top_layout.addWidget(self.button_af1, 0, 0)
		self.top_layout.addWidget(self.button_af2, 1, 0)


class Edit(QLineEdit):
	def __init__(self, parent=None):
		QLineEdit.__init__(self, parent)

	def keyPressEvent(self, event):
		if type(event) == QtGui.QKeyEvent:
			#self.setText (chr(event.key()).lower())
			event.accept()
		else:
			event.ignore()


class AFOperationsTab(QWidget):
	updateAF = QtCore.pyqtSignal(Automaton)
	def __init__(self):
		super(QWidget, self).__init__()

		self.line = 0
		self.layout = QGridLayout()
		self.layout.setRowStretch(0,1)
		self.layout.setRowStretch(1,1)
		self.layout.setRowStretch(2,1)
		self.top = QWidget()
		self.top.setStyleSheet("background-color:silver;")
		self.top_layout = QGridLayout()
		self.top_layout.setRowStretch(0,1)
		self.top_layout.setRowStretch(1,1)
		self.top_layout.setRowStretch(2,1)
		self.top_layout.setRowStretch(3,1)
		self.top_op1 = QWidget()
		self.top_op1.setStyleSheet("background-color:silver;")
		self.top_op1_layout = QGridLayout()
		self.top_op1_layout.setColumnStretch(0,1)
		self.top_op1_layout.setColumnStretch(1,1)
		self.top_op1label = QLabel()
		self.top_op1label.setText("AF 1:")
		self.top_op1edit = QLineEdit()
		self.top_op1_layout.addWidget(self.top_op1label,0,0)
		self.top_op1_layout.addWidget(self.top_op1edit,0,1)
		self.top_op1.setLayout(self.top_op1_layout)
		self.top_op2 = QWidget()
		self.top_op2.setStyleSheet("background-color:silver;")
		self.top_op2_layout = QGridLayout()
		self.top_op2_layout.setColumnStretch(0,1)
		self.top_op2_layout.setColumnStretch(1,1)
		self.top_op2label = QLabel()
		self.top_op2label.setText("AF 2:")
		self.top_op2edit = QLineEdit()
		self.top_op2_layout.addWidget(self.top_op2label,0,0)
		self.top_op2_layout.addWidget(self.top_op2edit,0,1)
		self.top_op2.setLayout(self.top_op2_layout)
		self.top_operation = QLabel()
		self.top_operation.setAlignment(Qt.AlignCenter)
		self.top_operation.setText("∩")
		self.top_operation.setStyleSheet("background-color:lightslategrey;")
		self.top_done = QPushButton("Pronto")
		self.top_done.clicked.connect(self.add_intersection)
		self.top_layout.addWidget(self.top_op1,0,0)
		self.top_layout.addWidget(self.top_op2,2,0)
		self.top_layout.addWidget(self.top_operation,1,0)
		self.top_layout.addWidget(self.top_done,3,0)
		self.top.setLayout(self.top_layout)

		self.mid = QWidget()
		self.mid.setStyleSheet("background-color:silver;")
		self.mid_layout = QGridLayout()
		self.mid_layout.setRowStretch(0,1)
		self.mid_layout.setRowStretch(1,1)
		self.mid_layout.setRowStretch(2,1)
		self.mid_layout.setRowStretch(3,1)
		self.mid_op1 = QWidget()
		self.mid_op1.setStyleSheet("background-color:silver;")
		self.mid_op1_layout = QGridLayout()
		self.mid_op1_layout.setColumnStretch(0,1)
		self.mid_op1_layout.setColumnStretch(1,1)
		self.mid_op1label = QLabel()
		self.mid_op1label.setText("AF 1:")
		self.mid_op1edit = QLineEdit()
		self.mid_op1_layout.addWidget(self.mid_op1label,0,0)
		self.mid_op1_layout.addWidget(self.mid_op1edit,0,1)
		self.mid_op1.setLayout(self.mid_op1_layout)
		self.mid_op2 = QWidget()
		self.mid_op2.setStyleSheet("background-color:silver;")
		self.mid_op2_layout = QGridLayout()
		self.mid_op2_layout.setColumnStretch(0,1)
		self.mid_op2_layout.setColumnStretch(1,1)
		self.mid_op2label = QLabel()
		self.mid_op2label.setText("AF 2:")
		self.mid_op2edit = QLineEdit()
		self.mid_op2_layout.addWidget(self.mid_op2label,0,0)
		self.mid_op2_layout.addWidget(self.mid_op2edit,0,1)
		self.mid_op2.setLayout(self.mid_op2_layout)
		self.mid_operation = QLabel()
		self.mid_operation.setAlignment(Qt.AlignCenter)
		self.mid_operation.setText("-")
		self.mid_operation.setStyleSheet("background-color:lightslategrey;")
		self.mid_done = QPushButton("Pronto")
		self.mid_done.clicked.connect(self.add_difference)
		self.mid_layout.addWidget(self.mid_op1,0,0)
		self.mid_layout.addWidget(self.mid_op2,2,0)
		self.mid_layout.addWidget(self.mid_operation,1,0)
		self.mid_layout.addWidget(self.mid_done,3,0)
		self.mid.setLayout(self.mid_layout)

		self.bot = QWidget()
		self.bot.setStyleSheet("background-color:silver;")
		self.bot_layout = QGridLayout()
		self.bot_layout.setRowStretch(0,1)
		self.bot_layout.setRowStretch(1,1)
		self.bot_layout.setRowStretch(2,1)
		self.bot_op1 = QWidget()
		self.bot_op1.setStyleSheet("background-color:silver;")
		self.bot_op1_layout = QGridLayout()
		self.bot_op1_layout.setColumnStretch(0,1)
		self.bot_op1_layout.setColumnStretch(1,1)
		self.bot_op1label = QLabel()
		self.bot_op1label.setText("AF:")
		self.bot_op1edit = QLineEdit()
		self.bot_op1_layout.addWidget(self.bot_op1label,0,0)
		self.bot_op1_layout.addWidget(self.bot_op1edit,0,1)
		self.bot_op1.setLayout(self.bot_op1_layout)
		self.bot_operation = QLabel()
		self.bot_operation.setAlignment(Qt.AlignCenter)
		self.bot_operation.setText("R")
		self.bot_operation.setStyleSheet("background-color:lightslategrey;")
		self.bot_done = QPushButton("Pronto")
		self.bot_done.clicked.connect(self.add_reverse)
		self.bot_layout.addWidget(self.bot_op1,0,0)
		self.bot_layout.addWidget(self.bot_operation,1,0)
		self.bot_layout.addWidget(self.bot_done,2,0)
		self.bot.setLayout(self.bot_layout)

		self.layout.addWidget(self.top,0,0)
		self.layout.addWidget(self.mid,1,0)
		self.layout.addWidget(self.bot,2,0)

		self.setLayout(self.layout)
	def add_intersection(self):
		a_1 = None
		a_2 = None
		for a1 in Globals.automata:
			if a1.name == self.top_op1edit.text():
				a_1 = a1
		for a2 in Globals.automata:
			if a2.name == self.top_op2edit.text():
				a_2 = a2
		if a_1 != None and a_2 != None:
			newA = automata_intersec(a_1, a_2)
			while newA in Globals.automata:
				newA.name = newA.name + "'"
			Globals.automata.append=(newA)
			Globals.selected = newA
			self.updateAF.emit(Globals.selected)

	def add_difference(self):
		a_1 = None
		a_2 = None
		for a1 in Globals.automata:
			if a1.name == self.mid_op1edit.text():
				a_1 = a1
		for a2 in Globals.automata:
			if a2.name == self.mid_op2edit.text():
				a_2 = a2
		if a_1 != None and a_2 != None:
			newA = automata_difference(a_1, a_2)
			while newA in Globals.automata:
				newA.name = newA.name + "'"
			Globals.automata.append=(newA)
			Globals.selected = newA
			self.updateAF.emit(Globals.selected)
	def add_reverse(self):
		a_1 = None
		for a1 in Globals.automata:
			if a1.name == self.bot_op1edit.text():
				a_1 = a1
		if a_1 != None:
			newA = getReverse(a_1)
			while newA in Globals.automata:
				newA.name = newA.name + "'"
			Globals.automata.append=(newA)
			Globals.selected = newA
			self.updateAF.emit(Globals.selected)
