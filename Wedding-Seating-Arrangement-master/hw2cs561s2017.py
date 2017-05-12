# CSCI-561 2017S Homework2
# Student Name: Chaoran Lu
# Student ID: 6524-2400-52
# Email: luchaora@usc.edu
# References:
# 1. To learn how DPLL would work
# URL: http://www.dis.uniroma1.it/~liberato/ar/dpll/dpll.html
# 2. Reference for Python implementation 1
# URL: https://github.com/asgordon/DPLL.git
# 3. Reference for Python implementation 2
# URL: http://aima.cs.berkeley.edu/python/logic.html
####################################################

# # This global variable is used to contain the relationship matrix
myTrack = []

# DPLL Algorithm
def CheckNotEmpty(s):
    for i in range(0, len(s)):
        c = s[i]
        if not c:
            return False
    return True

def DPLLSAT(s):
    # for i4 in range(0, len(s)):
    #     print s[i4]
    # print "***************"
    global myTrack

    # Base case 1
    if len(s) == 0:
        return True

    # Base case 2
    for i in range(0, len(s)):
        c = s[i]
        if not c:
            return False


    neos = []
    # Pure Literal Assign
    pure_literal_clause = find_pure_symbol(s)
    if pure_literal_clause != []:
        neos = pure_literal_assign(s, pure_literal_clause[0])

    if not CheckNotEmpty(neos):
        return False

    tmp = []
    if neos != []:
        tmp = neos
    else:
        tmp = s

    # Unit-Propagation
    unit_clause = find_unit_clause(tmp)
    if unit_clause != []:
        neos = unit_prop(tmp, unit_clause[0])

    if not CheckNotEmpty(neos):
        return False

    clause1 = []
    tmp1 = []
    if neos == []:
        clause1 = copy_clause(s[0][0], clause1)
        tmp1 = s
    else:
        clause1 = copy_clause(neos[0][0], clause1)
        tmp1 = neos

    # Recursive rule
    tmp2 = []
    tmp2 = copy_clause(tmp1, tmp2)
    if DPLLSAT(unit_prop(tmp1, clause1)):
        if pure_literal_clause:
            myTrack.append(pure_literal_clause[0])

        if unit_clause:
            myTrack.append(unit_clause[0])

        myTrack.append(clause1)
        return True
    else:
        clause2 = []
        clause2 = copy_clause(tmp1[0][0], clause2)
        clause2[0] = -clause2[0]
        # neos2 = []
        # for i in range(0, len(neos)):
        #     if delClause(tmp1[i], clause2):
        #         continue
        #     neos2.append(tmp1[i])
        if DPLLSAT(unit_prop(tmp2, clause2)):

            if pure_literal_clause:
                myTrack.append(pure_literal_clause[0])

            if unit_clause:
                myTrack.append(unit_clause[0])

            myTrack.append(clause2)
            return True
    return False

def find_unit_clause(s):
    result = []
    for i in range(0, len(s)):
        if len(s[i]) == 1:
            result.append(s[i][0])
    return result

# Delete all the clauses in s, which may contain unit_clause
def unit_prop(s, clause):
    result = []
    # Delete all the lines which contains a unit_clause
    for i in range(0, len(s)):
        if containClause(s[i], clause):
            continue
        result.append(s[i])

    result1 = []
    clause1 = []
    clause1 = copy_clause(clause, clause1)
    # Delete all the causes whose symbols are reverse number of unit clauses
    clause1[0] = - clause[0]
    for i in range(0, len(result)):
        sentence = []
        for j in range(0, len(result[i])):
            if result[i][j][0] == clause1[0] and result[i][j][1] == clause1[1] and result[i][j][2] == clause1[2]:
                if len(result[i]) == 1:
                    result1.append([])
                    break
                else:
                    continue
            sentence.append(result[i][j])
        if sentence != []:
            result1.append(sentence)
    return result1

def find_pure_symbol(s):

    posiArr = []
    negaArr = []
    result = []

    for i in range(0, len(s)):
        for j in range(0, len(s[i])):
            if s[i][j][0] == 1:
                posiArr.append(s[i][j])
            elif s[i][j][0] == -1:
                negaArr.append(s[i][j])

    for k in range(0, len(posiArr)):
        flag1 = 0
        for l in range (0, len(negaArr)):
            if posiArr[k][1] == negaArr[l][1] and posiArr[k][2] == negaArr[l][2]:
                flag1 = 100
        if flag1 == 0:
            result.append(posiArr[k])

    for m in range(0, len(negaArr)):
        flag2 = 0
        for n in range (0, len(posiArr)):
            if posiArr[n][1] == negaArr[m][1] and posiArr[n][2] == negaArr[m][2]:
                flag2 = 100
        if flag2 == 0:
            result.append(negaArr[m])

    return result

def pure_literal_assign(s, clause):
    neos = []
    for i in range(0, len(s)):
        if containClause(s[i], clause):
            continue
        neos.append(s[i])

    return neos

def delClause(c1, c2):
    for i in range(0, len(c1)):
        if c1[i][0] == c2[0] and c1[i][1] == c2[1] and c1[i][2] == c2[2]:
            return True
    return False

# Copy everything in clause1 and paste it to clause2
def copy_clause(clause1, clause2):
    for k in range(0, len(clause1)):
        clause2.append(clause1[k])
    return clause2

def containClause(c1, c2):
    for i in range(0, len(c1)):
        if c1[i][0] == c2[0] and c1[i][1] == c2[1] and c1[i][2] == c2[2]:
            return True
    return False

def main():
    # This line of code is used to read the input.txt
    infile = open('input.txt', 'r')

    # read the input file and put it into a list, each element is a string
    tmp = infile.readlines()
    line = tmp[0].split()
    guestNum = int(line[0])
    tableNum = int(line[1])

    # The relationship between the elements of s is "and"
    s = []
    # For each guest a, the assignment should be at only one table
    # The relationship between the elements of clause is "or"
    for i in range(0, guestNum):
        clause = []
        clause1 = [i + 1]

        for j in range(0, tableNum):
            clause2 = []
            for k in range(0, len(clause1)):
                clause2.append(clause1[k])
            clause2 = copy_clause(clause1, clause2)
            if len(clause2) != 1:
                clause2.pop()
            clause2.extend([j + 1])
            clause2.insert(0, 1)
            clause.append(clause2)
        s.append(clause)

    # For each pair of friends, guest  a and guest  b. a and b should sit at the same table.
    # For each pair of enemies, guest  a and guest  b. a and b should not sit at the same table
    # The relationship between clause3 clause4 and clause5 is "and"
    # The relationship within clause3 clause4 and clause5 is "or"
    satLen = len(tmp)
    for i1 in range(1, satLen):
        line2 = tmp[i1].split()
        a = int(line2[0])
        b = int(line2[1])
        if line2[2] == "F":
            for j1 in range(0, tableNum):
                clause3 = [[-1, a, j1 + 1], [1, b, j1 + 1]]
                s.append(clause3)
                clause4 = [[1, a, j1 + 1], [-1, b, j1 + 1]]
                s.append(clause4)
        else:
            for j1 in range(0, tableNum):
                clause5 = [[-1, a, j1 + 1], [-1, b, j1 + 1]]
                s.append(clause5)

    # for i4 in range(0, len(s)):
    #     print s[i4]
    #s = [[1,2,3],[]]
    torF = DPLLSAT(s)

    outputl = ""
    if torF:
        track = []
        for i2 in range(0, len(myTrack)):
            if myTrack[i2][0] == 1:
                track.append(myTrack[i2])
        sch = []
        for j2 in range(0, guestNum):
            sch.append(0)
        for i3 in range(0, len(track)):
            sch[track[i3][1] - 1] = track[i3][2]
        outputl = "yes" + '\n'
        for i4 in range(0, len(sch)):
            outputl = outputl + str(i4 + 1) + " " + str(sch[i4]) + '\n'
    else:
        outputl = "no"

    # This line of code is used to create the output.txt
    outfile = open('output.txt', 'w')
    outfile.write(outputl)
    
if __name__ == "__main__": main()