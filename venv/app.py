def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


# Fault_Find_Cause1
# csv 파일을 읽어서 Transaction의 형태로 저장
def getDataset():
    with open("faultz.txt", encoding="utf-8-sig") as f:
        keys = set()
        transactionData = list()
        for line in f:
            line = str(line).replace("\n", "")
            transactionItems = str(line).split(",")
            transactionData.append(transactionItems)

    return transactionData


# 후보 아이템 집합 C1을 만드는 함수
# C1을 생성한 다음 단일 아이템이 minSupport를 만족하는지를 확인하기 위해 데이터 집합을 살펴보고
# 요구조건을 만족하는 아이템 집합은 L1이 된다.
# L1을 다시 결합하면 C2가 되고ㅡ 요구조건으로 걸러진 C2는 L2가 된다.
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])

    C1.sort()
    # frozenset은 고정된 집합이므로 변경할 수 없다.
    # set 대신 frozenset을 사용하는 이유는
    # 나중에 이 집합들을 딕셔너리의 키처럼 사용할 것이기 때문이다.
    return list(map(frozenset, C1))  # use frozen set so we
    # can use it as a key in a dict


# D는 dataset (transaction list)
# Ck는 후보 집합 리스트
# minSupport는 최소 지지도
# C1으로부터 L1을 생성한다.
def scanD(D, Ck, minSupport):
    # 나중에 사용하게 될 지지도 값을 가진 딕셔너리 ssCnt
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can in ssCnt:
                    ssCnt[can] += 1
                else:
                    ssCnt[can] = 1

    transLen = float(len(D))
    # 최소 지지도를 만족하는 집합 retList
    retList = []

    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / transLen
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData


def aprioriGen(Lk, k):  # creates Ck
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()

            if L1 == L2:  # if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j])  # set union
    return retList


def apriori(dataSet, minSupport):
    C1 = createC1(dataSet)
    D = list(map(set, dataSet))

    # 길이가 1인 후보 아이템 목록 생성
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    # 집합 내에 있는 아이템의 갯수가 0보다 큰 동안 반복
    # 길이가 2 이상인 후보 아이템 목록 생성
    while (len(L[k - 2]) > 0):
        # 길이가 k인 후보 아이템 집합 Ck 생성
        Ck = aprioriGen(L[k - 2], k)
        # Ck를 이용해 Lk를 생성하고 지지도를 저장하는 딕셔너리 추가
        Lk, supK = scanD(D, Ck, minSupport)  # scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1

    return L, supportData


def generateRules(L, supportData, minConf):  # supportData is a dict coming from scanD
    bigRuleList = []
    for i in range(1, len(L)):  # only get the sets with two or more items
        for freqSet in L[i]:
            # 빈발 아이템 집합을 단일 아이템 집합의 리스트로 만든다 -> H1
            H1 = [frozenset([item]) for item in freqSet]

            for tmp in H1:
                lhs = freqSet - tmp
                rhs = tmp

                calcConf(lhs, rhs, supportData, bigRuleList, minConf)

    return bigRuleList



def calcConf(lhs, rhs, supportData, brl, minConf):
    # print((lhs | rhs) in supportData.keys(), lhs in supportData.keys(),rhs in supportData.keys())

    if (lhs | rhs) in supportData.keys()and lhs in supportData.keys() and rhs in supportData.keys():
        conftmp = supportData[lhs | rhs] / supportData[lhs]
        if conftmp >= minConf:
            # print(lhs, '-->', rhs, 'sup: ', supportData[lhs | rhs], ' conf: ', conftmp, ' lift: ',
            #       conftmp / supportData[rhs])
            brl.append((lhs, rhs, supportData[lhs | rhs], conftmp, conftmp / supportData[rhs]))
            tmp = {}
            tmp["lhs"] = list(lhs)
            tmp["rhs"] = list(rhs)
            tmp["sup"] = supportData[lhs | rhs]
            tmp["conf"] = conftmp
            tmp["lift"] = conftmp / supportData[rhs]



minsup = 0.01

dataSet = getDataset()
print("======================================")

L, suppData = apriori(dataSet, 0.01)



rules = generateRules(L, suppData, 0.4)
print("======================================")
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
for i, val in enumerate(rules):
    tttt = list(val[1])
    if len(val[0]) == 5 and len(val[1]) == 1 and tttt[0][0] == 'F':
        count7 += 1
    if len(val[0]) + len(val[1]) == 2:
        count2 += 1
    elif len(val[0]) + len(val[1]) == 3:
        count3 += 1
    elif len(val[0]) + len(val[1]) == 4:
        count4 += 1
    elif len(val[0]) + len(val[1]) == 5:
        count5 += 1
    elif len(val[0]) + len(val[1]) == 6:
        count6 += 1

print(count2)
print(count3)
print(count4)
print(count5)
print(count6)
print(count7)

C1 = createC1(dataSet)
itemList = []
print(C1)
for i in C1:
    print(i)
    # itemList.append()