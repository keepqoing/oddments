import random
from random import randint

oldNumCount = {}
numlist = []
with open("lotto2.txt", encoding="utf-8") as f:
    for line in f:
        line = line.replace("\n", "")
        tmp = line.split("\t")
        tmp = tmp[1:7]
        for i in tmp:
            numlist.append(int(i))
            if i in oldNumCount.keys():
                oldNumCount[i] = oldNumCount[i] + 1
            else:
                oldNumCount[i] = 1

a = sorted(oldNumCount.items())
print(a)
b = sorted(oldNumCount.items(), key=lambda t: t[1], reverse=True)
print(b)

print(len(numlist))

random.shuffle(numlist)

print(numlist)

numCount = {}
mynumberlist = []
for j in range(0, 1000):
    random.shuffle(numlist)
    mynumber = []

    for i in range(0, 6):
        ranNum = randint(0, len(numlist)-1)
        if numlist[ranNum] not in mynumber:
            mynumber.append(numlist[ranNum])
        else:

            while numlist[ranNum] in mynumber:
                ranNum = randint(0, len(numlist)-1)
            mynumber.append(numlist[ranNum])

    mynumberlist.append(mynumber)
    for i in mynumber:
        if i in numCount.keys():
            numCount[i] = numCount[i] + 1
        else:
            numCount[i] = 1

c = sorted(numCount.items(), key=lambda t: t[1], reverse=True)
print(b)
print(c)

makedNum = set()

count = 0
ranNum = randint(0, 8145060)
while True:
    random.shuffle(mynumberlist)
    ranNum = randint(0, 8145060)
    if ranNum == 421:

        #
        makedNum.update(mynumberlist[ranNum])
        #

        count = count+1
        mynumberlist[ranNum].sort()
        print(mynumberlist[ranNum])
    if count == 5:
        break


print(makedNum)

aa = list(makedNum)
print(aa)


mynumber2 = []
for i in range(0, 6):
    random.shuffle(mynumberlist)
    ranNum = randint(0, len(aa) - 1)
    mynumber2.append(aa[ranNum])
    aa.remove(aa[ranNum])

mynumber2.sort()
print(mynumber2)


