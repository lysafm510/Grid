import numpy as npp
from math import sqrt

# *******************************************************************
# 3. 将模块2离散化的点进行逐一连线，并赋属性值
#
# 按以下顺序进行：
# 第1步：更改输入输出文件
# 输入文件：将模块2生成的离散点，拼接。顺序为先小圆后大圆
side_gridt_file = "sidegridt.dat"
side_npoch_file = "sidenpoch.dat"
# 输出文件：
side_face_file = "sideface.dat"


# 第2步：对main函数进行修改，统计各个圆上点的数量，需要手动统计。。。

# *******************************************************************


def not_empty(s):
    return s and s.strip()


def main():
    '''
    输入：sidegridt2.dat -->  大圆，小圆上所有点的坐标，第1行是点数，小圆上45个点，大圆337个点
        sidenpoch2.dat -->  大圆，小圆上所有点的属性，多1行，多出来的是大圆上第一个入流点和最后一个入流点属性重复了
    :return:
    '''
    boun = npp.zeros(100, int)
    nboun = 26
    boun[0] = 11
    boun[1] = 23
    boun[2] = 35
    boun[3] = 47
    boun[4] = 58
    boun[5] = 70
    boun[6] = 81
    boun[7] = 92
    boun[8] = 103
    boun[9] = 115
    boun[10] = 127
    boun[11] = 138
    boun[12] = 149
    boun[13] = 160
    boun[14] = 173
    boun[15] = 186
    boun[16] = 197
    boun[17] = 208
    boun[18] = 219
    boun[19] = 232
    boun[20] = 242
    boun[21] = 254
    boun[22] = 266
    boun[23] = 278
    boun[24] = 289
    boun[25] = 681
    sidegridt = open(side_gridt_file, "r")
    sidenpoch = open(side_npoch_file, "r")
    sideface = open(side_face_file, "w")

    d = 0
    sidenpochs = npp.empty(1000, int)
    for line in sidenpoch.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        sidenpochs[d] = current_line[0]
        d = d + 1
    # nb = d
    # sideface.write(str(nb)+ "\n")   # sideface 第一行写：统计npoch有多少行
    istart = 0
    for i in range(0, nboun):
        iend = boun[i]
        for j in range(istart, iend - 1):
            k = sidenpochs[j]
            if k != sidenpochs[j + 1]:  # 线段两端一个是入流点，一个是壁面点，那么这个线段上的点都是壁面点
                k = 1
            sideface.write(str(j + 1) + " " + str(j + 2) + " " + str(k) + "\n")
        k = sidenpochs[iend - 1]
        if k != sidenpochs[istart]:  # 最后一个点和起点的比较
            k = 1
        sideface.write(str(iend) + " " + str(istart + 1) + " " + str(k) + "\n")
        istart = iend
    sideface.close()
    sidegridt.close()
    sidenpoch.close()


main()
