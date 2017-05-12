# CSCI-561 2017S Homework3
# Student Name: Chaoran Lu
# Student ID: 6524-2400-52
# Email: luchaora@usc.edu
# Algorithm: Variable Elimination Algorithm for inference in Bayesian networks(AIMA Figure 14.11)
# Reference Sample code: https://github.com/aimacode/aima-python/blob/master/probability.py

# ##################### MAKE_FACTOR ###########################
# Return the factor for var in bn's joint distribution given e.
def make_factor(varLcr, graphNode):
    combFac = []
    comb1 = []
    for i in graphNode:
        if varLcr in i[0]:
            comb1.append(i)
    # DEBUG
    # print comb1

    # Build a position dictionary for reference
    # [[A, B],{++: 0.6, -+: 0.4, +-: 0.3, --: 0.7} -> {A: 0, B: 1}]
    posiDic = []
    for i1 in comb1:
        subposiDic = {}
        for i2 in i1[0]:
            subposiDic[i2] = i1[0].index(i2)
        posiDic.append(subposiDic)
    # DEBUG
    # print posiDic

    # Build the variable list and the new factor table
    varlist = []
    for j1 in comb1[0][0]:
        varlist.append(j1)
    for j2 in range(0, len(comb1)):
        for j3 in comb1[j2][0]:
            if j3 != varLcr:
                varlist.append(j3)
    # DEBUG
    # print varlist
    varlist = list(set(varlist))
    numPower = len(varlist)
    dictEle = {}
    for k1 in range(0, pow(2, numPower)):
        # dictEle = {}
        dictEleSub = {}
        # This is a reference code from:
        # Website: http://doc.sagemath.org/html/en/thematic_tutorials/tutorial-programming-python.html
        tmp = [((k1 >> x) & 1) for x in range(numPower)]
        # DEBUG
        # print bitToStr(tmp)
        tmp1 = bitToStr(tmp)
        # Build a dictionary such as {A:+, B:-, C:+} from "+-+"
        for k2 in varlist:
            dictEleSub[k2] = tmp1[varlist.index(k2)]
        # From [[[A, B, C], {}], [[C, D], {}]] to [[A, B, C, D, E], {}]
        # To get each probability in {}, I multiply f1 * f2
        myProduct = 1
        for k3 in comb1:
            oneKey = ""
            for k4 in k3[0]:
                oneKey = oneKey + dictEleSub[k4]
            oneVal = k3[1][oneKey.strip("")]
            myProduct = myProduct * oneVal
        dictEle[tmp1] = myProduct

    combFac.append(varlist)
    combFac.append(dictEle)

    return combFac

# ##################### UPDATE THE FACTOR LIST ############
def updateFaclist(valLcr, fclist):
    result = []
    for i in fclist:
        if valLcr not in i[0]:
            result.append(i)
    return result

# ##################### Sum-Out A Variable from a Factor ###########################
def sum_out_factor(delvar, myFactor, eviDic):
    result = []
    # In myFactor1, the variable to del would be moved to the right bottom of the string
    myFactor1 = configFactor(delvar, myFactor)
    # DEBUG
    # print myFactor
    # print myFactor1
    varlist = []
    for i1 in myFactor[0]:
        if i1 != delvar:
            varlist.append(i1)

    numPower = len(varlist)
    dictEle = {}
    if eviDic != 0 and eviDic.has_key(delvar):
        if eviDic[delvar] == "+":
            for k1 in range(0, pow(2, numPower)):
                tmp = [((k1 >> x) & 1) for x in range(numPower)]
                tmp1 = bitToStr(tmp)
                dictEle[tmp1] = myFactor1[1][tmp1 + "+"]
        else:
            for k1 in range(0, pow(2, numPower)):
                tmp = [((k1 >> x) & 1) for x in range(numPower)]
                tmp1 = bitToStr(tmp)
                dictEle[tmp1] = myFactor1[1][tmp1 + "-"]
    else:
        for k1 in range(0, pow(2, numPower)):
            tmp = [((k1 >> x) & 1) for x in range(numPower)]
            tmp1 = bitToStr(tmp)
            dictEle[tmp1] = myFactor1[1][tmp1 + "+"] + myFactor1[1][tmp1 + "-"]


    result.append(varlist)
    result.append(dictEle)
    # DEBUG
    # print result
    return result

########################################################
# This Function is used to normalize the probability
def normalize_prob(fac):
    resultFac = []
    varlist = fac[0][0]
    numPower = len(varlist)
    myValues = fac[0][1].values()

    mySum = 0
    for i in myValues:
        mySum = mySum + i

    dictEle = {}
    for k1 in range(0, pow(2, numPower)):
        tmp = [((k1 >> x) & 1) for x in range(numPower)]
        tmp1 = bitToStr(tmp)
        dictEle[tmp1] = fac[0][1][tmp1]/mySum

    resultFac.append(varlist)
    resultFac.append(dictEle)

    return resultFac

########################################################
# Calculate the Probability(Using Elimination Algorithm)
def calculateP(query, graphNode, varlist):

    # a list of query variables
    queryVar = query[0].keys()

    # a dic of evidences
    if len(query) == 2:
        eviDic = query[1]
    else:
        eviDic = 0

    # DEBUG
    # print queryVar

    # get the orderlist
    orderlist = []
    for i in varlist:
        if i not in queryVar:
            orderlist.append(i)
    # DEBUG
    # print orderlist

    factorList = []
    for j in graphNode:
        factorList.append(j)

    for k in orderlist:
        # print factorList
        # Make_Factor Operation
        mFactor = make_factor(k, factorList)

        # SUM_OUT Operation
        sFactor1 = sum_out_factor(k, mFactor, eviDic)

        # Update the factor list
        factorList = updateFaclist(k, factorList)
        factorList.append(sFactor1)

    # DEBUG
    # print queryVar
    for l in queryVar:
        # Make_Factor Operation
        fac1 = make_factor(l, factorList)

        # Update the factor list
        factorList = updateFaclist(l, factorList)
        factorList.append(fac1)

    result1 = normalize_prob(factorList)
    return result1

################################
# Calculate the Expected Utility
def calculateEU(query, graphNode, varlist, utilTable):

    evid = query[1]

    var_Com = list(set(query[0].keys()) & set(query[1].keys()))
    sign_Com = [query[1][v] for v in var_Com]
    sign_Com = ''.join(sign_Com)

    newGraph = []
    for n in graphNode:
        newNode = []
        vars = [v for v in n[0]]
        val = {}
        for kv in n[1].keys():
            val[kv] = n[1][kv]
        newNode.append(vars)
        newNode.append(val)
        newGraph.append(newNode)

    for node in newGraph:
        for e in evid.keys():
            if e == node[0][0]:
                if (evid[e] == '+'):
                    node[1]['+'] = 1
                    node[1]['-'] = 0
                else:
                    node[1]['+'] = 0
                    node[1]['-'] = 1

    tresult = calculateP(query, newGraph, varlist)


    pVar = tresult[0]
    uVar = utilTable[0]

    pTable = tresult[1]
    uTable = utilTable[1]
    print tresult
    print utilTable

    sum = 0


    for k in pTable.keys():
        k_T = ''
        k_T = [k_T + k[pVar.index(v)]for v in uVar]
        k_T = ''.join(k_T)

        k_C = ''
        k_C = [k_C + k[var_Com.index(v)] for v in var_Com]
        k_C = ''.join(k_C)

        #if k_C == sign_Com:
        sum = sum + pTable[k]*uTable[k_T]
    #resultEU = utilTable[1]["+"] * tresult[1]["+"] + utilTable[1]["-"] * tresult[1]["-"]

    return sum

###############################
# Calculate the Maximum Utility
def calculateMEU(query, graphNode, varlist, utilTable):

    results = []

    # print query
    qContent = query[4:len(query) - 1].split("|")
    qContent1 = []
    for i in qContent:
        qContent1.append(i.strip())
    # decision nodes
    deci = qContent1[0].replace(' ','').split(",")
    deciNum = len(deci)

    # Iterate all kinds of conditions of decision nodes
    for j in range(0, pow(2, deciNum)):
        singleAnswer = []
        euQuery = []
        qDict = {}
        tmp = [((j >> x) & 1) for x in range(deciNum)]
        tmp1 = bitToStr(tmp)
        for j1 in range(0, deciNum):
            qDict[deci[j1]] = tmp1[j1]

        if len(qContent1) == 2:
            evi = qContent1[1].split(",")
            for j2 in range(0, len(evi)):
                eviEle = evi[j2].split(" ")
                qDict[eviEle[0]] = eviEle[2]

        uDict = {}
        pNode = utilTable[0]
        for k in pNode:
            uDict[k] = 1

        euQuery.append(uDict)
        euQuery.append(qDict)

        euVal = calculateEU(euQuery, graphNode, varlist, utilTable)
        singleAnswer.append(euVal)
        singleAnswer.append(tmp1)
        results.append(singleAnswer)

    # print results
    max = 0
    ans =  ''
    for r in results:
        if r[0] > max:
            max = r[0]
            ans = r[1]
    max = int(round(max,0))
    ret = []
    ret.append(max)
    ret.append(ans)
    return ret

# Configure a probability query
# from String: 'P(A = +)' to list[dict]: [{'A': '+'}]
# from String: 'P(A = + , B = -)' to list[dict]: [{'A': '+', 'B': '-'}]
# from String: 'P(A = + | B = +, C = -)'  to list[dict, dict]: [{'A': '+'}, {'B': '+', 'C': '-'}]
def pqueryConfig(query):
    # remove parenthesis
    tmp1 = query[2: len(query) - 1]
    tmp2 = tmp1.split("|")
    result = []
    configQuery = []
    if (len(tmp1.split("|")) == 1):
        tmp3 = tmp2[0].split(",")
        result.append(delSpace(tmp3))
    else:
        tmp3 = tmp2[0].split(",")
        tmp4 = tmp2[1].split(",")
        result.append(delSpace(tmp3))
        result.append(delSpace(tmp4))
    if len(result) == 1:
        queryDict = {}
        for i in result[0]:
            x1 = i.split(" ")
            queryDict[x1[0]] = x1[2]
        configQuery.append(queryDict)
    else:
        queryDict = {}
        eviDict = {}
        for j in result[0]:
            x2 = j.split(" ")
            queryDict[x2[0]] = x2[2]
        configQuery.append(queryDict)
        for k in result[1]:
            x3 = k.split(" ")
            eviDict[x3[0]] = x3[2]
        configQuery.append(eviDict)
    return configQuery

# Configure a EU query
def pqueryConfigE(eu, utilTable):
    # remove parenthesis
    tmp1 = eu[3: len(eu) - 1]
    tmp2 = tmp1.split("|")
    result = []
    configQuery = []
    if (len(tmp1.split("|")) == 1):
        tmp3 = tmp2[0].split(",")
        result.append(delSpace(tmp3))
    else:
        tmp3 = tmp2[0].split(",")
        tmp4 = tmp2[1].split(",")
        result.append(delSpace(tmp3))
        result.append(delSpace(tmp4))
    if len(result) == 1:
        eviDict = {}
        for i in result[0]:
            x1 = i.split(" ")
            eviDict[x1[0]] = x1[2]
        configQuery.append(eviDict)
    else:
        eviDict = {}
        for j in result[0]:
            x2 = j.split(" ")
            eviDict[x2[0]] = x2[2]
        for k in result[1]:
            x3 = k.split(" ")
            eviDict[x3[0]] = x3[2]

    configQuery1 = []
    parentDict = {}
    for x in utilTable[0]:
        parentDict[x] = 1
    configQuery1.append(parentDict)
    configQuery1.append(eviDict)
    # print configQuery1
    return configQuery1

# Configure a node
# from [line1, line2, ...]
# to [Name of Node(string), Parent Nodes(list), contentline(string(no parent)/dict), ...] in another word:
# neonode[0] == Name of Node (nodeName)
# neonode[1] == Name of Parant Nodes (parantNodeName)
# if the node has no parent, neonode[1] == "0"
# for every contentline dict, {Key(string): Value(probability string)} in another word:
# contentline[0] == probability(string)

def configNode(node):
    headline = node[0]
    h1 = headline.split("|")
    nodeName = h1[0].replace(" ", "")
    if len(h1) > 1:
        parentNodeName = h1[1].split()

    neoNode = []
    neoNode.append(nodeName)
    if len(headline) == 1:
        neoNode.append("0")
    else:
        neoNode.append(parentNodeName)

    if node[1] == "decision":
        neoNode.append({'+': 1, '-': 1})
        neoNode.append("decision")
    else:
        if len(node) == 2:
            neoNode.append({'+': float(node[1]), '-': 1 - float(node[1])})
        else:
            contentline = {}
            for j in range(1, len(node)):
                tmp = node[j].split()
                valueLcr = tmp[0]
                keyLcr1 = "+"
                keyLcr2 = "-"
                for k in range(1, len(tmp)):
                    keyLcr1 = keyLcr1 + tmp[k]
                    keyLcr2 = keyLcr2 + tmp[k]
                numLcr = float(valueLcr)
                contentline[keyLcr1] = numLcr
                # contentline[keyLcr2] = round(1-numLcr, 2)
                contentline[keyLcr2] = 1 - numLcr
            neoNode.append(contentline)
    return neoNode

# Helper: Congfigure the myFactor, put the "to be deleted element" to the right side
# e.x [[A, B, C, D], {}] and B -> [[A, C, D, B], {}]
def configFactor(myVar, myFactor):
    myFactor1 = []
    posiDelval = myFactor[0].index(myVar)
    varlist = []
    for i1 in myFactor[0]:
        if i1 != myVar:
            varlist.append(i1)
    varlist.append(myVar)

    newDic = {}
    numPower = len(myFactor[0])
    for k1 in range(0, pow(2, numPower)):
        tmp = [((k1 >> x) & 1) for x in range(numPower)]
        # DEBUG
        # print bitToStr(tmp)
        tmp1 = bitToStr(tmp)
        newDic[mvToEnd(posiDelval, tmp1)] = myFactor[1][tmp1]

    myFactor1.append(varlist)
    myFactor1.append(newDic)
    return myFactor1

# Helper: Delete extra space in each element of a list
# e.x. [1 + 1 , 2 + 2   ] -> [1 + 1,2 + 2]
def delSpace(list):
    result = []
    for i in list:
        result.append(i.strip())
    return result

# Helper: [1, 0, 1] -> "+-+"
def bitToStr(bitlist):
    result = " "
    for i in bitlist:
        if i == 1:
            result = result + "+"
        else:
            result = result + "-"
    return result.strip(" ")

# Helper: move a char in a string and put it to the end of the string
# 'abcd' 1 -> 'acdb'
def mvToEnd(pois, myStr):
    return myStr[0:pois] + myStr[pois + 1 :] + myStr[pois]

# DEBUG: print out a list line by line
def printOutList(a):
    for i in a:
        print i

def main():
    # This line of code is used to read the input.txt
    infile = open('input.txt', 'r')

    # read the input file and put it into a list, each element is a string
    tmp = infile.readlines()

    # get rid of "\n" in the tmp list
    inputInfo = []
    for x in tmp:
        x = x.strip()
        inputInfo.append(x)

    # separate the query, tables and utility if possible
    numSixStar = 0
    querylist = []
    tablelist = []
    utilitylist = []

    for y in inputInfo:
        if(y != '******' and numSixStar == 0):
            querylist.append(y)

        if (y != '******' and numSixStar == 1):
            tablelist.append(y)

        if (y != '******' and numSixStar == 2):
            utilitylist.append(y)

        if (y == '******'):
            numSixStar = numSixStar + 1

    # ##### Build the node graph based on tablelist ##### #
    graphNode = []
    node = []
    tablelist.append("***")
    for i in tablelist:
        if (i != '***'):
            node.append(i)

        if (i == '***'):
            # configure the node elements in the chance node
            Node1 = configNode(node)
            Node2 = []
            if Node1[1] == '0':
                Node2.append([Node1[0]])
                Node2.append(Node1[2])
            else:
                p1 = []
                p1.append(Node1[0])
                for n1 in Node1[1]:
                    p1.append(n1)
                Node2.append(p1)
                Node2.append(Node1[2])
            graphNode.append(Node2)
            node = []

    # DEBUG:
    # printOutList(graphNode)

    # print utilitylist
    # ##### Deal with utility list, if there would be some ##### #
    utilTable = []
    if len(utilitylist) != 0:
        # utilVar = []
        utiltmp = utilitylist[0].split("|")[1]
        utiltmp1 = utiltmp[1:]
        # utilVar.append(utiltmp1.split(" "))
        utilVar = utiltmp1.split(" ")
        # print utilVar

        utilDic = {}
        for z in range(1, len(utilitylist)):
            utiltmp2 = utilitylist[z].split(" ")
            keys = ''
            keys = [keys + utiltmp2[i][0] for i in range(1,len(utiltmp2))]
            keys = ''.join(keys)
            #    utiltmp2[1]+utiltmp2[2]
            utilDic[keys] = float(utiltmp2[0])
        utilTable.append(utilVar)
        utilTable.append(utilDic)
    # DEBUG
    # print utilTable

    # set the result variable
    result = []

    outfile = open('output.txt','w')
    # ##### Handle queries ##### #
    # Put all the nodes in a list, this is the elimination order
    varList = []
    for el in graphNode:
        varList.append(el[0][0])

    for j in range(0, len(querylist)):
        # DEBUG
        # print queryLcr
        if (querylist[j][0] == "P"):
            queryLcrP = pqueryConfig(querylist[j])
            resultP = calculateP(queryLcrP, graphNode, varList)
            checklist = queryLcrP[0].values()
            mkey = ""
            for var_q in resultP[0]:
                mkey = mkey + queryLcrP[0][var_q]


            result2 = resultP[1][mkey]
            result.append(round(result2, 2))
            outputl = str('{0:.2f}'.format(result2))
            outfile.write(outputl+'\n')
        if (querylist[j][0] == "E"):
            queryLcrE = pqueryConfigE(querylist[j], utilTable)
            # print queryLcrE
            resultEU = calculateEU(queryLcrE, graphNode, varList, utilTable)
            result.append(int(round(resultEU, 0)))
            outputl = str(int(round(resultEU, 0)))
            outfile.write(outputl+'\n')

        if (querylist[j][0] == "M"):
            resultMEU = calculateMEU(querylist[j], graphNode, varList, utilTable)
            result.append(resultMEU)

            decision = resultMEU[1]
            str_out = ''
            for i in range(len(decision)):
                str_out = str_out + decision[i] + ' '

            outfile.write(str_out)

            outputl =str(int(resultMEU[0]))+'\n'
            outfile.write(outputl)

    outfile.close()
    # Data post-processing for the result
    # print result
    # This line of code is used to create the output.txt
    # outfile = open('output.txt', 'w')
    # outfile.write()

if __name__ == "__main__": main()