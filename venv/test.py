import GeoConverter
import math
def convertGRID_GPS(mode, lat_X, lng_Y, Z):
    RE = 6371.00877 # 지구 반경(km)
    GRID = 5.0 # 격자 간격(km)
    SLAT1 = 30.0 # 투영 위도1(degree)
    SLAT2 = 60.0 # 투영 위도2(degree)
    OLON = 126.0 # 기준점 경도(degree)
    OLAT = 38.0 # 기준점 위도(degree)
    XO = -50 # 기준점 X좌표(GRID)
    YO = 50 # 기1준점 Y좌표(GRID)


 # LCC DFS 좌표변환 ( code : "TO_GRID"(위경도->좌표, lat_X:위도,  lng_Y:경도), "TO_GPS"(좌표->위경도,  lat_X:x, lng_Y:y) )

    DEGRAD = math.pi / 180.0
    RADDEG = 180.0 / math.pi

    re = RE / GRID
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5);
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn);
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5);
    sf = pow(sf, sn) * math.cos(slat1) / sn;
    ro = math.tan(math.pi * 0.25 + olat * 0.5);
    ro = re * sf / pow(ro, sn);

    if mode == 1:
        ra = math.tan(math.pi * 0.25 + (lat_X)* DEGRAD * 0.5)
        ra = re * sf / pow(ra, sn)
        theta = lng_Y * DEGRAD - olon
        if theta > math.pi:
            theta -= 2.0 * math.pi
        if theta < -math.pi:
            theta += 2.0 * math.pi
        theta *= sn
        cx = (ra * math.sin(theta) + XO + 0.5)
        cy = (ro - ra * math.cos(theta) + YO + 0.5)
    	# /*cx = floor(ra * math.sin(theta) + XO + 0.5);
    	# cy = floor(ro - ra * math.cos(theta) + YO + 0.5);*/
        # print(cx, cy, Z)
        # return "{" + str(cx) + "," + str(cy) + "," + str(Z) + "}"
        # return str(cx) + " " + str(cy) + " " + str(Z) + " "
        return str(cx) + " " + str(cy)
# with open("C:\\Users\\USER\\Desktop\\그래픽스\\서울특별시\\2014 서울특별시[ascii]\\서울특별시 강남구.txt") as f:
#     for line in f:
#         tmp = line.split(' ')
#         pt = GeoConverter.GeoPoint(float(tmp[0]), float(tmp[1]))
#         output = GeoConverter.convert(GeoConverter.TM, GeoConverter.GEO, pt)
#         # print(output.getX(), output.getY(), tmp[2])
#         aa = convertGRID_GPS(1, output.getY(), output.getX(), float(tmp[2]))
#         print(aa)

def copy_and_print(filename):
  with open(filename, encoding="utf8") as f1:
    targetfile = 'copied_'
    maxX = 0
    minX = 100000000
    maxY = 0
    minY = 100000000
    prevX = "0"
    prevY = "0"
    count = 0
    ttt = 0
    aa = ""
    dic = []

    for line in f1:
        tmp = line.split(' ')
        if count == 0:
            # f2.write(str(ttt) + " " + aa + '\n')
            # print (line)
            if (float(tmp[0]) > maxX):
                maxX = float(tmp[0])
            if (float(tmp[0]) < minX):
                minX = float(tmp[0])
            if (float(tmp[1]) > maxY):
                maxY = float(tmp[1])
            if (float(tmp[1]) < minY):
                minY = float(tmp[1])
            prevX = tmp[0]
            prevY = tmp[1]
            count = count + 1

        else:
            if (float(tmp[0]) > maxX):
                maxX = float(tmp[0])
            if (float(tmp[0]) < minX):
                minX = float(tmp[0])
            if (float(tmp[1]) > maxY):
                maxY = float(tmp[1])
            if (float(tmp[1]) < minY):
                minY = float(tmp[1])

            if (float(prevX) - float(tmp[0])) != 0:
                ttt = ttt + 1
                prevX = tmp[0]
                prevY = tmp[1]
                count = 0
            else:
                prevX = tmp[0]
                prevY = tmp[1]
                count = count + 1
    print(minX,maxX,minY,maxY)
    pt = GeoConverter.GeoPoint(float(15968.71), float(-39467.05))
    output = GeoConverter.convert(GeoConverter.TM, GeoConverter.GEO, pt)
    aa = convertGRID_GPS(1, output.getY(), output.getX(), float(tmp[2]))
    print(aa)
    # print(minX,maxX)
    # print(int((maxX - minX) / 90))


    # arr = [[0] * int((maxY - minY) / 90) for i in range(int((maxX - minX) / 90))]
    # print(len(arr))
    #
    # with open(filename, encoding="utf8") as f1:
    #     count = 0
    #     ttt = 0
    #     for line in f1:
    #         tmp = line.split(' ')
    #         arr[int((float(tmp[0]) - minX) / 90)-1][int((float(tmp[1]) - minY) / 90)-1] = float(tmp[2])
    #         # print(int((float(tmp[0]) - minX) / 90), int((float(tmp[1]) - minY) / 90))
    #         # print(arr[int((float(tmp[0]) - minX) / 90)-1][int((float(tmp[1]) - minY) / 90)-1])
    #         if count == 0:
    #             # print(int((float(tmp[0]) - minX)/90),int((float(tmp[1]) - minY)/90))
    #             prevX = tmp[0]
    #             prevY = tmp[1]
    #             count = count + 1
    #
    #         else:
    #             # print(int((float(tmp[0]) - minX) / 90), int((float(tmp[1]) - minY) / 90))
    #
    #             if (float(prevX) - float(tmp[0])) != 0:
    #                 ttt = ttt + 1
    #                 prevX = tmp[0]
    #                 prevY = tmp[1]
    #                 count = 0
    #             else:
    #                 prevX = tmp[0]
    #                 prevY = tmp[1]
    #                 count = count + 1
    #
    # # print(minX,maxX)
    # # print((maxX - minX) / 90)
    # with open(targetfile, 'w', encoding='utf8') as f2:
    #     f2.write(str(int((maxX - minX) / 90)) + ' ')
    #     f2.write(str(int((maxY - minY) / 90)) + '\n')
    #     for i in arr:
    #         for j in i:
    #             f2.write(str(j) + ' ')
    #         f2.write("\n")




    # linecount = 0
    # with open(targetfile, 'w', encoding='utf8') as f2:
    #     for line in f1:
    #         linecount = linecount+1
    #         tmp = line.split(' ')
    #         pt = GeoConverter.GeoPoint(float(tmp[0]), float(tmp[1]))
    #         output = GeoConverter.convert(GeoConverter.TM, GeoConverter.GEO, pt)
    #         if count == 0:
    #             # f2.write(str(ttt) + " " + aa + '\n')
    #             # print (line)
    #             if (float(tmp[0]) > maxX):
    #                 maxX = float(tmp[0])
    #             if (float(tmp[0]) < minX):
    #                 minX = float(tmp[0])
    #             if (float(tmp[1]) > maxY):
    #                 maxY = float(tmp[1])
    #             if (float(tmp[1]) < minY):
    #                 minY = float(tmp[1])
    #             prevX = tmp[0]
    #             prevY = tmp[1]
    #             count = count+1
    #             aa = aa + convertGRID_GPS(1, output.getY(), output.getX(), float(tmp[2]))
    #
    #         else:
    #             # print("X", float(prevX) - float(tmp[0]))
    #             # print("Y", float(prevY) - float(tmp[1]))
    #             if(float(tmp[0]) > maxX):
    #                 maxX = float(tmp[0])
    #             if(float(tmp[0]) < minX):
    #                 minX = float(tmp[0])
    #             if (float(tmp[1]) > maxY):
    #                 maxY = float(tmp[1])
    #             if (float(tmp[1]) < minY):
    #                 minY = float(tmp[1])
    #             # if (float(prevY) - float(tmp[1])) != 90 and (float(prevX) - float(tmp[0])) == 0:
    #             #     print("Y", linecount, ttt, count, prevY, tmp[1], float(prevY) - float(tmp[1]))
    #
    #             # if(float(prevY) - float(tmp[1])) !=90:
    #                 # print("Y", linecount, ttt,count,prevY,tmp[1],float(prevY) - float(tmp[1]))
    #                 # print("Y",linecount,prevY,tmp[1],float(prevY) - float(tmp[1]))
    #
    #             if (float(prevX) - float(tmp[0])) != 0:
    #                 # print("X", linecount, ttt,count,prevX,tmp[0],float(prevX) - float(tmp[0]))
    #                 # print("X",linecount,prevX,tmp[0],float(prevX) - float(tmp[0]))
    #                 # dic[ttt] = count
    #                 if ttt != 0:
    #                     count = count+1
    #                     dic.append(count)
    #                 else:
    #                     dic.append(count)
    #                 # else:
    #                 #     f2.write(str(ttt) + " " + str(count) + '\n')
    #                 # print(ttt,count)
    #                 ttt = ttt + 1
    #                 f2.write(aa + 'NEXT\n')
    #                 aa = ""
    #                 aa = aa + convertGRID_GPS(1, output.getY(), output.getX(), float(tmp[2]))
    #                 prevX = tmp[0]
    #                 prevY = tmp[1]
    #                 count = 0
    #             else:
    #                 # f2.write(str(ttt) + " " + aa + '\n')
    #                 prevX = tmp[0]
    #                 prevY = tmp[1]
    #                 count = count + 1
    #                 aa = aa + convertGRID_GPS(1, output.getY(), output.getX(), float(tmp[2]))

        # print(maxX,minX)
        # print((maxX-minX)/90)
        # print(maxY, minY)
        # print((maxY-minY)/90)
        # print(max(dic), len(dic))
            # pt = GeoConverter.GeoPoint(float(tmp[0]), float(tmp[1]))
            # output = GeoConverter.convert(GeoConverter.TM, GeoConverter.GEO, pt)
            # aa = convertGRID_GPS(1, output.getY(), output.getX(), float(tmp[2]))
            # f2.write(aa + '\n')
        # f2.write('}')

copy_and_print("C:\\Users\\USER\\Desktop\\새 폴더 (2)\\강원도\\map5.txt")

# pt = GeoConverter.GeoPoint(309557.63, 543200.07)
# output = GeoConverter.convert(GeoConverter.TM, GeoConverter.GEO, pt)
# ta = convertGRID_GPS(1, output.getY(), output.getX(), 0)
# print(ta)
# print(str(output.getY()) + " " + str(output.getX()))
# print(convertGRID_GPS(1, 37.3779, 128.3946, 0))