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
        open_point = [1, 9, 10, 22]
    print(open_point)

    # 关闭的点：也就是需要改变属性的点
    close_point = list(set(all_point).difference(set(open_point)))
    print(close_point)

    # 下面这个长度为26的数组代表了中间的25个RyR通道，不需要变
    boun = np.zeros(26, int)
    boun[0] = 0
    boun[1] = 30
    boun[2] = 52
    boun[3] = 74
    boun[4] = 96
    boun[5] = 126
    boun[6] = 148
    boun[7] = 168
    boun[8] = 188
    boun[9] = 208
    boun[10] = 230
    boun[11] = 252
    boun[12] = 272
    boun[13] = 292
    boun[14] = 312
    boun[15] = 334
    boun[16] = 356
    boun[17] = 376
    boun[18] = 396
    boun[19] = 416
    boun[20] = 438
    boun[21] = 468
    boun[22] = 490
    boun[23] = 512
    boun[24] = 534
    boun[25] = 564

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
