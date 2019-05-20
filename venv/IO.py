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
        return str(cx) + " " + str(cy)
               # + " " + str(Z) + " "

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
    tmp1 = "0"
    tmp2 = "0"
    count = 0
    ttt = 0
    aa = ""
    with open(targetfile, 'w', encoding='utf8') as f2:
        for line in f1:
            tmp = line.split(' ')
            # pt = GeoConverter.GeoPoint(float(tmp[0]), float(tmp[1]))
            # output = GeoConverter.convert(GeoConverter.TM, GeoConverter.GEO, pt)

            aa = convertGRID_GPS(1, float(tmp[1]), float(tmp[2]), float(0))
            # f2.write(str(output.getY()) + " " + str(output.getX()) + '\n')
            print(tmp[3])
            f2.write(tmp[0] + " " + aa + " " + tmp[3] )
        # f2.write('}')

copy_and_print("C:\\Users\\USER\\Desktop\\새 폴더 (2)\\지점a.txt")

# pt = GeoConverter.GeoPoint(309557.63, 543200.07)
# output = GeoConverter.convert(GeoConverter.TM, GeoConverter.GEO, pt)
# ta = convertGRID_GPS(1, output.getY(), output.getX(), 0)
# print(ta)
# print(str(output.getY()) + " " + str(output.getX()))
# print(convertGRID_GPS(1, 37.3779, 128.3946, 0))

