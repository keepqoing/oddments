import GeoConverter
import math

def convertGEO(val1, val2):
    # -- 호출부 - -
    Geo2Tm(val1, val2)

    # -- 라이브러리 - -

def Geo2Tm(plon, plat):
    lon = plon
    lat = plat
    lon = lon * math.pi / 180;
    lat = lat * math.pi / 180;
    m_arScaleFactor = 1;
    m_arLonCenter = 2.21661859489632;
    m_arLatCenter = 0.663225115757845;
    m_arFalseNorthing = 600000.0;
    m_arFalseEasting = 200000.0;

    m_arMajor = 6377397.155;
    m_arMinor = 6356078.9633422494;

    temp = m_arMinor / m_arMajor

    m_dSrcEs = 1.0 - temp * temp;
    m_dDstEs = 1.0 - temp * temp;
    m_dDstEsp = m_dDstEs / (1.0 - m_dDstEs);
    m_dDstE0 = 1.0 - 0.25 * m_dDstEs * (1.0 + m_dDstEs / 16.0 * (3.0 + 1.25 * m_dDstEs));
    m_dDstE1 = 0.375 * m_dDstEs * (1.0 + 0.25 * m_dDstEs * (1.0 + 0.46875 * m_dDstEs));
    m_dDstE2 = 0.05859375 * m_dDstEs * m_dDstEs * (1.0 + 0.75 * m_dDstEs);
    m_dDstE3 = m_dDstEs * m_dDstEs * m_dDstEs * (35.0 / 3072.0);
    m_dDstMl0 = m_arMajor * (m_dDstE0 * m_arLatCenter - m_dDstE1 * math.sin(2.0 * m_arLatCenter) + m_dDstE2 * math.sin(4.0 * m_arLatCenter) - m_dDstE3 * math.sin(6.0 * m_arLatCenter));
    
    m_dDstInd = 0.0;

    delta_lon = lon - m_arLonCenter;
    sin_phi = math.sin(lat);
    cos_phi = math.cos(lat);

    b = 0;
    x = 0.5 * m_arMajor * m_arScaleFactor * math.log((1.0 + b) / (1.0 - b));
    con = math.acos(cos_phi * math.cos(delta_lon) / math.sqrt(1.0 - b * b));

    al = cos_phi * delta_lon;
    als = al * al;
    c = m_dDstEsp * cos_phi * cos_phi;
    tq = math.tan(lat);
    t = tq * tq;
    con = 1.0 - m_dDstEs * sin_phi * sin_phi;
    n = m_arMajor / math.sqrt(con);
    ml = m_arMajor * (m_dDstE0 * lat - m_dDstE1 * math.sin(2.0 * lat) + m_dDstE2 * math.sin(4.0 * lat) - m_dDstE3 * math.sin(6.0 * lat));

    x = m_arScaleFactor * n * al * (1.0 + als / 6.0 * (1.0 - t + c + als / 20.0 * (5.0 - 18.0 * t + t * t + 72.0 * c - 58.0 * m_dDstEsp))) + m_arFalseEasting;
    y = m_arScaleFactor * (ml - m_dDstMl0 + n * tq * (als * (0.5 + als / 24.0 * (5.0 - t + 9.0 * c + 4.0 * c * c + als / 30.0 * (
                    61.0 - 58.0 * t + t * t + 600.0 * c - 330.0 * m_dDstEsp))))) + m_arFalseNorthing;
    plon = x;
    plat = y;
    # print(x,y)

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

    sn = math.math.tan(math.pi * 0.25 + slat2 * 0.5) / math.math.tan(math.pi * 0.25 + slat1 * 0.5);
    sn = math.math.log(math.math.cos(slat1) / math.math.cos(slat2)) / math.math.log(sn);
    sf = math.math.tan(math.pi * 0.25 + slat1 * 0.5);
    sf = pow(sf, sn) * math.math.cos(slat1) / sn;
    ro = math.math.tan(math.pi * 0.25 + olat * 0.5);
    ro = re * sf / pow(ro, sn);

    if mode == 1:
        ra = math.math.tan(math.pi * 0.25 + (lat_X)* DEGRAD * 0.5)
        ra = re * sf / pow(ra, sn)
        theta = lng_Y * DEGRAD - olon
        if theta > math.pi:
            theta -= 2.0 * math.pi
        if theta < -math.pi:
            theta += 2.0 * math.pi
        theta *= sn
        cx = (ra * math.math.sin(theta) + XO + 0.5)
        cy = (ro - ra * math.math.cos(theta) + YO + 0.5)
    	# /*cx = floor(ra * math.math.sin(theta) + XO + 0.5);
    	# cy = floor(ro - ra * math.math.cos(theta) + YO + 0.5);*/
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

    with open(targetfile, 'w', encoding='utf8') as f2:
      for line in f1:
         tmp = line.split(' ')
         convertGEO(float(tmp[2]), float(tmp[1]))
         pt = GeoConverter.GeoPoint(float(tmp[2]), float(tmp[1]))
         output = GeoConverter.convert(GeoConverter.GEO, GeoConverter.TM, pt)
         # print(output.getX(),output.getY(), tmp[3])
         minXX = 22667.79
         # 632349.58
         minYY = 58111.02
         # 670973.78
         x = (output.getX() - minXX)/9000
         y = (output.getY() - minYY)/(-9000)
         print(x,y)

         f2.write(tmp[0] + " " + str(x) + " " + str(y) + " " + tmp[3])
           # f2.write("\n")
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
    #



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

copy_and_print("C:\\Users\\USER\\Desktop\\새 폴더 (2)\\지점a.txt")

# pt = GeoConverter.GeoPoint(309557.63, 543200.07)
# output = GeoConverter.convert(GeoConverter.TM, GeoConverter.GEO, pt)
# ta = convertGRID_GPS(1, output.getY(), output.getX(), 0)
# print(ta)
# print(str(output.getY()) + " " + str(output.getX()))
# print(convertGRID_GPS(1, 37.3779, 128.3946, 0))