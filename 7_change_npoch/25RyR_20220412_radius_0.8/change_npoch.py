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
        open_point = [1, 9, 10, 24]
    print(open_point)

    # 关闭的点：也就是需要改变属性的点
    close_point = list(set(all_point).difference(set(open_point)))
    print(close_point)

    # 下面这个长度为26的数组代表了中间的25个RyR通道，不需要变
    boun = np.zeros(26, int)
    boun[0] = 0
    boun[1] = 26
    boun[2] = 51
    boun[3] = 76
    boun[4] = 101
    boun[5] = 127
    boun[6] = 153
    boun[7] = 180
    boun[8] = 207
    boun[9] = 234
    boun[10] = 260
    boun[11] = 286
    boun[12] = 313
    boun[13] = 340
    boun[14] = 367
    boun[15] = 393
    boun[16] = 419
    boun[17] = 446
    boun[18] = 473
    boun[19] = 500
    boun[20] = 526
    boun[21] = 552
    boun[22] = 576
    boun[23] = 601
    boun[24] = 625
    boun[25] = 651

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
