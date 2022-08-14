# ----------------------------------------------------------------------------
# Created By  : Sahil CS20S017
# Created Date: 14 Aug 2022
# version ='1.0'
# ---------------------------------------------------------------------------
""" Template based Explanation of Age Word Problems using Ontology """
# ---------------------------------------------------------------------------

# ---------------------- Imports --------------------------------------------
# Importing OWLReady2 API
# Use "pip install owlready2" if not installed
from owlready2 import *

# ---------------------------------------------------------------------------

onto = get_ontology("file://OWL/AgeSolver.owl").load()  # Ontology is loaded in the onto object

# Provide the Ontology object we are loading the classes, Parent class is Thing
with onto:
    class Agent(Thing):
        pass


    class agentAge(Thing):
        pass


    class ageWordProblem(Thing):
        pass


    class invalidNumEquation(ageWordProblem):
        pass


    class Equation(Thing):
        pass


    class Grammar(Thing):
        pass


    class basicOpGrammar(Grammar):
        pass


    class multipleOpGrammar(Grammar):
        pass


    class invalidAgentAge(Thing):
        pass


    class invalidAgeWordProblem(Thing):
        pass


    class invalidNumEquation(Thing):
        pass


    class invalidProductOperation(Thing):
        pass


    class invalidSumOperation(Thing):
        pass


    class Offset(Thing):
        pass


    class Operand(Thing):
        pass


    class agentAge(Operand):
        pass


    class Number(Operand):
        pass


    class validAgentAge(Operand):
        pass


    class Operation(Thing):
        pass


    class operationWithConstant(Operation):
        pass


    class operationWithoutConstant(Operation):
        pass


    class Question(Thing):
        pass


    class timeInstance(Thing):
        pass


    class validAgentAge(Thing):
        pass

ag = [[None for i in range(8)] for j in range(2)]
linearEq = [[None for i in range(9)] for j in range(2)]
ag[0][1] = 'x'
ag[1][1] = 'y'
aName = [1, 2]
i = 0
for agents in Agent.instances():
    ag[i][0] = agents.hasName
    i = i + 1
qsName = (Question.instances())[0].computeAgentAge[0].involvesAgent[0].hasName
qsOffset = (Question.instances())[0].computeAgentAge[0].atTime.hasOffset
if qsName == ag[0][0]:
    qs = 0
else:
    qs = 1
verb = " "
if qsOffset > 0:
    verb = ' after '
elif qsOffset < 0:
    verb = ' before '
print(qsOffset)

countI = 0
signCount = 4
countTime = 2
for eq in Equation.instances():
    print(eq.name)
    countJ = 0
    linearEq[countI][countJ] = eq.hasSignedFactor1
    countJ += 1

    linearEq[countI][countJ] = "x"
    countJ += 1

    linearEq[countI][countJ] = eq.hasOperand1.atTime.hasOffset
    countJ += 1

    if eq.hasOperation.name == "S1":
        linearEq[countI][countJ] = "+"
    elif eq.hasOperation.name == "D1":
        linearEq[countI][countJ] = '-'
    countJ += 1

    linearEq[countI][countJ] = eq.hasSignedFactor2
    countJ += 1

    linearEq[countI][countJ] = "y"
    countJ += 1

    linearEq[countI][countJ] = eq.hasOperand2.atTime.hasOffset
    countJ += 1

    linearEq[countI][countJ] = "="
    countJ += 1

    linearEq[countI][countJ] = eq.hasConstant

    countI += 1

print(ag)
print(linearEq)

print("Conditions")
print("Let the age of " + str(aName[0]) + " be x ")
print("Let the age of " + str(aName[1]) + " be y ")
if qsOffset == 0:
    print("To find the current age of " + str(ag[qs][0]))
    print("Such that to find value of " + str(ag[qs][1]))
else:
    print("To find the current age of " + str(ag[qs][0]) + verb + str(qsOffset) + " years")
print("Given that ")
state = ["" for i in range(2)]
t = 0
opFlag = False
count = 0
for t in range(2):
    opFlag = False
    count = 0
    for u in range(2):
        if linearEq[t][count] != 0:
            state[t] += " ( " + str(linearEq[t][count]) + " ) * "
        count += 1
        if linearEq[t][count + 1] == 0:
            state[t] += str(linearEq[t][count])
        else:
            state[t] += "( " + str(linearEq[t][count]) + " + "
            count += 1
            state[t] += str(linearEq[t][count]) + " ) "
            count += 1
        if opFlag is False:
            state[t] += " " + str(linearEq[t][3])
            opFlag = True
            count = 4
    state[t] += str(linearEq[t][7]) + " " + str(linearEq[t][8])

print(state[0])
print(state[1])

print("Using Cross Multiplication method for solving two equations" )
print("x = (b1*c2 - b2*c1)/(b2*a1 - b1*a2)")
print("y = (c1*a2 - c2*a1)/(b2*a1 - b1*a2)")
