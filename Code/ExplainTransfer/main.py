from owlready2 import *

# onto_path.append("/Applications/MAMP/htdocs/")
onto = get_ontology("file://OWL/SWRLrdf.owl").load()
# print(list(onto.classes()))
# print(list(onto.individuals()))
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
# onto.save("/Applications/MAMP/htdocs/SWRLrules.owl")
# with onto:
#     sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True, debug=3)


# onto.save()


def getOntoVal():
    allSentence = ProblemStatement.instances()
    totalSentence = len(allSentence)
    # print(totalSentence)
    allPerson = (Person.instances())
    totalPerson = len(allPerson)
    # print(totalPerson)
    sen = [None for i in range(2)]
    ag = [[None for i in range(8)] for j in range(totalPerson)]
    for problems in ProblemStatement.instances():
        # print(problems)
        sCounter = 0
        aCounter = 0
        # print("----------------------------")
        for sentences in problems.Involves:
            # print(sentences.name)
            sen[sCounter] = sentences.name
            sCounter = sCounter + 1
            for agents in sentences.involvesAjent:
                # print(agents.name)
                ag[aCounter][0] = agents.name
                per = agents.hasQuant[0]
                # print(agents.hasQuant[0].name)
                # print(list(per.quantValue))
                if not per.quantValue:
                    ag[aCounter][1] = None
                    ag[aCounter][2] = None
                else:
                    ag[aCounter][1] = per.quantValue[0]
                    ag[aCounter][2] = per.quantType[0]
                # print(agents.hasGained)
                # print(agents.hasLost)
                properties = agents.get_properties()
                # if not (agents.hasLost[0]).quantValue:
                #     print("lol")
                for prop in properties:
                    x = prop.name
                    # print(x)
                    if x == "hasGained" and (agents.hasGained[0]).quantValue:
                        ag[aCounter][3] = (agents.hasGained[0]).quantValue[0]
                    if x == "hasLost" and (agents.hasLost[0]).quantValue:
                        ag[aCounter][4] = (agents.hasLost[0]).quantValue[0]
                    if x == "transfersTo" and agents.transfersTo[0]:
                        ag[aCounter][5] = (agents.transfersTo[0]).name
                    if x == "hasNewQuant" and (agents.hasNewQuant[0]).quantValue:
                        ag[aCounter][6] = (agents.hasNewQuant[0]).quantValue[0]
                        ag[aCounter][7] = (agents.hasNewQuant[0]).quantType[0]
            aCounter = aCounter + 1
    #         print("--- Sentence End ---")
    #     print("--- Problem End ---")
    # print("########################")
    # print(sen)
    print(ag)
    return ag


# ag[AgentName, x_old, x_old_type, t_gained, t_lost, transfer_to, x_new, x_new_type]
# .......0 ........ 1 .....2 ..........3........4........5..........6........7.......

# ------------------- Function -----------------
def explain(a, qs):
    if a[0][5] is not None:
        tname = a[0][5]
        tvar = a[0][4]
        dir = 0
    elif a[1][5] is not None:
        tname = a[1][5]
        tvar = a[1][4]
        dir = 1
    # if a[0][2] != a[1][2]:
    #     print("Type of transfer NOT SAME !!!!!")
    # else:
    #     ttype = a[0][2]
    if a[0][2] is not None:
        ttype = a[0][2]
    elif a[1][2] is not None:
        ttype = a[1][2]

    print("Conditions:")
    print("Let the initial " + str(a[0][2]) + " with " + str(a[0][0]) + " be x_old")
    print("Initial " + str(a[1][2]) + " with " + str(a[1][0]) + " be y_old")
    print(ttype + " transferred to " + tname + " be t")
    print("current " + str(a[0][2]) + " with " + str(a[0][0]) + " be x_new")
    print("current " + str(a[1][2]) + " with " + str(a[1][0]) + " be y_new")
    print()

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

    if qs == "Agent1":
        val = 0
        opp_val = 1
        var = "x"
        opp_var = "y"
        if a[val][1] is None:
            find = 2
        elif a[val][6] is None:
            find = 6
        if dir == 0:
            op = "-"
            opp_op = "+"
        else:
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
        val = 1
        op = "#"

    print("We need to find " + str(var) + "_new")

    # 2 -> old
    # 6 -> new
    # 8 -> transfer
    # print("var -> " + str(var))
    # print("op -> " + str(op))
    # print("find -> " + str(find))
    # print("dir -> " + str(dir))

    print("Since, we know ")
    if find == 8:
        if a[0][1] is not None and a[0][6] is not None:
            var = "x"
            val = 0
            opp_val = 1
            print("x01 ->" +str(a[0][1]) + " " + str(a[0][6]))
        elif a[1][1] is not None and a[1][6] is not None:
            var = "y"
            val = 1
            opp_val = 0
            print("y01 ->" +str(a[1][1]) + " " + str(a[1][6]))
        # print("var -> " + str(var))

        if (dir == 0 and val == 0) or (dir == 1 and val == 1):
            print("t = " + str(var) + "_old - " + str(var) + "_new ")
            print("t = " + str(a[val][1]) + " - " + str(a[val][6]))
            f = 4
        else:
            print("t = " + str(var) + "_new - " + str(var) + "_old")
            print("t = " + str(a[val][6]) + " - " + str(a[val][1]))
            f = 5
        # f is for gain or loss check
        with onto:
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
        a = getOntoVal()

        tvar = a[val][f]
        print("t = " + str(tvar))
        print()
        print("Hence, transferred books were " + str(tvar))
    # if find == 2:
    #     print(str(var) + "_new = " + str(var) + "_old " + op + " t")
    # elif find == 6:
    else:
        if tvar is None:
            with onto:
                sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
            a = getOntoVal()
            print("t = " + str(opp_var) + "_old - " + str(opp_var) + "_new")
            print("t = " + str(a[opp_val][1]) + " - " + str(a[opp_val][6]))
            tvar = a[val][3]
            print("t = " + str(tvar))
            print("Using t,")
        print(str(var) + "_new = " + str(var) + "_old " + op + " t")
        with onto:
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
        a = getOntoVal()
        if find == 6:
            print(str(var) + "_new = " + str(a[val][1]) + op + str(tvar))
            print(str(var) + "_new = " + str(a[val][6]))
            print()
            print("Hence, " + str(a[val][0]) + " now have " + str(a[val][6]) + " " + str(ttype))
        elif find == 2:
            print(var + "_old = " + str(var) + "_new " + opp_op + " t")
            print(var + "_old = " + str(a[val][6]) + " " + opp_op + " " + str(tvar))
            print(var + "_old = " + str[a[val][1]])
            print()
            print("Hence, " + str(a[val][0]) + " had " + str(a[val][1]) + " " + str(ttype))


# ------------------- Function END -----------------
qs = 'Transfer'
a = getOntoVal()
explain(a=a, qs=qs)
