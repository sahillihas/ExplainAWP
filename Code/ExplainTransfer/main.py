#----------------------------------------------------------------------------
# Created By  : Sahil CS20S017
# Created Date: 01 Aug 2022
# version ='1.0'
# ---------------------------------------------------------------------------
""" Template based Explanation of Transfer based AWP's using Ontology """
# ---------------------------------------------------------------------------

# ---------------------- Imports --------------------------------------------
# Importing OWLReady2 API
# Use "pip install owlready2" if not installed
from owlready2 import *
# ---------------------------------------------------------------------------

onto = get_ontology("file://OWL/SWRLrdf.owl").load()        # Ontology is loaded in the onto object


# Provide the Ontology object we are loading the classes, Parent class is Thing
with onto:
    class ProblemStatement(Thing):
        pass


    class AfterState(Thing):
        pass


    class BeforeState(Thing):
        pass


    class QuestionState(Thing):
        pass


    class TransferState(Thing):
        pass


    class Person(Thing):
        pass


    class Quantity(Thing):
        pass


#######################################################
# FUNCTION - getOntoVal()
# Get the Agents and their values from the Ontology
# Input - Ontology object
# Output - Array of Agents and Values in it
# [ 1. Agent Name,
#   2. Initial Obj Value,
#   3. Initial Obj Type,
#   4. Gain Value,
#   5. Loss Value,
#   6. Transfer to Agent Name,
#   7. New Value Obj Value,
#   8. New Obj Type
# ]
#######################################################
def getOntoVal():
    allPerson = (Person.instances())  # Getting all the instances of Agent
    totalPerson = len(allPerson)  # Counting the number of agents
    count = 0  # Counter for No. of Agents in Array
    # Initialising the 2D array for Agents
    # ag[AgentName, x_old, x_old_type, t_gained, t_lost, transfer_to, x_new, x_new_type]
    ag = [[None for i in range(8)] for j in range(totalPerson)]

    # Structure for iteration
    # ProblemStatement
    #   |
    #   |-- Sentences
    #           |
    #           |-- Person
    #                   |
    #                   | -- Quant
    #                   |       |-- QuantValue
    #                   |       |-- QuantType
    #                   | -- NewQuant
    #                   |       |-- QuantValue
    #                   |       |-- QuantType
    #                   | -- hasLost
    #                   |       |-- QuantValue
    #                   |       |-- QuantType
    #                   | -- hasGained
    #                   |       |-- QuantValue
    #                   |       |-- QuantType
    #                   | -- TransferTo
    #                           |-- Name

    for problems in ProblemStatement.instances():
        for sentences in problems.Involves:
            for agents in sentences.involvesAjent:
                ag[count][0] = agents.name
                per = agents.hasQuant[0]
                if not per.quantValue:
                    ag[count][1] = None
                    ag[count][2] = None
                else:
                    ag[count][1] = per.quantValue[0]
                    ag[count][2] = per.quantType[0]
                properties = agents.get_properties()
                for prop in properties:
                    x = prop.name
                    if x == "hasGained" and (agents.hasGained[0]).quantValue:
                        ag[count][3] = (agents.hasGained[0]).quantValue[0]
                    if x == "hasLost" and (agents.hasLost[0]).quantValue:
                        ag[count][4] = (agents.hasLost[0]).quantValue[0]
                    if x == "transfersTo" and agents.transfersTo[0]:
                        ag[count][5] = (agents.transfersTo[0]).name
                    if x == "hasNewQuant" and (agents.hasNewQuant[0]).quantValue:
                        ag[count][6] = (agents.hasNewQuant[0]).quantValue[0]
                        ag[count][7] = (agents.hasNewQuant[0]).quantType[0]
            count = count + 1
    # print(ag)
    return ag


#################################################################################
# FUNCTION - explain()
# Explanation on given and inferred values
# INPUT - 1. Given Values of Ontology in Array a
#         2. Find value for ?
# OUTPUT - Printing the explanation on the basis of pre-defined templates
#################################################################################
def explain(a, qs):
    # tname - Transfer to Agent (Name)
    # ttype - Object Type in Transfer
    # tvar - Value of Transfer
    # dir - 0 = x -> y
    #       1 = y -> x

    # Getting Transfer name, value and direction
    if a[0][5] is not None:
        tname = a[0][5]
        tvar = a[0][4]  # tvar = Gain Value
        dir = 0
    elif a[1][5] is not None:
        tname = a[1][5]
        tvar = a[1][4]
        dir = 1  # tvar = Gain Value

    # Getting Type of object transfer
    if a[0][2] is not None:
        ttype = a[0][2]
    elif a[1][2] is not None:
        ttype = a[1][2]

    # --------------- Template for Conditions ---------------
    print("Conditions:")
    print("Let the initial " + str(a[0][2]) + " with " + str(a[0][0]) + " be x_old")
    print("Initial " + str(a[1][2]) + " with " + str(a[1][0]) + " be y_old")
    print(ttype + " transferred to " + tname + " be t")
    print("current " + str(a[0][2]) + " with " + str(a[0][0]) + " be x_new")
    print("current " + str(a[1][2]) + " with " + str(a[1][0]) + " be y_new")
    # -------------------------------------------------------

    # --------------- Template for Conditions ---------------
    print("Given that,")
    if a[0][1] is not None:
        print("x_old = " + str(a[0][1]))
    if a[0][6] is not None:
        print("x_new = " + str(a[0][6]))
    if a[1][1] is not None:
        print("y_old = " + str(a[1][1]))
    if a[1][6] is not None:
        print("y_new = " + str(a[1][6]))
    if tvar is not None:
        print("t = " + str(tvar))
    print()
    # -------------------------------------------------------

    # Checking what is asked in question
    # val = 0 - Agent1, 1 - Agent2
    # opp_val = 0 - Agent1, 1 - Agent2
    # var = x - Agent 1, y - Agent2
    # opp_var = x - Agent 1, y - Agent 2
    # op = Operator to be used depending on the direction of transfer and cases
    if qs == "Agent1":
        val = 0
        opp_val = 1
        var = "x"
        opp_var = "y"
        if a[val][1] is None:
            find = 2
        elif a[val][6] is None:
            find = 6
        if dir == 0:        # x -> y, hence loss for x thereby op = -
            op = "-"
            opp_op = "+"
        else:               # x <- y, hence gain for x thereby op = +
            op = "+"
            opp_op = "-"
    elif qs == "Agent2":
        val = 1
        opp_val = 0
        var = "y"
        opp_var = "x"
        if a[val][6] is None:
            find = 6
        elif a[val][1] is None:
            find = 2
        if dir == 1:
            op = "-"
            opp_op = "+"
        else:
            op = "+"
            opp_op = "-"
    elif qs == "Transfer":
        find = 8
        var = "t"
        val = 1         # Randomly set between 0 and 1

    # --------------- Template for To Find ---------------
    print("We need to find " + str(var) + "_new")
    # ----------------------------------------------------

    # --------------------- Solution ---------------------
    print("Since, we know ")
    if find == 8:                    # Transfer Value
        if a[0][1] is not None and a[0][6] is not None:
            var = "x"
            val = 0
        elif a[1][1] is not None and a[1][6] is not None:
            var = "y"
            val = 1

        if (dir == 0 and val == 0) or (dir == 1 and val == 1):
            print("t = " + str(var) + "_old - " + str(var) + "_new ")
            print("t = " + str(a[val][1]) + " - " + str(a[val][6]))
            f = 4
        else:
            print("t = " + str(var) + "_new - " + str(var) + "_old")
            print("t = " + str(a[val][6]) + " - " + str(a[val][1]))
            f = 5
        # f is for gain or loss check

        # Using reasoner on our ontology
        with onto:
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
        a = getOntoVal() # Using the infer results in our array for solution

        tvar = a[val][f]
        print("t = " + str(tvar))
        print()
        print("Hence, transferred books were " + str(tvar))
    else:
        reasonerRan = False         # Will check if reasoner already ran or not
        if tvar is None:
            with onto:
                sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
            a = getOntoVal()
            print("t = " + str(opp_var) + "_old - " + str(opp_var) + "_new")
            print("t = " + str(a[opp_val][1]) + " - " + str(a[opp_val][6]))
            tvar = a[val][3]
            print("t = " + str(tvar))
            print("Using t,")
            reasonerRan = True
        print(str(var) + "_new = " + str(var) + "_old " + op + " t")
        if not reasonerRan:
            with onto:
                sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
            a = getOntoVal()
        if find == 6:  # New Value
            print(str(var) + "_new = " + str(a[val][1]) + op + str(tvar))
            print(str(var) + "_new = " + str(a[val][6]))
            print()
            print("Hence, " + str(a[val][0]) + " now have " + str(a[val][6]) + " " + str(ttype))
        elif find == 2:  # Old Value
            print(var + "_old = " + str(var) + "_new " + opp_op + " t")
            print(var + "_old = " + str(a[val][6]) + " " + opp_op + " " + str(tvar))
            print(var + "_old = " + str[a[val][1]])
            print()
            print("Hence, " + str(a[val][0]) + " had " + str(a[val][1]) + " " + str(ttype))

    # -------------------------------------------------------


# ------------------- Function END -----------------

qs = 'Transfer'
a = getOntoVal()
explain(a=a, qs=qs)
