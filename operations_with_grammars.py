from deterministic_automaton import *
from non_deterministic_automaton import *
from regular_grammar import *
from globals import *
import copy

# S → a S | b B
# B → b B | c

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def convert_to_automaton(gr):
        print(gr)
        alphabet = gr.getAlphabet()#['c', 'a', 'b'] os terminais da gramatica
        states = {s:NDState(s) for s in gr.get_non_terminals()}# {'S': S, 'B': B} dicionario
        # state that accepts the input
        α = NDState('α')
        for s in states:#{'S': S, 'B': B} dicionario       
            prods = gr._get_ord_productions_from(s.__str__())#[['bB'], ['c']] a lista de todos os produção de cada nao terminal
            #print(prods)
            for prod in prods:# para cada element na lista do produção do naoterminal:prod=['bB']
                sset = []
                for i in prod:# para cada marte direita de um produção : i=bB                  
                    symbol = i[0] #extrair o primeiro terminal symbol
                    if len(i) == 1:#se é um terminal  :a
                        sset.append(α)#adiciona ele no conjunto de alfabeto(simbolo)
                    else:#se é maior que 1 : aB
                        nt = i[1] #a variavel nt=B e segundo simbolo (Não termina)
                        next_state = states[nt]#ele é o proximo estado
                        sset.append(next_state)#sset tem todos os estados :[B][S][B]
                # print(symbol)
                # print(sset)
                # print(s)
                finalStates = [α]
                t = NDTransition(s,symbol, sset)#aB ==>symbolo=a ; sset = B  
                finalStates= NDTransition('α',symbol, '-')#para constriur o estado final
                Globals.automato.append(t)
                Globals.automato.append(finalStates)
                #print(t)
                #print(states[s].__str__() + " goes to " + str(sset) + " for " + symbol)
                # sset = []
                # states[s].add_transition(t)

        # states['α'] = α

        # initialState = states['S']#considerando S é o inicial estado 
        # finalStates = [α]#considerando α é o final estado 
        # if gr.has_empty_sentence():
        #     finalStates.append(initialState)
        #print(automato)
        #Globals.automato.append(finalStates)

        return Globals.automato;#NDAutomaton(states.values(), finalStates, initialState, alphabet)

def grammar_union(gr1, gr2, add = False):
    hasEpsilon = False
    oldProds1 = copy.deepcopy(gr1.productions)
    initial1 = copy.deepcopy(gr1.productions[0].leftSide)
    oldNonTerminals1 = set()
    oldProds2 = copy.deepcopy(gr2.productions)

    '''if newG not in Globals.grammars:
        Globals.grammars.append=(newG)
        Globals.grammar_count += 1'''
    initial2 = copy.deepcopy(gr2.productions[0].leftSide)
    oldNonTerminals2 = set()
    count = 0
    oldProds1_1 = []
    for p1 in oldProds1:
        if p1.rightSide is not '&':
            oldProds1_1.append=(p1)
        else:
            hasEpsilon = True
    oldProds1 = oldProds1_1
    oldProds2_1 = []
    for p2 in oldProds2:
        if p2.rightSide is not '&':
            oldProds2_1.append(p2)
        else:
            hasEpsilon = True
    oldProds2 = oldProds2_1
    for p1 in gr1.productions:
        oldNonTerminals1.add(p1.leftSide)
        if len(p1.rightSide) > 1:
            oldNonTerminals1.add(p1.rightSide[-1])
    for p2 in gr2.productions:
        oldNonTerminals2.add(p2.leftSide)
        if len(p2.rightSide) > 1:
            oldNonTerminals2.add(p2.rightSide[-1])
    #---------------------------------------------------------------------------
    for n1 in oldNonTerminals1:
        for p1 in oldProds1:
            if p1.leftSide == n1:
                if n1 == initial1:
                    initial1 = str(count)
                p1.leftSide = str(count)
            if len(p1.rightSide) > 1 and p1.rightSide[-1] == n1:
                p1.rightSide = p1.rightSide[0] + str(count)
        count += 1
    count1 = count
    for n2 in oldNonTerminals2:
        for p2 in oldProds2:
            if p2.leftSide == n2:
                if n2 == initial2:
                    initial2 = str(count)
                p2.leftSide = str(count)
            if len(p2.rightSide) > 1 and p2.rightSide[-1] == n2:
                p2.rightSide = p2.rightSide[0] + str(count)
        count += 1
    count2 = count
    #---------------------------------------------------------------------------
    for n1 in range(count1):
        for p1 in oldProds1:
            if p1.leftSide == str(n1):
                if str(n1) == initial1:
                    initial1 = alphabet[n1]
                p1.leftSide = alphabet[n1]
            if len(p1.rightSide) > 1 and p1.rightSide[-1] == str(n1):
                p1.rightSide = p1.rightSide[0] + alphabet[n1]
    for n2 in range(count2):
        for p2 in oldProds2:
            if p2.leftSide == str(n2):
                if str(n2) == initial2:
                    initial2 = alphabet[n2]
                p2.leftSide = alphabet[n2]
            if len(p2.rightSide) > 1 and p2.rightSide[-1] == str(n2):
                p2.rightSide = p2.rightSide[0] + alphabet[n2]

    newProds = []

    for p1 in oldProds1:
        if p1.leftSide == initial1:
            newProds.append=(Production('S', p1.rightSide))
    for p2 in oldProds2:
        if p2.leftSide == initial2:
            newProds.append=(Production('S', p2.rightSide))
    if hasEpsilon:
        newProds.append=(Production('S', '&'))

    newProds = newProds + oldProds1 + oldProds2

    newG = Grammar(newProds, gr1.name + " ∪ " + gr2.name, add)

    return newG

def grammar_concatenation(gr1, gr2, add = False):
    hasEpsilon1 = False
    hasEpsilon2 = False
    oldProds1 = copy.deepcopy(gr1.productions)
    initial1 = copy.deepcopy(gr1.productions[0].leftSide)
    oldNonTerminals1 = set()
    oldProds2 = copy.deepcopy(gr2.productions)
    initial2 = copy.deepcopy(gr2.productions[0].leftSide)
    oldNonTerminals2 = set()
    count = 0
    oldProds1_1 = []
    oldProds2_1 = []
    for p1 in oldProds1:
        if p1.rightSide is not '&':
            oldProds1_1.append=(p1)
        else:
            hasEpsilon1 = True
    oldProds1 = oldProds1_1
    for p2 in oldProds2:
        if p2.rightSide is not '&':
            oldProds2_1.append=(p2)
        else:
            hasEpsilon2 = True
    oldProds2 = oldProds2_1
    for p1 in gr1.productions:
        oldNonTerminals1.add(p1.leftSide)
        if len(p1.rightSide) > 1:
            oldNonTerminals1.add(p1.rightSide[-1])
    for p2 in gr2.productions:
        oldNonTerminals2.add(p2.leftSide)
        if len(p2.rightSide) > 1:
            oldNonTerminals2.add(p2.rightSide[-1])
    #---------------------------------------------------------------------------
    for n1 in oldNonTerminals1:
        for p1 in oldProds1:
            if n1 == initial1:
                continue
            if p1.leftSide == n1:
                p1.leftSide = str(count)
            if len(p1.rightSide) > 1 and p1.rightSide[-1] == n1:
                p1.rightSide = p1.rightSide[0] + str(count)
        count += 1
    count1 = count
    for n2 in oldNonTerminals2:
        for p2 in oldProds2:
            if p2.leftSide == n2:
                if n2 == initial2:
                    initial2 = str(count)
                p2.leftSide = str(count)
            if len(p2.rightSide) > 1 and p2.rightSide[-1] == n2:
                p2.rightSide = p2.rightSide[0] + str(count)
        count += 1
    count2 = count
    #---------------------------------------------------------------------------
    for n1 in range(count1):
        for p1 in oldProds1:
            if p1.leftSide == str(n1):
                if str(n1) == initial1:
                    initial1 = alphabet[n1]
                p1.leftSide = alphabet[n1]
            if len(p1.rightSide) > 1 and p1.rightSide[-1] == str(n1):
                p1.rightSide = p1.rightSide[0] + alphabet[n1]
    for n2 in range(count2):
        for p2 in oldProds2:
            if p2.leftSide == str(n2):
                if str(n2) == initial2:
                    initial2 = alphabet[n2]
                p2.leftSide = alphabet[n2]
            if len(p2.rightSide) > 1 and p2.rightSide[-1] == str(n2):
                p2.rightSide = p2.rightSide[0] + alphabet[n2]
    #initial1 = oldProds1[0].leftSide
    #initial2 = oldProds2[0].leftSide
    if hasEpsilon1 and hasEpsilon2:
        newProdsEpsilon = []
        for p1 in oldProds1:
            if len(p1.rightSide) == 1 and p1.rightSide != '&':
                newProdsEpsilon.append=(Production(p1.leftSide, p1.rightSide + initial2))
            if p1.leftSide == initial1:
                newProdsEpsilon.append=(Production(p1.leftSide, '&'))
                for p2 in oldProds2:
                    if p2.leftSide == initial2:
                        newProdsEpsilon.append=(Production(p1.leftSide, p2.rightSide))
        oldProds1 += newProdsEpsilon
    elif hasEpsilon1 and not hasEpsilon2:
        newProdsEpsilon = []
        for p1 in oldProds1:
            if len(p1.rightSide) == 1:
                p1.rightSide = p1.rightSide + initial2
            if p1.leftSide == initial1:
                for p2 in oldProds2:
                    if p2.leftSide == initial2:
                        newProdsEpsilon.append=(Production(p1.leftSide, p2.rightSide))
        oldProds1 += newProdsEpsilon
    elif not hasEpsilon1 and hasEpsilon2:
        for p1 in oldProds1:
            if len(p1.rightSide) == 1:
                oldProds1.append=(Production(p1.leftSide, p1.rightSide + initial2))
    else:
        for p1 in oldProds1:
            if len(p1.rightSide) == 1:
                p1.rightSide = p1.rightSide + initial2

    newProds = oldProds1 + oldProds2

    newG = Grammar(newProds, gr1.name + "." + gr2.name, add)

    return newG

def grammar_kleene_star(gr, add = False):
    oldProds = copy.deepcopy(gr.productions)
    initial = copy.deepcopy(gr.productions[0].leftSide)
    oldNonTerminals = set()
    count = 0
    for p in oldProds:
        if p.rightSide is '&':
            oldProds1 = []
            for p1 in oldProds:
                if p1 != p:
                    oldProds1.append=(p1)
            break
        oldProds1 = oldProds
    oldProds = oldProds1
    for p in gr.productions:
        oldNonTerminals.add(p.leftSide)
        if len(p.rightSide) > 1:
            oldNonTerminals.add(p.rightSide[-1])
    #---------------------------------------------------------------------------
    for n in oldNonTerminals:
        #print(n)
        for p in oldProds:
            if p.leftSide == n:
                if n == initial:
                    initial = str(count)
                p.leftSide = str(count)
            if len(p.rightSide) > 1 and p.rightSide[-1] == n:
                p.rightSide = p.rightSide[0] + str(count)
        count += 1
    #---------------------------------------------------------------------------
    for n in range(count):
        for p in oldProds:
            if p.leftSide == str(n):
                if str(n) == initial:
                    initial = alphabet[n]
                p.leftSide = alphabet[n]
            if len(p.rightSide) > 1 and p.rightSide[-1] == str(n):
                p.rightSide = p.rightSide[0] + alphabet[n]

    for p in oldProds:
        print(p)
    newProds = []

    for p in oldProds:
        if p.leftSide == initial:
            newProds.append=(Production('S', p.rightSide))
    newProds.append=(Production('S', '&'))
    for p in oldProds:
        if len(p.rightSide) == 1:
            newP = Production(p.leftSide, p.rightSide + initial)
            #if newP not in oldProds:
            oldProds.append=(newP)

    newProds = newProds + oldProds

    newG = Grammar(newProds, gr.name + "*", add)

    return newG
#-----------------------------------------------------------------------
    # def AutToGrammar(automata)
    #     for elem in automata
def AutToGram(Tabela,estadoFinal,estadoInicial):
    gram=[]
    if estadoInicial in estadoFinal:
        prod=estadoInicial + "->"+ 'ε'
        gram.append(prod)
    for elem in Tabela:
        for elem1 in elem.getSecondtSet(): 
            if elem1=='-':
                 continue
            if elem1 in estadoFinal:
                prod=elem.getFirstSet() + "->"+ elem.getSymbole() 
            else:     
                pro=elem.getSymbole()+elem1
                prod=elem.getFirstSet()+ "->" + pro
            gram.append(prod) 
    return gram