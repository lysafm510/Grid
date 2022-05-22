import random
import numpy as np


# *******************************************************************
# 7. 主要对25个RyR通道的属性进行改变
# *******************************************************************


def change(type):
    all_point = [i for i in range(25)]
    open_point = []

    if type == 1:
        # 随机开放的点
        open_point = random.sample(range(0, 25), 4)
        # open_point = [1, 9, 10, 22]
    elif type == 2:
        # 自定义开放的点
        open_point = [17, 23, 4, 10, 7, 9]
    print(open_point)

    # 关闭的点：也就是需要改变属性的点
    close_point = list(set(all_point).difference(set(open_point)))
    print(close_point)

    # 下面这个长度为26的数组代表了中间的25个RyR通道，不需要变
    boun = np.zeros(26, int)
    boun[0] = 0
    boun[1] = 22
    boun[2] = 43
    boun[3] = 64
    boun[4] = 85
    boun[5] = 107
    boun[6] = 129
    boun[7] = 152
    boun[8] = 175
    boun[9] = 198
    boun[10] = 220
    boun[11] = 242
    boun[12] = 265
    boun[13] = 288
    boun[14] = 311
    boun[15] = 333
    boun[16] = 355
    boun[17] = 378
    boun[18] = 401
    boun[19] = 424
    boun[20] = 446
    boun[21] = 468
    boun[22] = 489
    boun[23] = 510
    boun[24] = 531
    boun[25] = 553

    npoch = np.loadtxt('npoch.dat', dtype=np.int64)
    for i in close_point:
        for j in range(boun[i], boun[i + 1]):
            npoch[j] = 1

    file_name = "npoch_" + str(open_point) + ".dat"
    # file_name = "npoch_center.dat"

    file = open(file_name, "w")
    print(file_name)
    for i in range(0, len(npoch)):
        file.write(str(npoch[i]) + "\n")
    file.close()


if __name__ == '__main__':
    change(2)
