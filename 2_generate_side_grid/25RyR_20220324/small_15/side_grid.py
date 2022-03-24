from math import asin, sin, cos
import numpy as npp

global boungridts, bounpochs

# *******************************************************************
# 2. 对中间小圆(RyR)和大圆(终池边界)离散化生成点
#
# 按以下顺序进行：
# 第1步：更改输入输出文件
# 输入文件：前三个文件从第一个模块中取，第四个文件根据grid坐标信息自定义步长
background_gridt_file = "bggridt.dat"
background_noe_file = "bgnoe.dat"
background_nod_file = "bgnod.dat"
background_step_file = "bgstep.dat"
# 输出文件：离散化后的点坐标和属性值
boundary_gridt_file = "boungridt.dat"
boundary_npoch_file = "bounpoch.dat"

# 第2步：选择边界类型
SIDE_TYPE = 2
# side_type : 1 - (暂时没用到过)
#             2 - 单段连续边界，对应RyR小圆，点的属性全都是4
#             3 - 分段连续边界，对应终池大圆，点的属性有1有2
# 如果选择边界类型为2
SMALL_COORDINATES_X = 60.0
SMALL_COORDINATES_Y = 0.0
SMALL_RADIUS = 0.5

# 如果选择边界类型为3，
# 1. 更改半径
# 2. 修改xyarcbo()函数。本文件中的xyarcbo()例子为4fSR管子，不同fSR管子需要修改，一般也不需要变动
BIG_RADIUS = 300

# *******************************************************************

boungridts = npp.zeros((1000, 2), float)
bounpochs = npp.zeros(1000, float)

pmax = 100000
emax = 200000
bmax = 50000
fmin = 10 * -8
fm2 = 10 * -8

global np, nboun, sidetype, nbs, bounarc, px, py, pstep, bx, by, bs
np = 0
nboun = 0
sidetype = 0
nbs = 0
bounarc = 0
px = npp.zeros(bmax, float)
py = npp.zeros(bmax, float)
pstep = npp.zeros(bmax, float)
bx = npp.zeros(bmax, float)
by = npp.zeros(bmax, float)
bs = npp.zeros(bmax, float)

global gx, gy, gcx, gcy, gcr, x, y, xce, yce
gx = npp.zeros(3, float)
gy = npp.zeros(3, float)
gcx = 0.00
gcy = 0.00
gcr = 0.00
x = 0.00
y = 0.00
xce = 0.00
yce = 0.00

global bgnp, bgne, bgstep, bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
bgnp = 0
bgne = 0
bgpx = npp.zeros(pmax, float)
bgpy = npp.zeros(pmax, float)
bgstep = npp.zeros(pmax, float)
bgnod = npp.zeros((3, emax), int)
bgnoe = npp.zeros((3, emax), int)
bgcx = npp.zeros(emax, float)
bgcy = npp.zeros(emax, float)
bgcr = npp.zeros(emax, float)


def not_empty(s):
    return s and s.strip()


def main():
    global boungridts, bounpochs
    global np, nboun, sidetype, nbs, bounarc, px, py, pstep, bx, by, bs
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    global bgnp, bgne, bgstep, bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    global arcboun
    global cent_x, cent_y
    global rad
    iloop = 0
    npoch = npp.zeros(2000, int)
    arc = 0.00
    x0 = 0.00
    y0 = 0.00
    x1 = 0.00
    y1 = 0.00
    pai = 0.00
    arcboun = 0.00
    xbo = npp.zeros(2000, float)
    ybo = npp.zeros(2000, float)
    arcbo = npp.zeros(2000, float)
    filename = ""

    sidetype = SIDE_TYPE
    boungridt_file = open(boundary_gridt_file, "w+")
    bounpoch_file = open(boundary_npoch_file, "w+")
    # sidetype=1 离散形式的边界
    if sidetype == 1:
        filename = 'boun3.dat'
        loadboun(filename)
        x0 = bx[0]
        y0 = by[0]
        x1 = bx[nboun]
        y1 = by[nboun]
        arc = bs[nboun]
        arcscatter(x0, y0, x1, y1, arc)
        savedata(1, boungridt_file, bounpoch_file)
    # sidetype=2 单段连续边界，函数形式，须改动
    elif sidetype == 2:
        cent_x = SMALL_COORDINATES_X
        cent_y = SMALL_COORDINATES_Y
        rad = SMALL_RADIUS  # 小圆半径
        pai = 2 * asin(1.0)

        x0 = cent_x + rad  # 起点
        y0 = cent_y + 0
        x1 = cent_x + rad  # 终点
        y1 = cent_y + 0
        arc = 2 * pai * rad  # 小圆周长
        arcscatter(x0, y0, x1, y1, arc)
        savedata(4, boungridt_file, bounpoch_file)
        # sidetype=3 分段连续边界，函数形式，须改动
    elif sidetype == 3:
        rad = BIG_RADIUS  # 大圆半径
        xbo, ybo, arcbo, npoch = xyarcbo()
        arcboun = 0  # 计算已并入的弧的总长度
        for iloop in range(0, 9):  # 遍历9段圆弧。 一共10个点，第一个点和最后一个点是同一个点
            x0 = xbo[iloop]  # 这段圆弧的起点
            y0 = ybo[iloop]
            x1 = xbo[iloop + 1]  # 下一段圆弧的起点:下一段圆弧和这一段属性不一样
            y1 = ybo[iloop + 1]
            arc = arcbo[iloop]  # 这段圆弧的弧长
            arcscatter(x0, y0, x1, y1, arc)  # 只是求出一个属性段上的边界点
            np = np - 1  # 最后一个点并进来，下次循环又会当作第一个点并进来，重复所以减1
            savendata(npoch[iloop], boungridt_file, bounpoch_file)
            arcboun = arcboun + arcbo[iloop]  # 计算已并入的弧的总长度，为了通过总弧长求x,y坐标
    boungridt_file.close()
    bounpoch_file.close()


# ****************************************************
# 单段连续边界，弧长arc和直角坐标x，y的关系，需改动
def arc_to_xy(arc):
    '''
    计算小圆上的坐标
    :param arc:  一段弧的长度，是小圆的话就是圆周长
    :return:    x,y 绝对位置
    '''
    rad = SMALL_RADIUS
    x = rad * cos(- arc / rad)
    y = rad * sin(- arc / rad)
    x = x + cent_x  # 偏移量
    y = y + cent_y
    return x, y


# 分段连续边界，各段起止点、弧长
def xyarcbo():
    '''
    可以理解为是一个大圆，圆上分为不同的圆弧，每段圆弧都有不同的属性，或是壁面或是入流
    :return:
    xbo: 每段小圆弧的起始点的x坐标
    ybo: 每段小圆弧的起始点的y坐标
    arcbo: 每段圆弧的弧长
    npoch: 每段圆弧的属性
    '''
    xbo = npp.zeros(100, float)
    ybo = npp.zeros(100, float)
    arcbo = npp.zeros(100, float)
    i = 0
    npoch = npp.zeros(100, int)
    pai = 2 * asin(1.0)
    arc = 0

    # 半径缩小，fSR管子尺寸不变，需修改成4个
    arcbo[0] = 15
    arcbo[1] = rad * (pai / 2) - 30
    arcbo[2] = 30
    arcbo[3] = rad * (pai / 2) - 30
    arcbo[4] = 30
    arcbo[5] = rad * (pai / 2) - 30
    arcbo[6] = 30
    arcbo[7] = rad * (pai / 2) - 30
    arcbo[8] = 15
    npoch[0] = 2
    npoch[1] = 1
    npoch[2] = 2
    npoch[3] = 1
    npoch[4] = 2
    npoch[5] = 1
    npoch[6] = 2
    npoch[7] = 1
    npoch[8] = 2
    for i in range(0, 10):  # 遍历10个点, 最后一个点和第一个点重合(225,0), 9段弧长
        xbo[i] = rad * cos(arc / rad)  # arc/rad = 圆心角度数, xbo,ybo是每段弧长起始点坐标
        ybo[i] = rad * sin(arc / rad)
        arc = arc + arcbo[i]
    return xbo, ybo, arcbo, npoch


# 分段连续边界，弧长arc和直角坐标x，y的关系，需改动
def arcn_to_xy(arc):
    '''
    计算大圆上的坐标
    :param arc: 新加入的弧长
    :return: x,y 新加入点的横纵坐标
    '''
    global arcboun
    x = rad * cos((arc + arcboun) / rad)  # L=θ*r,计算θ, x=rcosθ,rad在主函数里给出
    y = rad * sin((arc + arcboun) / rad)
    return x, y


# ************************************************
def savedata(npoch, boungridt_file, bounpoch_file):
    global boungridts, bounpochs
    global np, nboun, sidetype, nbs, bounarc, px, py, pstep, bx, by, bs
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    global bgnp, bgne, bgstep, bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    global arcboun
    i = 0
    for i in range(0, np - 1):
        boungridt_file.write(str(px[i]) + 5 * " " + str(py[i]) + "\n")
        bounpoch_file.write(str(npoch) + "\n")


# *******************************
def savendata(npoch, boungridt_file, bounpoch_file):
    '''
    每一段弧保存数据
    :param npoch: 这段弧的属性
    :param boungridt_file: 文件
    :param bounpoch_file: 文件
    :return:
    '''
    global boungridts, bounpochs
    global np, nboun, sidetype, nbs, bounarc, px, py, pstep, bx, by, bs
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    global bgnp, bgne, bgstep, bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    global arcboun
    i = 0
    for i in range(0, np):
        boungridt_file.write(str(px[i]) + 5 * " " + str(py[i]) + "\n")
    if npoch == 1:  # 如果是壁面，那么弧两端的两个点都要去掉
        np = np - 1
    else:  # 如果是入流点，那么弧两端的两个点都要加上，都是入流点
        np = np + 1
    for i in range(0, np):
        bounpoch_file.write(str(npoch) + "\n")


def arcscatter(x0, y0, x1, y1, arc):
    '''
    在一段弧上找所有边界点，特点是这个弧上属性是一样的，至少有起点和终点两个点
    :param x0:  这段圆弧的起点 x坐标
    :param y0:  这段圆弧的起点 y坐标
    :param x1:  下一段圆弧的起点 x坐标 (和上一段属性不一样)
    :param y1:  下一段圆弧的起点 y坐标
    :param arc:  这段圆弧的弧长
    '''
    global boungridts, bounpochs
    global np, nboun, sidetype, nbs, bounarc, px, py, pstep, bx, by, bs
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    global bgnp, bgne, bgstep, bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    global arcboun
    ee = 0
    arcxy = 0.00
    arc0 = 0.00
    arcstep = 0.00
    background_grid()  # 载入背景网格
    arcstep = asin(1.0) * 10  # 2*asin(1.0)=pai  5pai   没用到
    np = 1  # 每一段弧的np都要重新计数
    nbs = 1
    px[np - 1] = x0  # px[0] = x0
    py[np - 1] = y0  # py[0] = y0
    x = px[np - 1]  # x0
    y = py[np - 1]  # y0
    ee, arcxy = search_boun(x, y, ee, arcxy)  # 求步长
    arc0 = 0.0  # 每到一个弧后重新置0，arc0相比pstep，要多一个新加点的步长，用作判断新加点合不合适
    pstep[np - 1] = 0  # 可以理解为这一条弧上已经使用了的长度，这个长度上的点都已确定
    arc0 = arc0 + arcxy  # arc0 用作判断，存储：从一段弧第一个点开始，到要加的点(x,y)的整个弧长或步长
    while True:
        if (arc - arc0) <= 0:  # 弧长 < 这个弧上加点的所有步长, 说明: 要新加的这一个点跑到了下一个属性段了，放弃
            arc0 = arc  # 这一属性的弧长赋值给arc0，arc0变小了
            x = x1  # 下一个属性段的起始点坐标(原来要加的那个点舍弃，使用下一个弧段的起点作为新加点)
            y = y1
            ee, arcxy = search_boun(x, y, ee, arcxy)  # 找 下一段弧的起始点(也就是这段弧的终点)的步长
            if (arcxy * 1.5) > (arc0 - pstep[np - 1]):  # 终点步长的1.5倍比这段弧剩下的长度大，不加点了，直接跳出循环把终点加进来
                break
        elif (arc - arc0) < arcxy:  # 要新加的点还在原来的弧上，但是要新加的点离终点(下一个弧起点)太近，取中点
            arc0 = (arc + arc0 - arcxy) / 2  # 取平均位置，加个点
            transfer_xy(arc0)  # 求出要新加入的点的坐标
            ee, arcxy = search_boun(x, y, ee, arcxy)  # 计算要新加入点的步长
        else:  # 要新加的点既没有跑到下一个属性段，又没有离得终点太近，说明可以加入
            transfer_xy(arc0)  # 直接计算这个点的坐标
            ee, arcxy = search_boun(x, y, ee, arcxy)  # 计算要新加点的步长

        if (arcxy * 1.5) <= (arc0 - pstep[np - 1]):  # arc0 - pstep[np-1] 就是上一个点的步长
            arc0 = arc0 - arcxy * 0.5
            # 可以理解为如果新加点的步长过小，那么上个点的步长可以小一点，不加这个点，返回循环重新判断新加点
        else:
            np = np + 1
            px[np - 1] = x  # 新加点的坐标
            py[np - 1] = y
            pstep[np - 1] = arc0  # 可以理解为这一条弧上已经使用了的长度
            arc0 = arc0 + arcxy
    np = np + 1  # 从break跳出来的，所以下一个属性段的起点直接并进来 = 最后一个点
    px[np - 1] = x1
    py[np - 1] = y1
    pstep[np - 1] = arc


# *****************************************
def background_grid():
    global boungridts, bounpochs
    global np, nboun, sidetype, nbs, bounarc, px, py, pstep, bx, by, bs
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    global bgnp, bgne, bgstep, bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    global arcboun
    i = 0
    j = 0
    bgn = open(background_nod_file, "r+")
    bgno = open(background_noe_file, "r+")
    bgg = open(background_gridt_file, "r+")
    bgs = open(background_step_file, "r+")
    bgncount = 0
    bggcount = 0
    for line in bgg.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        bgpx[bggcount] = current_line[0]
        bgpy[bggcount] = current_line[1]
        bggcount += 1
    bgnp = bggcount
    bgscount = 0
    for line in bgs.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        bgstep[bgscount] = current_line[0]
        bgscount = bgscount + 1
    for line in bgn.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        bgnod[0, bgncount] = current_line[0]
        bgnod[1, bgncount] = current_line[1]
        bgnod[2, bgncount] = current_line[2]
        bgncount = bgncount + 1
    bgne = bgncount
    bgn0count = 0
    for line in bgno.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        bgnoe[0, bgn0count] = current_line[0]
        bgnoe[1, bgn0count] = current_line[1]
        bgnoe[2, bgn0count] = current_line[2]
        bgn0count += 1
    bgn.close()
    bgno.close()
    bgg.close()
    bgs.close()
    for i in range(0, bgne):
        for j in range(0, 3):
            gx[j] = bgpx[bgnod[j, i] - 1]
            gy[j] = bgpy[bgnod[j, i] - 1]
        circumcircle()
        bgcx[i] = gcx
        bgcy[i] = gcy
        bgcr[i] = gcr


# ***********************************
def search_boun(xx, yy, result, step):
    ''' 和delaundry函数有点区别,判断边界点是不是合理'''
    global boungridts, bounpochs
    global np, nboun, sidetype, nbs, bounarc, px, py, pstep, bx, by, bs
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    global bgnp, bgne, bgstep, bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    global arcboun
    i = 0
    j = 0
    k = 0
    nbg = npp.zeros(3, int)
    arr = npp.zeros([3, 3], float)
    dcp = 0
    bulk = npp.zeros(3, float)
    v1 = 0
    v2 = 0
    v4 = 0
    vol = npp.zeros(3, float)
    vmin = 1.0
    emin = 0
    for i in range(bgne - 1, -1, -1):
        nbg[0] = bgnoe[0, i]
        nbg[1] = bgnoe[1, i]
        nbg[2] = bgnoe[2, i]
        # if nbg[0] != 0 and nbg[1] != 0 and nbg[2] != 0:
        # continue
        gcx = bgcx[i]
        gcy = bgcy[i]
        gcr = bgcr[i]
        dcp = npp.sqrt((xx - gcx) ** 2 + (yy - gcy) ** 2)
        #  if((dcp-gcr)<gcr*fm2*1000)then
        for k in range(0, 3):
            for j in range(0, 3):
                arr[0, j] = 1
                arr[1, j] = bgpx[bgnod[j, i] - 1]
                arr[2, j] = bgpy[bgnod[j, i] - 1]
            arr[1, k] = xx
            arr[2, k] = yy
            bulk[k] = det(arr, 3)
        v1 = bulk[0] + bulk[1] + bulk[2]
        v2 = abs(bulk[0]) + abs(bulk[1]) + abs(bulk[2])
        v4 = (v2 - v1) / v1
        # if(v4<1e-4)then
        if vmin > v4:
            vmin = v4
            emin = i + 1
            vol[0] = bulk[0]
            vol[1] = bulk[1]
            vol[2] = bulk[2]
    if emin == 0:
        print('error')
        return result, step
    v1 = vol[0] + vol[1] + vol[2]
    v2 = abs(vol[0]) + abs(vol[1]) + abs(vol[2])
    v4 = v1 + v2
    step = 0
    for k in range(0, 3):
        vol[k] = (vol[k] + abs(vol[k])) / v4
        step = step + bgstep[bgnod[k, emin - 1] - 1] * vol[k]
    result = emin
    return result, step


# *****************************************
def circumcircle():
    global boungridts, bounpochs
    global np, nboun, sidetype, nbs, bounarc, px, py, pstep, bx, by, bs
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    global bgnp, bgne, bgstep, bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    global arcboun
    i = 0
    arr = npp.zeros([2, 2], float)
    ver = npp.zeros(2, float)
    verx = npp.zeros(2, float)
    x1 = 0.0
    x2 = 0.0
    x3 = 0.0
    r1 = 0.0
    r2 = 0.0
    r3 = 0.0
    for i in range(0, 2):
        arr[i, 0] = gx[i] - gx[2]
        arr[i, 1] = gy[i] - gy[2]
        ver[i] = 0.5 * (arr[i, 0] ** 2 + arr[i, 1] ** 2)
    axeqb(arr, ver, 2, verx)  # 计算圆心和半径，解那个方程用的
    gcx = verx[0] + gx[2]
    gcy = verx[1] + gy[2]

    x1 = gx[0] - gcx
    x2 = gy[0] - gcy
    x3 = npp.sqrt(x1 * x1 + x2 * x2)
    r1 = x3
    x1 = gx[1] - gcx
    x2 = gy[1] - gcy
    x3 = npp.sqrt(x1 * x1 + x2 * x2)
    r2 = x3
    r3 = npp.sqrt(verx[0] ** 2 + verx[1] ** 2)
    gcr = (r1 + r2 + r3) / 3


# *************************************
def axeqb(arr1, verb1, num, verx1):
    arr = npp.zeros([num, num], float)
    verb = npp.zeros(num, float)
    verx = npp.zeros(num, float)
    i = 0
    j = 0
    k = 0
    real_1 = 0.0
    real_2 = 0.0
    for i in range(0, num):
        for j in range(0, num):
            arr[i, j] = arr1[i, j]
        verb[i] = verb1[i]

    for i in range(0, num - 1):
        real_1 = arr[i, i]
        for j in range(i + 1, num):
            if abs(arr[j, i]) > abs(real_1):
                for k in range(i, num):
                    real_1 = arr[i, k]
                    arr[i, k] = arr[j, k]
                    arr[j, k] = real_1
                real_1 = verb[i]
                verb[i] = verb[j]
                verb[j] = real_1
            real_1 = arr[i, i]
        real_1 = arr[i, i]
        arr[i, i] = 1.0
        if abs(real_1) < (10 ** -6):
            print("error1:3 point in 1 line")
            print(i, real_1)
            k = input()
            return
        for j in range(i + 1, num):
            arr[i, j] = arr[i, j] / real_1
        verb[i] = verb[i] / real_1
        for j in range(i + 1, num):
            real_2 = arr[j, i]
            arr[j, i] = 0.0
            for k in range(i + 1, num):
                arr[j, k] = arr[j, k] - real_2 * arr[i, k]
            verb[j] = verb[j] - real_2 * verb[i]
    if abs(arr[num - 1, num - 1]) < 10 ** -6:
        print("error2:3 point in 1 line")
        print(arr[num, num])
        k = input()
        return
    verx[num - 1] = verb[num - 1] / arr[num - 1, num - 1]
    for i in range(num - 2, -1, -1):
        verx[i] = verb[i]
        for j in range(num - 1, i, -1):
            verx[i] = verx[i] - arr[i, j] * verx[j]

    for i in range(0, num):
        verx1[i] = verx[i]


# ****************************************
def det(matri, num):
    '''I: num 数组的元素个数'''
    matrix = npp.zeros([num, num], float)
    i = 0
    j = 0
    k = 0
    sign_1 = 0
    det_matrix = 0.0
    real_1 = 0.0
    real_2 = 0.0
    for i in range(0, num):
        for j in range(0, num):
            matrix[j, i] = matri[i, j]
    det_matrix = 1
    sign_1 = 1
    for i in range(0, num - 1):
        real_1 = matrix[i, i]
        for j in range(i + 1, num):
            if abs(matrix[j, i]) > abs(real_1):
                for k in range(i, num):
                    real_1 = matrix[i, k]
                    matrix[i, k] = matrix[j, k]
                    matrix[j, k] = real_1
                real_1 = matrix[i, i]
                sign_1 = sign_1 * (-1)
        real_1 = matrix[i, i]
        if abs(real_1) < 10 ** (-15):
            return 0.0
        matrix[i, i] = 1.0
        det_matrix = det_matrix * real_1
        for j in range(i + 1, num):
            real_2 = matrix[j, i] / real_1
            matrix[j, i] = 0.0
            for k in range(i + 1, num):
                matrix[j, k] = matrix[j, k] - real_2 * matrix[i, k]
    det_matrix = det_matrix * matrix[num - 1, num - 1] * sign_1
    return det_matrix


# *********************************
def loadboun(filename):
    global boungridts, bounpochs
    global np, nboun, sidetype, nbs, bounarc, px, py, pstep, bx, by, bs
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    global bgnp, bgne, bgstep, bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    global arcboun
    i = 0
    fil = open(filename, "r")
    for line in fil.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        if i > 0:
            bx[i] = current_line[0]
            by[i] = current_line[1]
            bs[i] = current_line[2]
        else:
            nboun = current_line[0]
        i = i + 1
    fil.close()


# ***********************************
def transfer_xy(arc):
    global boungridts, bounpochs
    global np, nboun, sidetype, nbs, bounarc, px, py, pstep, bx, by, bs
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    global bgnp, bgne, bgstep, bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    global arcboun
    ratio = 0.00
    i = 0
    n = 0
    # sidetype=1 离散形式的边界
    if sidetype == 1:
        if bs[nbs - 1] >= arc:
            n = 1
            for i in range(nbs - 1, -1, -1):
                if bs[i] < arc:
                    n = i + 1
                    break
        elif bs[nbs - 1] < arc:
            n = nboun
            for i in range(nbs - 1, nboun):
                if bs[i] >= arc:
                    n = i
                    break
        nbs = n
        if n == 1 or n == nboun:
            x = bx[n - 1]
            y = by[n - 1]
        else:
            ratio = (arc - bs[n - 1]) / (bs[n] - bs[n - 1])
            x = bx[n - 1] + ratio * (bx[n] - bx[n - 1])
            y = by[n - 1] + ratio * (by[n] - by[n - 1])
        # sidetype=2 连续边界，函数形式
    elif sidetype == 2:
        x, y = arc_to_xy(arc)
    elif sidetype == 3:
        x, y = arcn_to_xy(arc)


main()
