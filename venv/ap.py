# fault = []
# keys = []


# csv 파일을 읽어서 Transaction의 형태로 저장
def getDataset():
    with open("Fault_Find_Cause1.txt", encoding="utf-8-sig") as f:
        keys = set()
        transactionData = list()
        for line in f:
            line = str(line).replace("\n", "")
            transactionItems = str(line).split(",")
            transactionData.append(transactionItems)

            # support 계산을 위해 key 목록을 따로 저장
            for item in transactionItems:
                keys.add(item)

    return transactionData, keys


# 한 subset의 support를 계산하는 함수
def getSupport(subset, transactionData):
    # print(subset, transactionData)
    count = 0
    transLen = len(transactionData)
    for trans in transactionData:
        set_trans = set(trans)
        set_subset = set(subset)
        if set_trans & set_subset == set_subset:
            count = count + 1

    sup = count / transLen



    # print(subset, sup)
    return sup


# 각 item의 support를 계산하는 함수
def get_All_Items_Support(transactionData, items):
    for item in items:
        subset = list()
        subset.append(item)
        print(item, getSupport(subset, transactionData))


# 각 item의 support를 계산하고 minSupport보다 낮으면 제거하는 함수
def get_All_Items_Support_and_Remove(transactionData, items, minSupport):
    minSupList = []
    print(len(items))
    for item in items:
        subset = list()
        subset.append(item)
        if getSupport(subset, transactionData) >= minSupport:
            print(item, getSupport(subset, transactionData))
            minSupList.append(item)

    print(len(minSupList), minSupList)
    return minSupList

# 한 트랜잭션의 모든 부분집합을 구하는 함수
def getSubset(minSupList, tmp, current, transactionData, minSupport):
    if current == len(minSupList):
        return

    sup = getSupport(tmp, transactionData)
    if sup < minSupport:
        return
    print(tmp, sup)

    # 현재 Item을 포함하지 않고 시도
    getSubset(minSupList, tmp, current + 1, transactionData, minSupport)

    # 현재 Item을 포함하고 시도
    tmp.append(minSupList[current])

    sup = getSupport(tmp, transactionData)
    if sup < minSupport:
        return
    print(tmp, sup)

    getSubset(minSupList, tmp, current + 1, transactionData, minSupport)
    tmp.remove(minSupList[current])


transactionData, items = getDataset()
print(transactionData)
print(items)
minSupList = get_All_Items_Support_and_Remove(transactionData, items, 0.1)

getSubset(minSupList, [], 0, transactionData, 0.01)