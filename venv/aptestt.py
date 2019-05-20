# coding: utf-8

# In[ ]:


## 패키지 임포트
import os
import sys
import pandas as pd
import numpy as np


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

## 데이터 로딩, Optionparser를 통해 수정이 필요함 예를들어 python Apriori Algorith.py -f "OrderList.csv" 이런식으로 커널에서 돌아가게
def load_data():
    data = getDataset()

    return data


## user - 구매내역 데이터 만들고, 구매내역만 리스트로 추출하기
def preparing_bought_list():
    user_list = data['m_id'].unique()  ## 구매자 id 목록
    user_bought_dict = dict()

    ## 구매자 - 구매 목록 집합 생성
    for id in user_list:
        user_bought_dict[id] = [str(item) for item in data.loc[data["m_id"] == id, "goods_code"]]

    ## 구매 목록만 추출
    bought_list = list(user_bought_dict.values())

    return bought_list


## 비교를 위한 key로 사용할 각 아이템 목록 생성
def Create_ItemKeyList(dataSet):
    # 각 아이템 목록 리스트
    ItemKeyList = []

    ## 각 구매명단에 있는 item들을 추출해냄
    for transaction in dataSet:
        for item in transaction:
            if not [item] in ItemKeyList:
                ItemKeyList.append([item])

    ## 정렬
    ItemKeyList.sort()

    ## dict에서 key로 이용할 수 있도록 frozenset에 매핑한 리스트를 만듦
    return list(map(frozenset, ItemKeyList))


## minimum_support를 만족하는 1.아이템의 key, 2,key와 support가 담긴 각각의 리스트를 추출함
## support란 전체 N에서 frequency의 비율이라고 할 수 있음
def ItemWithMinSupport(DistinctTransactionList, K_ItemKeyList, MinSupport):
    ItemCountDict = {}

    ## 중복제거한 각 거래목록에서 각 아이템의 갯수를 파악
    for distinct_transaction in DistinctTransactionList:
        for element in K_ItemKeyList:
            if element.issubset(distinct_transaction):
                if element not in ItemCountDict:
                    ItemCountDict[element] = 1
                else:
                    ItemCountDict[element] += 1

    NumItems = float(len(DistinctTransactionList))
    KeyList = []
    ItemSupportDict = {}

    for key in ItemCountDict:
        support = ItemCountDict[key] / NumItems
        ## minimum support를 만족하는 아이템들의 key
        if support >= MinSupport:
            KeyList.insert(0, key)
        ## 각 key들의 support를 반영한 dict를 생성
        ItemSupportDict[key] = support

    return KeyList, ItemSupportDict


def aprioriGen(K_SatisfiedKey, k):
    """minimum support를 만족하는 리스트들을 탐색하면서 아이템 조합을 만들어냄"""
    KeyList = []
    lenKSK = len(K_SatisfiedKey)

    ## Minimum Support를 만족하는 리스트들을 탐색함
    for i in range(lenKSK):
        for j in range(i + 1, lenKSK):
            ## k-2까지의 요소들을 탐색해서 정렬
            First_SatisfiedKey = list(K_SatisfiedKey[i])[:k - 2];
            Second_SatisfiedKey = list(K_SatisfiedKey[j])[:k - 2]
            First_SatisfiedKey.sort();
            Second_SatisfiedKey.sort()
            ## k-2의 요소가 같다면 union
            if First_SatisfiedKey == Second_SatisfiedKey:
                KeyList.append(K_SatisfiedKey[i] | K_SatisfiedKey[j])

    return KeyList


## 전체 데이터에서 MinSupport를 만족하는 집단들 연관성 분석
def apriori(dataSet, MinSupport):
    ItemKeyList = Create_ItemKeyList(dataSet)
    DistinctTransactionList = list(map(set, dataSet))

    ## MinSupport를 만족하는 집합 추출 후, 이것을 가지고 모든 경우의 수를 판단함
    First_SatisfiedKey, ItemSupportDict = ItemWithMinSupport(DistinctTransactionList, ItemKeyList, MinSupport)
    Satisfied_Key = [First_SatisfiedKey]
    k = 2

    ## 탐색 => 판단 => 추가
    while (len(Satisfied_Key[k - 2]) > 0):
        K_ItemKeyList = aprioriGen(Satisfied_Key[k - 2], k)
        K_SatisfiedKey, K_ItemSupportDict = ItemWithMinSupport(DistinctTransactionList, K_ItemKeyList, MinSupport)
        ItemSupportDict.update(K_ItemSupportDict)
        Satisfied_Key.append(K_SatisfiedKey)
        k += 1

    return Satisfied_Key, ItemSupportDict


## Minimum Support를 만족하는 집단 중, Minimum Confidence를 만족하는 집단 => 해당 규칙과 Confidence를 출력해줌
## 1개 넘으면 rulesFromConseq에 가서 aprioriGen을 거친 후 계산
## 1개면 바로 계산
def generateRules(Satisfied_Key, ItemSupportDict, MinConf):
    BigRuleList = []
    for i in range(1, len(Satisfied_Key)):
        for FreqSet in Satisfied_Key[i]:
            print("generateRules FreqSet : ", FreqSet)
            H1 = [frozenset([item]) for item in FreqSet]

            if (i > 1):
                rulesFromConseq(FreqSet, H1, ItemSupportDict, BigRuleList, MinConf)
            else:
                calcConf(FreqSet, H1, ItemSupportDict, BigRuleList, MinConf)

    return BigRuleList


## 신뢰도를 계산해주기 위한 함수
def calcConf(FreqSet, H, ItemSupportDict, brl, MinConf):
    prunedH = []
    for conseq in H:
        print("calcConf conseq : ", conseq)
        conf = ItemSupportDict[FreqSet] / ItemSupportDict[conseq]
        if conf >= MinConf:
            print(conseq, '-->', FreqSet - conseq, 'conf:', conf)
            brl.append((conseq, FreqSet - conseq, conf))
            prunedH.append(conseq)

    return prunedH


### 주어진 set들에 대해 신뢰도를 계산, 2개 이상일 경우 다시 aprioriGen을 거친 후 계산
def rulesFromConseq(FreqSet, H, ItemSupportDict, brl, MinConf):
    print("rulesFromConseq FreqSet : ", FreqSet)
    print("rulesFromConseq H : ", H)
    m = len(H[0])
    if (len(FreqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m + 1)
        print("rulesFromConseq Hmp1 : ", Hmp1)
        Hmp1 = calcConf(FreqSet, Hmp1, ItemSupportDict, brl, MinConf)
        print("rulesFromConseq Hmp1 : ", Hmp1)
        if (len(Hmp1) > 1):
            rulesFromConseq(FreqSet, Hmp1, ItemSupportDict, brl, MinConf)

print("start")
data = load_data()
dataSet = getDataset()
MinSupport = 0.01
MinConf = 0.4
Satisfied_Key, ItemSupportDict = apriori(dataSet, MinSupport)
rules = generateRules(Satisfied_Key, ItemSupportDict, MinConf)

count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
for i, val in enumerate(rules):
    # print("rules ", i, " : ", val)
    if len(val[0]) + len(val[1]) == 2:
        count2 += 1
    elif len(val[0]) + len(val[1]) == 3:
        count3 += 1
    elif len(val[0]) + len(val[1]) == 4:
        count4 += 1
    elif len(val[0]) + len(val[1]) == 5:
        if len(val[0]) == 4 and len(val[1]) == 1:
            count7 += 1
        else:
            count5 += 1
    elif len(val[0]) + len(val[1]) == 6:
        count6 += 1

print(count2)
print(count3)
print(count4)
print(count5)
print(count6)
print(count7)



# for i, val in enumerate(rules):
#     if len(val[0]) + len(val[1]) == 3:
#         print(i, val[0], " ==> ", val[1])