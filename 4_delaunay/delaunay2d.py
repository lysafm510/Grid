'''start num ending edel nod大于零的元素都改为数组的下标'''
from math import sqrt
import numpy as npp

# *******************************************************************
# 4. delaunay三角化
#
# 只需调整输入文件即可，其他不变，等待结果
# 模块2中的文件
background_gridt_file = "bggridt.dat"
background_noe_file = "bgnoe.dat"
background_nod_file = "bgnod.dat"
background_step_file = "bgstep.dat"
# 模块3中的文件
side_gridt_file = "sidegridt.dat"
side_face_file = "sideface.dat"


# *******************************************************************


def not_empty(s):
    return s and s.strip()


# fortran中数组的大小不能是任意的，必须要给定一个大小
pmax = 100000
emax = 200000
delmax = 1000
bmax = 2000
fmin = 10 ** -8
fm2 = 10 ** -8

global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
np = 0  # 点的个数
ne = 0  # 三角形单元的个数
nsearch = 0  # 寻找到第几个单元
px = npp.zeros(pmax, float)  # x坐标，y坐标
py = npp.zeros(pmax, float)
ipx = npp.zeros(4, float)  # 存放点的临时横纵坐标
ipy = npp.zeros(4, float)
centx = 0.0  # 临时变量，可能放圆的质心
centy = 0.0
length = 0.0
nod = npp.empty((3, emax), int)  # nod是每个单元由哪几个点组成
noe = npp.empty((3, emax), int)  # 每个单元三个相邻的单元是哪几个
epoch = npp.zeros(emax, int)  # epoch是每个单元的属性，npoch是每个点的属性
cx = npp.zeros(emax, float)
cy = npp.zeros(emax, float)
cr = npp.zeros(emax, float)

global gx, gy, gcx, gcy, gcr, x, y, xce, yce
gx = npp.zeros(3, float)  # 临时变量
gy = npp.zeros(3, float)  # 临时变量
gcx = 0.0
gcy = 0.0
gcr = 0.0
x = 0.0
y = 0.0
xce = 0.0
yce = 0.0

global ndel, edel, neibn
ndel = 0
edel = npp.zeros(delmax, int)  # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
neibn = npp.zeros(delmax, int)  # 相邻单元的信息

global eos, side, nb, nps
eos = npp.zeros((2, bmax), int)
side = npp.zeros((3, bmax), int)  # side是边界，3可能是原来是三维的
nb = 0  # nb是边界数目
nps = 0  # nps可能是边界点数

global newnp, ecrit, eop, bgeop, pstep
newnp = 0
ecrit = npp.zeros(emax, int)  # 存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
eop = npp.zeros(pmax, int)  # 用来存放这个点的对应的单元的信息
bgeop = npp.zeros(pmax, int)  # 这个点在背景网格的哪一个单元里面
pstep = npp.zeros(pmax, float)  # 用来存放每一点的步长

global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
bgnp = 0  # 背景网格的点数
bgne = 0  # 背景网格的单元数
bgfail = 0
bgsearch = 0
bgpx = npp.zeros(pmax, float)  # 背景网格的每一个点的x坐标，y坐标以及步长
bgpy = npp.zeros(pmax, float)
bgstep = npp.zeros(pmax, float)
bgnod = npp.zeros((3, emax), int)  # 背景网格由哪三个点组成
bgnoe = npp.zeros((3, emax), int)  # 有哪三个相邻单元
bgepoch = npp.zeros(emax, int)  # 背景网格的属性
bgcx = npp.zeros(emax, float)  # 背景网格对应的外接圆的圆心和半径
bgcy = npp.zeros(emax, float)
bgcr = npp.zeros(emax, float)


def main():
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    np = 0
    i = 0
    j = 0
    k = 0
    nei = 0
    nfrontele = 0
    ep = 0
    xx = 0.0
    yy = 0.0
    step = 0.0
    boun_grid()  # 调入边界网格，多边形边界
    print("boun_grid ok")
    for i in range(0, ne):  # 判断每一个三角形单元是不是正常数组
        ecrit[i] = 0
        for j in range(0, 3):
            nei = noe[j, i]
            if nei == 0:
                ecrit[i] = 1
                break
    background_grid()  # 背景网格，控制网格的密度
    print("background grid ok")
    bgsearch = 0
    for i in range(0, bgne):  # 为每一个点赋值一个属性
        bgepoch[i] = 0
    for i in range(0, np):
        xx = px[i]
        yy = py[i]
        ep, step = search_in_bg(xx, yy, 1, ep, step)  # 检查每一个边界点对应着背景网格的哪一个单元，步长的大小
        if ep == 0:
            ep, step = search_boun(xx, yy, ep, step)  # 计算出边界点对应的步长
            if ep == 0:  # 防止出错，ep为背景网格的某一个单元，ep为背景网格的单元号，等于0代表没有找到
                print("error: search boungrid in bg no found", i)
                ep = input()
        bgeop[i] = ep  # 记录了第i个点在背景网格哪个单元
        pstep[i] = step  # 记录了这个点的步长，step为步长，相当于网格密度应该是多少，相当于把边界点每一个点的信息都给读出来
    # *********************************
    while True:
        advance_front()  # 边界向里面推进，一次生成很多个内部点
        for i in range(0, ne):
            if ecrit[i] != 1:  # 标记这个单元是不是正常，不正常就给它赋值为-1
                continue
            ecrit[i] = -1
        print("np=", newnp)  # newnp为新生成的点的个数
        for i in range(np, newnp):  # newnp为生成的新点的个数，就是刚生成的点的个数加上原来点的个数
            if i == 616:  # debug用的
                print(i)
            k = eop[i]  # 新生成的点由哪一个单元给推出来的，k是单元号，这样话就方便寻找，因为找的话肯定先从这一个单元找，这样速度就更快
            if k > ne:  # 如果一个点由一个单元推出来，那这个点往往在这个单元的外接圆内
                k = ne
            j = search_1st(i + 1, k)  # 寻找第一个包含它的单元，i就是这个点的编号，k就是推出的这个单元的编号，j就是找到的第一个包含这个点的单元
            if j == 0:  # j=0的话就说明没找到
                print("error:search_ist=0/i=", i)
                j = input()
                break
            search_all(i + 1, j)  # 找出其他所有的包含这个点的单元，根据i和j
            if ndel > 200:
                print("nodel=", ndel, "/i=", i)
                k = input()
            check_up(i + 1)  # 把刚找到的点引进去生成新的单元
            clear_up(i + 1)  # 把整个数组重新写
            if (i + 1) % 1000 == 0:
                print("i=", i + 1, ne)
        np = newnp  # 把引入的新的点数赋值给np,再去继续重复的去找新的点
        nfrontele = 0
        for i in range(0, ne):
            if ecrit[i] == -1:
                continue
            nfrontele += 1  # 推进的步数，每次都向内部推进很多点，一直推进到最后
            ecrit[i] = 0
            for j in range(0, 3):
                nei = noe[j, i]
                if nei == 0:
                    ecrit[i] = 1
                    break
                elif ecrit[nei - 1] == -1:
                    ecrit[i] = 1
                    break

        print('frontele=', nfrontele)
        if nfrontele == 0:
            break
    while True:
        i = np
        smooth()
        # 判断有没有三角形单元过于畸形，如果有畸形，就在加一个点，两种判断方法，第一就是看三角形的角，等边三角形肯定是最匀称的
        # 钝角超过某个阈值肯定不是那么匀称；或者就是一条边比另外两条边小很多
        if i == np:
            break
    optimize()  # 生成完网格后，最后平滑网格，因为最后可能还存在部分的网格有点畸形，用包含这个点的多边形的坐标平均来代替这个点，即质心的位置
    gri = open("gridt.dat", "w")  # 把新生成的点写到这个文件中去
    for i in range(0, np):
        gri.write(str(px[i]) + " ")  # 每个点的横纵坐标
        gri.write(str(py[i]) + "\n")
    gri.close()
    bge = open("bgeop.dat", "w")  # 把每一个点在背景网格的哪一个单元也写到文件中去
    for i in range(0, np):
        bge.write(str(bgeop[i]) + "\n")
    bge.close()
    pst = open("pstep.dat", "w")  # 把每一个点所对应的步长也写到文件中去
    for i in range(0, np):
        pst.write(str(pstep[i]) + "\n")
    pst.close()
    savedata()  # 保存数据


# *****************************************************
def boun_grid():  # 把边界上的每一个点给引进来，作三角化，检查它的边界完整不完整，再把外部的四个点删除
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    i = 0
    j = 0
    lastnp = 0
    k = 0
    xmax = 0.0
    xmin = 0.0
    ymax = 0.0
    ymin = 0.0
    len_x = 0.0
    len_y = 0.0
    nps = 0
    sid = open(side_gridt_file, "r")  # 读取边界点的信息，此为边界点的文件
    # np=sid.read(1) # np为边界点的个数
    sidcount = 0
    for line in sid.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        px[sidcount] = current_line[0]
        py[sidcount] = current_line[1]

        # np=sidcount
        # nps=np
        # for i in range(0, np-1):
        #     px[i], py[i]=sid.read(2) # 每个边界点对应的X坐标和y坐标
        if sidcount == 0:
            xmax = px[sidcount]
            xmin = px[sidcount]
            ymax = py[sidcount]
            ymin = py[sidcount]
        else:
            if xmax < px[sidcount]:
                xmax = px[sidcount]
            if xmin > px[sidcount]:
                xmin = px[sidcount]
            if ymax < py[sidcount]:
                ymax = py[sidcount]
            if ymin > py[sidcount]:
                ymin = py[sidcount]
        sidcount = sidcount + 1
    np = sidcount
    nps = np
    sid.close()
    print("read ok")
    centx = (xmax + xmin) / 2
    centy = (ymax + ymin) / 2
    len_x = xmax - xmin
    len_y = ymax - ymin
    length = max(len_x, len_y)
    length = 1.2 * length
    convex_hull()
    ne = 2
    lastnp = -1
    nsearch = 0
    for i in range(lastnp + 1, np):  # 把边界点连成网格
        if i == 500:
            print("234")
        j = search_1st(i + 1, ne)  # 搜寻第一个三角形单元，遵循某个路径
        search_all(i + 1, j)  # 以第一个找的三角形单元为基础，再把其他所有的都搜出来
        if ndel >= 200:
            print("nodel=", ndel, "/i=", i)
            k = input()
        check_up(i + 1)  # 最后是个多边形包住这个点，多边形的每一条边和这个点相连成新的单元
        clear_up(i + 1)  # 在数组里面，把所有刚才删除的单元给清掉，再对新的单元重新排序
        if (i + 1) % 100 == 0:
            print("i+1=", i + 1, ne)  # 每100步打印一下，人可以看到进度，ne是单元数
    print("checkside start")
    checkside()  # 检查边界完整性
    print("checkside finished")
    delete_outside()  # 把边界外面引入的四个点全部删掉，删掉以后剩下的就是我们真正需要的
    savedata()


# ***************************************8
def convex_hull():  # 先引入四个点把整个边界都给框起来，用凸多边形把边界包住
    '''o:cx cy cr'''
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    i = 0
    j = 0
    ipx[0] = centx - 0.65 * length
    ipy[0] = centy - 0.6 * length
    ipx[1] = centx + 0.55 * length
    ipy[1] = centy - 0.6 * length
    ipx[2] = centx + 0.6 * length
    ipy[2] = centy + 0.6 * length
    ipx[3] = centx - 0.6 * length
    ipy[3] = centy + 0.6 * length

    nod[0, 0] = -1
    nod[1, 0] = -2
    nod[2, 0] = -4
    nod[0, 1] = -2
    nod[1, 1] = -3
    nod[2, 1] = -4

    noe[0, 0] = 2
    noe[1, 0] = 0
    noe[2, 0] = 0
    noe[0, 1] = 0
    noe[1, 1] = 1
    noe[2, 1] = 0
    for i in range(0, 2):
        for j in range(0, 3):
            gx[j] = ipx[-nod[j, i] - 1]
            gy[j] = ipy[-nod[j, i] - 1]
        circumcircle()  # 计算外部那四点所构成的三角形的外接圆的，记下它的圆心和半径
        cx[i] = gcx
        cy[i] = gcy
        cr[i] = gcr


# ***********************************8
def search_1st(p, start):  # 按照某个路径寻找第一个点
    '''o:ending'''
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    current = 0
    last = 0
    next = 0
    key = 0
    i = 0
    j = 0
    k = 0
    dcp = 0.0
    dep = 0.0
    x = px[p - 1]
    y = py[p - 1]
    nsearch = nsearch + 1
    ending = 0
    current = start  # start 是最后一个三角形
    for i in range(0, ne):
        if epoch[current - 1] == nsearch:
            break
        gcx = cx[current - 1]
        gcy = cy[current - 1]
        gcr = cr[current - 1]
        dcp = sqrt((x - gcx) ** 2 + (y - gcy) ** 2)
        if dcp < gcr:
            ending = current  # 找到这个三角形了，就是current，就是start，赋值返回ending
            break
        epoch[current - 1] = nsearch  # epoch 把这个三角形标为1，表示读过
        dep = -1
        next = 0
        for j in range(0, 3):  # 没找到
            k = noe[j, current - 1]  # 下一个三角形
            if k < 1 or k == last or epoch[k - 1] == nsearch:  # 找到邻居单元
                continue
            gcx = cx[k - 1]  # 邻居单元的圆心坐标和半径
            gcy = cy[k - 1]
            gcr = cr[k - 1]
            dcp = sqrt((x - gcx) ** 2 + (y - gcy) ** 2)  # dcp 距离
            if dcp < gcr:  # 判断
                ending = current  # current 赋值给 ending
                break
            centroid(k)  # 计算k这个单元的质心,计算结果是xce,yce
            dcp = sqrt((x - xce) ** 2 + (y - yce) ** 2)
            if dep < 0 or dep > dcp:
                dep = dcp
                next = k

        if next == 0:
            break
        last = current
        current = next

    current = ending
    ending = 0
    if current > 0:
        key = in_or_out(p, current)
        if key == -1:
            search_all(p, current)
            for i in range(0, ndel):
                j = edel[i]
                k = in_or_out(p, j)
                if k > -1:
                    ending = j
                    break
        else:
            ending = current
    if ending == 0:
        for i in range(ne - 1, -1, -1):
            gcx = cx[i]
            gcy = cy[i]
            gcr = cr[i]
            dcp = sqrt((x - gcx) ** 2 + (y - gcy) ** 2)
            if dcp < gcr:
                key = in_or_out(p, i + 1)
                if key == -1:
                    continue
                else:
                    ending = i + 1
                    break
    return ending


# **********************************************
def search_all(p, ending):  # 以刚才那个为基准找所有的
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    ele = 0
    nei = 0
    num = 0
    k = 0
    j = 0
    add = 0
    dcp = 0.0
    ndel = 1
    edel[ndel - 1] = ending
    x = px[p - 1]
    y = py[p - 1]
    num = 1
    while True:
        ele = edel[num - 1]
        for k in range(0, 3):
            nei = noe[k, ele - 1]
            if nei <= 0:
                continue
            gcx = cx[nei - 1]
            gcy = cy[nei - 1]
            gcr = cr[nei - 1]
            dcp = sqrt((x - gcx) ** 2 + (y - gcy) ** 2)
            if (dcp - gcr) < (fm2 * gcr):
                add = 1
                for j in range(0, ndel):
                    if edel[j] == (nei):
                        add = 0
                        break
                if add == 1:
                    ndel = ndel + 1
                    edel[ndel - 1] = nei
        num = num + 1
        if num > ndel:
            break


# **********************************************
def check_up(p):  # 找到所有单元之后，判断哪些单元要删除
    '''O: edel()  epoch() ndel'''
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    j = 0
    k = 0
    ele = 0
    nei = 0
    ndel1 = 0
    flag = 0
    vol1 = 0.0
    vol2 = 0.0
    pp = npp.zeros(3, int)
    for j in range(0, ndel):
        epoch[edel[j] - 1] = -nsearch
    ndel1 = ndel
    while True:
        flag = 0
        for j in range(0, ndel1):
            ele = edel[j]
            for k in range(0, 3):
                pp[k] = nod[k, ele - 1]
            for k in range(0, 3):
                nei = noe[k, ele - 1]
                if (nei) > 0 and epoch[nei - 1] == -nsearch:
                    continue
                else:
                    pp[k] = p
                    vol1 = area(pp[0], pp[1], pp[2])
                    pp[k] = nod[k, ele - 1]
                    vol2 = distance(pp[0], pp[1], pp[2], k)
                    if vol1 / vol2 < 10 ** -8:
                        flag = 1
                        break
            if flag == 1:
                epoch[ele - 1] = 0
                edel[j] = edel[ndel1 - 1]
                ndel1 = ndel1 - 1
                break
        if flag == 0:
            break

    ndel = ndel1


# *******************************************
def clear_up(p):  # 把该删除的单元都删除掉，把编号都更新，要么就是用新的单元来填充，要么就是把后面的单元号往前推
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    i = 0
    j = 0
    k = 0
    ele = 0
    fill = 0
    nei = 0
    nnew = 0
    n1 = 0
    n2 = 0
    n3 = 0
    arr1 = npp.zeros(3, int)
    arr2 = npp.zeros(3, int)
    nnew = ne
    for i in range(0, ndel):
        ele = edel[i]
        for j in range(0, 3):
            nei = noe[j, ele - 1]
            if nei <= 0:
                nnew = nnew + 1
                nod[j, nnew - 1] = p
                for k in range(0, 3):
                    if k == j:
                        continue
                    nod[k, nnew - 1] = nod[k, ele - 1]
                noe[j, nnew - 1] = nei
                neibn[nnew - ne - 1] = neibn[nnew - ne - 1] + 1
            elif epoch[nei - 1] != -nsearch:
                nnew = nnew + 1
                nod[j, nnew - 1] = p
                for k in range(0, 3):
                    if k == j:
                        continue
                    nod[k, nnew - 1] = nod[k, ele - 1]
                noe[j, nnew - 1] = nei
                neibn[nnew - ne - 1] = neibn[nnew - ne - 1] + 1
                for k in range(0, 3):
                    if noe[k, nei - 1] == ele:
                        noe[k, nei - 1] = nnew
                        break
    for i in range(ne, nnew - 1):
        if neibn[i - ne] == 3:
            continue
        for k in range(0, 3):
            arr1[k] = nod[k, i]
        for j in range(i + 1, nnew):
            if neibn[j - ne] == 3:
                continue
            for k in range(0, 3):
                arr2[k] = nod[k, j]
            n1, n2, n3 = common_point(arr1, arr2)
            if n3 != 2:
                continue
            neibn[i - ne] = neibn[i - ne] + 1
            neibn[j - ne] = neibn[j - ne] + 1
            noe[n1 - 1, i] = j + 1
            noe[n2 - 1, j] = i + 1
            if neibn[i - ne] == 3:
                break
    for i in range(0, nnew - ne):
        neibn[i] = 0
        epoch[i + ne] = 0
        ecrit[i + ne] = 0

    fill = nnew
    for i in range(0, ndel):
        ele = edel[i]
        if ele > nnew - ndel:
            continue
        for j in range(0, 3):
            nod[j, ele - 1] = nod[j, fill - 1]
            noe[j, ele - 1] = noe[j, fill - 1]
        ecrit[ele - 1] = ecrit[fill - 1]
        epoch[ele - 1] = epoch[fill - 1]
        for j in range(0, 3):
            nei = noe[j, ele - 1]
            if nei <= 0:
                continue
            for k in range(0, 3):
                if noe[k, nei - 1] == fill:
                    noe[k, nei - 1] = ele
        fill = fill - 1
        while True:
            if epoch[fill - 1] == -nsearch:
                fill = fill - 1
            else:
                break
        for j in range(0, 3):
            k = nod[j, ele - 1]
            if k < 0:
                gx[j] = ipx[-k - 1]
                gy[j] = ipy[-k - 1]
            else:
                gx[j] = px[k - 1]
                gy[j] = py[k - 1]
        circumcircle()
        cx[ele - 1] = gcx
        cy[ele - 1] = gcy
        cr[ele - 1] = gcr

    for i in range(ne + 1, nnew - ndel + 1):
        ele = i
        for j in range(0, 3):
            k = nod[j, ele - 1]
            if k < 0:
                gx[j] = ipx[-k - 1]
                gy[j] = ipy[-k - 1]
            else:
                gx[j] = px[k - 1]
                gy[j] = py[k - 1]
        circumcircle()  # 计算外接圆，下次再比较的时候就可以直接看这个点，看圆心的距离和这个点的距离是大于还是小于半径，就知道在园内还是圆外
        cx[ele - 1] = gcx
        cy[ele - 1] = gcy
        cr[ele - 1] = gcr
    ne = nnew - ndel


# **************************************
def common_point(arr1, arr2):  # 判断这两个多边形有几个共同点，两个三角形单元如果有两个共同的点就说明有一条边是相同的，有一个共同点就说明是个顶点
    n3 = 0
    n1 = 6
    n2 = 6
    i = 0
    j = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if arr2[j] == arr1[i]:
                n3 = n3 + 1
                n1 = n1 - i - 1
                n2 = n2 - j - 1
                break
    return n1, n2, n3


# ***********************
def in_or_out(p, e):  # 计算点p在单元e里面还是外面，和外接圆圆心还不同，计算这个点包含在哪个背景网格里面
    '''O:key'''
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    v1 = 0.0
    v2 = 0.0
    v3 = 0.0
    v = 0.0
    vv = 0.0
    v1 = area(p, nod[1, e - 1], nod[2, e - 1])  # 计算点p和这个三角形单元的三个点所组成的面积
    v2 = area(nod[0, e - 1], p, nod[2, e - 1])  # 如果这个点在三角形内部的话，那么这三个图形的面积就等于三角形的总面积
    v3 = area(nod[0, e - 1], nod[1, e - 1], p)  # 如果这个点在三角形外面的话，那么加起来就要大一点
    v = v1 + v2 + v3  # 计算是按照顺序的，如果三角形是按照逆时针的话，计算出来就是正的，否则就是负的
    vv = (abs(v1) + abs(v2) + abs(v3) - v) / v  # 如果点在三角形外面，取绝对值之后，得到的三个三角形的面积就大于原来三角形的面积
    if vv < 10 ** -8:
        key = 1
    else:
        key = -1
    return key


# ***********************************
def centroid(e):  # 计算e这个单元的质心
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    i = 0
    pp = npp.zeros(3, int)
    xce = 0
    yce = 0
    for i in range(0, 3):
        pp[i] = nod[i, e - 1]
        if pp[i] >= 0:
            xce = xce + px[pp[i] - 1] / 3.0
            yce = yce + py[pp[i] - 1] / 3.0
        else:
            xce = xce + ipx[-pp[i] - 1] / 3.0
            yce = yce + ipy[-pp[i] - 1] / 3.0


# ********************************************
def circumcircle():  # 计算外接圆的圆心和半径的
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
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
    x3 = sqrt(x1 * x1 + x2 * x2)
    r1 = x3
    x1 = gx[1] - gcx
    x2 = gy[1] - gcy
    x3 = sqrt(x1 * x1 + x2 * x2)
    r2 = x3
    r3 = sqrt(verx[0] ** 2 + verx[1] ** 2)
    gcr = (r1 + r2 + r3) / 3


# *******************************************
def axeqb(arr1, verb1, num, verx1):  # 解方程用的
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
        if abs(real_1) < (10 ** -8):
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
    if abs(arr[num - 1, num - 1]) < 10 ** -8:
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


# *****************************************
def area(p1, p2, p3):  # 计算三角形的面积，判断点在三角形的内部还是外部
    '''I:p1 p2 p2 下标加1
        o:vol 输出'''
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    i = 0
    vol = 0.0
    pp = npp.zeros(3, int)
    arr = npp.zeros((3, 3), float)
    det_arr = 0.0
    pp[0] = p1
    pp[1] = p2
    pp[2] = p3
    for i in range(0, 3):
        arr[0, i] = 1
        if pp[i] > -1:
            arr[1, i] = px[pp[i] - 1]
            arr[2, i] = py[pp[i] - 1]
        else:
            arr[1, i] = ipx[-pp[i] - 1]
            arr[2, i] = ipy[-pp[i] - 1]
    det_arr = det(arr, 3)
    vol = det_arr / 2.0
    return vol


# ***********************************************
def distance(p1, p2, p3, n):  # 计算p1和p2的距离，p3是三维时候的变量，实际上p3没用到，比如判断一个点是否在外接圆里面，就要求它和圆心的距离
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    pp = npp.zeros(3, int)
    x1 = 0.0
    y1 = 0.0
    x2 = 0.0
    y2 = 0.0
    vol = 0.0
    pp[0] = p1
    pp[1] = p2
    pp[2] = p3
    pp[n] = p3
    if pp[0] > 0:
        x1 = px[pp[0] - 1]
        y1 = py[pp[0] - 1]
    else:
        x1 = ipx[-pp[0] - 1]
        y1 = ipy[-pp[0] - 1]
    if pp[1] > -1:
        x2 = px[pp[1] - 1]
        y2 = py[pp[1] - 1]
    else:
        x2 = ipx[-pp[1] - 1]
        y2 = ipy[-pp[1] - 1]
    vol = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # vol就是求得的距离的值
    return vol


# ********************************************
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


# **********************************************
def savedata():  # 把数据保存起来
    i = 0
    no1 = open("nod.dat", "w")
    no2 = open("noe.dat", "w")
    ci = open("cir.dat", "w")
    # no1.write(str(ne) + "\n")
    for i in range(0, ne):
        no1.write(str(nod[0, i]) + " ")
        no1.write(str(nod[1, i]) + " ")
        no1.write(str(nod[2, i]) + "\n")
        no2.write(str(noe[0, i]) + " ")
        no2.write(str(noe[1, i]) + " ")
        no2.write(str(noe[2, i]) + "\n")
        ci.write(str(cx[i]) + " ")
        ci.write(str(cy[i]) + " ")
        ci.write(str(cr[i]) + "\n")
    # no1.write(str(np) + "\n")
    no1.close()
    no2.close()
    ci.close()


# ***************************************
def checkside():  # 检查边界玩不完整，每一条边界都是三角形的一条边
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    pp1 = npp.zeros(3, int)
    pp2 = npp.zeros(3, int)
    i = 0
    j = 0
    k = 0
    p = 0
    start = 0
    ending = 0
    nei = 0
    n1 = 0
    n2 = 0
    n3 = 0
    vol = 0.0
    sid_file = open(side_face_file, "r")
    sidconut = 0
    for line in sid_file.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        side[0, i] = current_line[0]
        side[1, i] = current_line[1]
        side[2, i] = current_line[2]
        i += 1
        sidconut = sidconut + 1
    nb = sidconut
    sid_file.close()
    nsearch = 0
    for j in range(0, ne):
        epoch[j] = 0
    start = 1
    for i in range(0, nb):
        if i == 444:
            print("123")
        k = ((i + 1) % 100) + 1
        p = np + k
        pp1[0] = side[0, i]
        pp1[1] = side[1, i]
        pp1[2] = 0
        px[p - 1] = (px[side[0, i] - 1] + px[side[1, i] - 1]) / 2.0
        py[p - 1] = (py[side[0, i] - 1] + py[side[1, i] - 1]) / 2.0
        ending = search_1st(p, start)
        pp2[0] = nod[0, ending - 1]
        pp2[1] = nod[1, ending - 1]
        pp2[2] = nod[2, ending - 1]
        n1, n2, n3 = common_point(pp1, pp2)
        if n3 != 2:
            for j in range(0, 3):
                nei = noe[j, ending - 1]
                pp2[0] = nod[0, nei - 1]
                pp2[1] = nod[1, nei - 1]
                pp2[2] = nod[2, nei - 1]
                n1, n2, n3 = common_point(pp1, pp2)
                if n3 == 2 and n1 == 3:
                    ending = nei
                    break
        if n3 != 2:
            search_all(p, ending)
            for j in range(0, ndel):
                nei = edel[j]
                pp2[0] = nod[0, nei - 1]
                pp2[1] = nod[1, nei - 1]
                pp2[2] = nod[2, nei - 1]
                n1, n2, n3 = common_point(pp1, pp2)
                if n3 == 2 and n1 == 3:
                    ending = nei
                    break
        if n3 == 2 and n1 == 3:
            start = ending
            vol = area(pp1[0], pp1[1], pp2[n2 - 1])
            if vol < 0:
                eos[1, i] = ending
                eos[0, i] = noe[n2 - 1, ending - 1]
                pp2[0] = nod[0, noe[n2 - 1, ending - 1] - 1]
                pp2[1] = nod[1, noe[n2 - 1, ending - 1] - 1]
                pp2[2] = nod[2, noe[n2 - 1, ending - 1] - 1]
                j = noe[n2 - 1, ending - 1]
                n1, n2, n3 = common_point(pp1, pp2)
                vol = area(pp1[0], pp1[1], pp2[n2 - 1])
                if vol < 0 or n1 != 3 or n3 != 2 or (noe[n2 - 1, j - 1]) != ending:
                    print("error")
            else:
                eos[0, i] = ending
                eos[1, i] = noe[n2 - 1, ending - 1]
                pp2[0] = nod[0, noe[n2 - 1, ending - 1] - 1]
                pp2[1] = nod[1, noe[n2 - 1, ending - 1] - 1]
                pp2[2] = nod[2, noe[n2 - 1, ending - 1] - 1]
                j = noe[n2 - 1, ending - 1]
                n1, n2, n3 = common_point(pp1, pp2)
                vol = area(pp1[0], pp1[1], pp2[n2 - 1])
                if vol > 0 or n1 != 3 or n3 != 2 or (noe[n2 - 1, j - 1]) != ending:
                    print("error")
        else:
            print("error:ending do not include s", i, ending)
            j = input()
        if (i + 1) % 100 == 0:
            print("i+1=", i + 1)
            nsearch = 0
            for j in range(0, ne):
                epoch[j] = 0


# ************************************************
def delete_outside():  # 在边界点引进来之后，把外面那四个点及其组成的单元全部删掉
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    i = 0
    j = 0
    k = 0
    e1 = 0
    e2 = 0
    nei = 0
    flag = 0
    for i in range(0, nb):
        e1 = eos[0, i]
        e2 = eos[1, i]
        flag = 0
        for j in range(0, 3):
            nei = noe[j, e1 - 1]
            if nei != e2:
                continue
            noe[j, e1 - 1] = 0
            flag = flag + 1
        for j in range(0, 3):
            nei = noe[j, e2 - 1]
            if nei != e1:
                continue
            noe[j, e2 - 1] = 0
            flag = flag + 1
        if flag != 2:
            print("error")
    print("inside and outside separate finished!")
    for i in range(0, nb):
        e2 = eos[1, i]
        nod[0, e2 - 1] = 0
        nod[1, e2 - 1] = 0
        nod[2, e2 - 1] = 0
        for j in range(0, 3):
            nei = noe[j, e2 - 1]
            if nei == 0:
                continue
            nod[0, nei - 1] = 0
            noe[j, e2 - 1] = 0
    e1 = 0
    while True:
        flag = 0
        for i in range(0, ne):
            if nod[0, i] != 0:
                continue
            if nod[1, i] == 0:
                continue
            flag = flag + 1
            nod[1, i] = 0
            nod[2, i] = 0
            for j in range(0, 3):
                nei = noe[j, i]
                if nei == 0:
                    continue
                nod[0, nei - 1] = 0
                noe[j, i] = 0
        print(e1)
        e1 = e1 + 1
        if flag == 0:
            break
    print("delete ok, times=", e1)
    e1 = 0
    for i in range(0, ne):
        if nod[0, i] == 0:
            continue
        e1 = e1 + 1
        if i + 1 == e1:
            continue
        for j in range(0, 3):
            nod[j, e1 - 1] = nod[j, i]
            noe[j, e1 - 1] = noe[j, i]
            cx[e1 - 1] = cx[i]
            cy[e1 - 1] = cy[i]
            cr[e1 - 1] = cr[i]
        for j in range(0, 3):
            nei = noe[j, i]
            if nei == 0:
                continue
            for k in range(0, 3):
                if noe[k, nei - 1] - 1 == i:
                    noe[k, nei - 1] = e1
    ne = e1
    print("rewrite delete ok,   ne=", ne)


# ********************************************
def advance_front():  # 用前沿推进方法来生成节点
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    i = 0
    j = 0
    k = 0
    m = 0
    n = 0
    nei = 0
    ep = 0
    emx = 0
    emn = 0
    bgep = 0
    p = 0
    f1 = 0.0
    f3 = 0.0
    step = 0.0
    xn = 0.0
    yn = 0.0
    vx = 0.0
    vy = 0.0
    lcs = 0.0
    lsp = 0.0
    xx = 0.0
    yy = 0.0
    x1 = 0.0
    x2 = 0.0
    y1 = 0.0
    y2 = 0.0
    pp = npp.zeros(3, int)
    ee = npp.zeros(2, int)
    p2 = npp.zeros(3, int)
    sx = npp.zeros(3, float)
    sy = npp.zeros(3, float)
    ss = npp.zeros(3, float)
    sr = npp.zeros(3, float)

    f1 = 0.7
    f3 = 0.3
    nsearch = 0
    for i in range(0, ne):
        epoch[i] = 0
    bgsearch = 0
    for i in range(0, bgne):
        bgepoch[i] = 0
    newnp = np
    for i in range(0, ne):
        if ecrit[i] != 1:
            continue
        pp[0] = nod[0, i]
        pp[1] = nod[1, i]
        pp[2] = nod[2, i]
        for j in range(0, 3):
            nei = noe[j, i]
            if nei > 0 and ecrit[nei - 1] != -1:
                continue
            m = j + 2
            n = m + 1
            # ？？？
            if m > 3:
                m = m - 3
            if n > 3:
                n = n - 3
            ee[0] = bgeop[pp[m - 1] - 1]
            ee[1] = bgeop[pp[n - 1] - 1]
            yn = px[pp[n - 1] - 1] - px[pp[m - 1] - 1]
            xn = py[pp[m - 1] - 1] - py[pp[n - 1] - 1]
            lsp = sqrt(xn * xn + yn * yn)
            xn = xn / lsp
            yn = yn / lsp
            lcs = (cx[i] - px[pp[n - 1] - 1]) * xn + (cy[i] - py[pp[n - 1] - 1]) * yn
            sx[j] = cx[i] - lcs * xn
            sy[j] = cy[i] - lcs * yn
            sr[j] = sqrt(cr[i] * cr[i] - lcs * lcs)
            emx = max(ee[0], ee[1])
            emn = min(ee[0], ee[1])
            if emx == emn:
                ss[j] = (pstep[pp[0] - 1] + pstep[pp[1] - 1]) / 2.0
            else:
                bgep, ss[j] = search_in_bg(sx[j], sy[j], emx, bgep, ss[j])
                if bgep == 0:
                    #  ss(j)=(pstep(pp(1))+pstep(pp(2)))/2.0
                    if nei != 0:
                        print("error:search=0", i, j, nei)
                        bgep = input()
                    else:
                        search_boun(sx[j], sy[j], bgep, ss[j])
                        if bgep == 0:
                            print("error:search=0", i, j, nei)
                            bgep = input()
            if ss[j] > 3.0 * sr[j]:
                ss[j] = 3.0 * sr[j]
            # 推进的新点坐标及其与该面构成的四面体外心及半径
            xx = sx[j] + ss[j] * xn
            yy = sy[j] + ss[j] * yn
            gcr = 0.5 * ss[j] + 0.5 * sr[j] * sr[j] / ss[j]
            gcx = xx - gcr * xn
            gcy = yy - gcr * yn
            # 以下为该点是否应存在的判定
            lcs = sqrt((gcx - px[pp[j] - 1]) ** 2 + (gcy - py[pp[j] - 1]) ** 2)
            if lcs < gcr:
                continue
            if bgep > 0:
                emx = bgep
            bgep, step = search_in_bg(xx, yy, emx, bgep, step)
            if bgep == 0:
                continue
            lcs = sqrt((xx - px[pp[j] - 1]) ** 2 + (yy - py[pp[j] - 1]) ** 2)
            if lcs < f1 * step:
                continue
            p = newnp + 1
            if p > pmax:
                print("newnp>pmax:", newnp, pmax)
                p = input()
            px[p - 1] = xx
            py[p - 1] = yy
            ep = search_1st(p, i + 1)
            if ep == 0:
                continue
            p2[0] = nod[0, ep - 1]
            p2[1] = nod[1, ep - 1]
            p2[2] = nod[2, ep - 1]
            for k in range(0, 3):
                lcs = sqrt((px[p2[k] - 1] - xx) ** 2 + (py[p2[k] - 1] - yy) ** 2)
                lsp = pstep[p2[k] - 1] * f1
                if lcs < f1 * step and lcs < lsp:
                    p = 0
                    break
            if p == 0:
                continue
            for k in range(0, 3):
                nei = noe[k, ep - 1]
                if nei != 0:
                    continue
                m = k + 2
                n = m + 1
                if m > 3:
                    m = m - 3
                if n > 3:
                    n = n - 3
                vx = py[p2[m - 1] - 1] - py[p2[n - 1] - 1]
                vy = px[p2[n - 1] - 1] - px[p2[m - 1] - 1]
                lsp = sqrt(vx * vx + vy * vy)
                vx = vx / lsp
                vy = vy / lsp
                lsp = abs(vx * (xx - px[p2[n - 1] - 1]) + vy * (yy - py[p2[n - 1] - 1]))
                if lsp < f3 * step:
                    p = 0
                    break
            if p == 0:
                continue
            search_all(p, ep)
            x1 = xx + step * f1
            x2 = xx - step * f1
            y1 = yy + step * f1
            y2 = yy - step * f1
            for k in range(1, ndel):
                for m in range(0, 3):
                    if px[nod[m, edel[k] - 1] - 1] > x1:
                        continue
                    if px[nod[m, edel[k] - 1] - 1] < x2:
                        continue
                    if py[nod[m, edel[k] - 1] - 1] > y1:
                        continue
                    if py[nod[m, edel[k] - 1] - 1] > y2:
                        continue
                    vx = px[nod[m, edel[k] - 1] - 1]
                    vy = py[nod[m, edel[k] - 1] - 1]
                    lcs = sqrt((vx - xx) ** 2 + (vy - yy) ** 2)
                    if lcs < f1 * step:
                        p = 0
                        break
                if p == 0:
                    break
            if p == 0:
                continue
            newnp = newnp + 1
            pstep[newnp - 1] = step
            eop[newnp - 1] = ep
            bgeop[newnp - 1] = bgep

    for i in range(np, newnp):
        if eop[i] == 0:
            continue
        for j in range(i + 1, newnp):
            if eop[j] == 0:
                continue
            if pstep[j] < pstep[i]:
                xx = px[i]
                px[i] = px[j]
                px[j] = xx
                yy = py[i]
                py[i] = py[j]
                py[j] = yy
                step = pstep[i]
                pstep[i] = pstep[j]
                pstep[j] = step
                ep = eop[i]
                eop[i] = eop[j]
                eop[j] = ep
                bgep = bgeop[i]
                bgeop[i] = bgeop[j]
                bgeop[j] = bgep
        xx = px[i]
        yy = py[i]
        step = pstep[i] * f1
        x1 = xx - step
        x2 = xx + step
        y1 = yy - step
        y2 = yy + step
        for j in range(i + 1, newnp):
            if px[j] < x1 or px[j] > x2:
                continue
            if py[j] < y1 or py[j] > y2:
                continue
            lcs = sqrt((px[j] - xx) ** 2 + (py[j] - yy) ** 2)
            if lcs < step:
                eop[j] = 0

    p = np
    for i in range(np, newnp):
        if eop[i] == 0:
            continue
        p = p + 1
        if i + 1 == p:
            continue
        bgeop[p - 1] = bgeop[i]
        pstep[p - 1] = pstep[i]
        eop[p - 1] = eop[i]
        px[p - 1] = px[i]
        py[p - 1] = py[i]
    newnp = p
    nsearch = 0
    for i in range(0, ne):
        epoch[i] = 0


# ***************************************
def background_grid():  # 读取背景网格的信息
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    i = 0
    j = 0
    bgn = open(background_gridt_file, "r+")
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


# ****************************************************
def search_in_bg(xx, yy, start, result, step):  # 搜查这个点在背景网格哪个单元，start是从背景网格哪一个地方搜寻，因为有时候背景网格很复杂的话，搜寻也是讲究以定策略的
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    bulki = 0.0
    i = 0
    j = 0
    nei = 0
    k = 0
    last = 0
    next = 0
    current = 0
    e = 0
    arr = npp.zeros([3, 3], float)
    dcp = 0.0
    dep = 0.0
    bulk = npp.zeros(3, float)
    v1 = 0.0
    v2 = 0.0
    v3 = 0.0
    v4 = 0.0
    bgsearch = bgsearch + 1
    current = start
    result = 0
    next = 0
    last = 0
    for i in range(0, bgne):
        if bgepoch[current - 1] == bgsearch:
            break
        gcx = bgcx[current - 1]
        gcy = bgcy[current - 1]
        gcr = bgcr[current - 1]
        dcp = sqrt((xx - gcx) ** 2 + (yy - gcy) ** 2)
        if (dcp - gcr) < gcr * fm2:
            result = current
            break
        bgepoch[current - 1] = bgsearch
        dep = -1
        next = 0
        for j in range(0, 3):
            nei = bgnoe[j, current - 1]
            if nei < 1 or nei == last or bgepoch[nei - 1] == bgsearch:
                continue
            gcx = bgcx[nei - 1]
            gcy = bgcy[nei - 1]
            gcr = bgcr[nei - 1]
            dcp = sqrt((xx - gcx) ** 2 + (yy - gcy) ** 2)
            if (dcp - gcr) < gcr * fm2:
                result = current
                break
            xce = 0
            yce = 0
            for k in range(0, 3):
                xce = xce + bgpx[bgnod[k, nei - 1] - 1] / 3.0
                yce = yce + bgpy[bgnod[k, nei - 1] - 1] / 3.0
            dcp = sqrt((xx - xce) ** 2 + (yy - yce) ** 2)
            if dep < 0 or dep > dcp:
                dep = dcp
                next = nei
        if next == 0:
            break
        last = current
        current = next
    current = result
    result = 0
    if current > 0:
        for i in range(0, 3):
            for j in range(0, 3):
                arr[0, j] = 1
                arr[1, j] = bgpx[bgnod[j, current - 1] - 1]
                arr[2, j] = bgpy[bgnod[j, current - 1] - 1]
            arr[1, i] = xx
            arr[2, i] = yy
            bulk[i] = det(arr, 3)

        v1 = bulk[0] + bulk[1] + bulk[2]
        v2 = abs(bulk[0]) + abs(bulk[1]) + abs(bulk[2])
        v3 = (v2 - v1) / v1
        if v3 < 10 ** -8:
            result = current
            step = 0
            for i in range(0, 3):
                bulk[i] = bulk[i] / v1
                step = step + bgstep[bgnod[i, result - 1] - 1] * bulk[i]
        else:
            search_bg_all(xx, yy, current)
            for i in range(0, ndel):
                e = edel[i]
                for k in range(0, 3):
                    for j in range(0, 3):
                        arr[0, j] = 1
                        arr[1, j] = bgpx[bgnod[j, e - 1] - 1]
                        arr[2, j] = bgpy[bgnod[j, e - 1] - 1]
                    arr[1, k] = xx
                    arr[2, k] = yy
                    bulk[k] = det(arr, 3)
                v1 = bulk[0] + bulk[1] + bulk[2]
                v2 = abs(bulk[0]) + abs(bulk[1]) + abs(bulk[2])
                v4 = (v2 - v1) / v1
                if v4 < 10 ** -8:
                    result = e
                    step = 0
                    for k in range(0, 3):
                        bulk[k] = bulk[k] / v1
                        step = step + bgstep[bgnod[k, result - 1] - 1] * bulk[k]
                    break

    if result == 0:
        for i in range(bgne - 1, -1, -1):
            gcx = bgcx[i]
            gcy = bgcy[i]
            gcr = bgcr[i]
            dcp = sqrt((xx - gcx) ** 2 + (yy - gcy) ** 2)
            if (dcp - gcr) < gcr * fm2:
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
                if v4 < 10 ** -8:
                    result = i + 1
                    step = 0
                    for k in range(0, 3):
                        bulk[k] = bulk[k] / v1
                        step = step + bgstep[bgnod[k, result - 1] - 1] * bulk[k]
                    break
    return result, step  # step是这个点对应的背景网格算出来的步长
    # resurt是结果，如果在背景网格第五个单元里面，result就是5


# ******************************************************
def search_boun(xx, yy, result, step):  # 判断边界点是不是合理
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
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
        if nbg[0] != 0 and nbg[1] != 0 and nbg[2] != 0:
            continue
        gcx = bgcx[i]
        gcy = bgcy[i]
        gcr = bgcr[i]
        dcp = sqrt((xx - gcx) ** 2 + (yy - gcy) ** 2)
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


# **********************************************
def search_bg_all(xx, yy, ending):
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    ele = 0
    nei = 0
    # num = 0
    k = 0
    dcp = 0.0
    ndel = 1
    edel[ndel - 1] = ending
    num = 1
    bgepoch[ending - 1] = -bgsearch
    while True:
        ele = edel[num - 1]
        for k in range(0, 3):
            nei = bgnoe[k, ele - 1]
            if nei <= 0 or bgepoch[nei - 1] == -bgsearch:
                continue
            gcx = bgcx[nei - 1]
            gcy = bgcy[nei - 1]
            gcr = bgcr[nei - 1]
            dcp = sqrt((xx - gcx) ** 2 + (yy - gcy) ** 2)
            if (dcp - gcr) < (fm2 * gcr):
                ndel = ndel + 1
                edel[ndel - 1] = nei
                bgepoch[nei - 1] = -bgsearch
        num = num + 1
        if num > ndel:
            break


# ************************************************************************
def smooth():
    # 判断有没有三角形单元过于畸形，如果有畸形，就在加一个点，两种判断方法，第一就是看三角形的角，等边三角形肯定是最匀称的
    # 钝角超过某个阈值肯定不是那么匀称；或者就是一条边比另外两条边小很多
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    m = 0
    n = 0
    i = 0
    j = 0
    k = 0
    p = 0
    nei = 0
    bgep = 0
    ep = 0
    pp = npp.zeros(3, int)
    p2 = npp.zeros(3, int)
    s1 = npp.zeros(3, float)
    slmin = 0.0
    stmin = 0.0
    xx = 0.0
    yy = 0.0
    step = 0.0
    lcs = 0.0
    x1 = 0.0
    x2 = 0.0
    y1 = 0.0
    y2 = 0.0
    vx = 0.0
    vy = 0.0
    f1 = 0.5
    f2 = 1.2
    f5 = 1.0
    f3 = 0.3
    f4 = 0.5
    newnp = np
    bgsearch = 0
    for i in range(0, bgne):
        bgepoch[i] = 0
    for i in range(0, ne):
        pp[0] = nod[0, i]
        pp[1] = nod[1, i]
        pp[2] = nod[2, i]
        for j in range(0, 3):
            m = j + 2
            n = j + 3
            if m > 3:
                m = m - 3
            if n > 3:
                n = n - 3
            s1[j] = sqrt((px[pp[m - 1] - 1] - px[pp[n - 1] - 1]) ** 2 + (py[pp[m - 1] - 1] - py[pp[n - 1] - 1]) ** 2)
        slmin = min(s1[0], s1[1], s1[2])
        stmin = min(pstep[pp[0] - 1], pstep[pp[1] - 1], pstep[pp[2] - 1])
        if cr[i] > slmin * f2 or cr[i] > stmin * f5:
            xx = cx[i]
            yy = cy[i]
            bgep, step = search_in_bg(xx, yy, bgeop[pp[0] - 1], bgep, step)
            if bgep == 0:
                continue
            p = newnp + 1
            px[p - 1] = xx
            py[p - 1] = yy
            j = min(i + 1, ne)
            ep = search_1st(p, j)
            if ep == 0:
                continue
            p2[0] = nod[0, ep - 1]
            p2[1] = nod[1, ep - 1]
            p2[2] = nod[2, ep - 1]
            for k in range(0, 3):
                nei = noe[k, ep - 1]
                if nei != 0:
                    continue
                m = k + 2
                n = m + 1
                if m > 3:
                    m = m - 3
                if n > 3:
                    n = n - 3
                vx = py[p2[m - 1] - 1] - py[p2[n - 1] - 1]
                vy = px[p2[n - 1] - 1] - px[p2[m - 1] - 1]
                lcs = sqrt(vx * vx + vy * vy)
                vx = vx / lcs
                vy = vy / lcs
                lcs = abs(vx * (xx - px[p2[n - 1] - 1]) + vy * (yy - py[p2[n - 1] - 1]))
                if lcs < f3 * step:
                    p = 0
                    break
            if p == 0:
                continue
            search_all(p, ep)
            for j in range(0, ndel):
                for k in range(0, 3):
                    vx = px[nod[k, edel[j] - 1] - 1]
                    vy = py[nod[k, edel[j] - 1] - 1]
                    lcs = sqrt((vx - xx) ** 2 + (vy - yy) ** 2)
                    if (lcs < f4 * step) and (lcs < slmin * f4):
                        p = 0
                        break
                if p == 0:
                    break
            if p == 0:
                continue
            newnp = newnp + 1
            px[newnp - 1] = xx
            py[newnp - 1] = yy
            bgeop[newnp - 1] = bgep
            pstep[newnp - 1] = step
            eop[newnp - 1] = ep
    for i in range(np, newnp):
        if eop[i] == 0:
            continue
        for j in range(i + 1, newnp):
            if eop[j] == 0:
                continue
            if pstep[j] < pstep[i]:
                xx = px[i]
                px[i] = px[j]
                px[j] = xx
                yy = py[i]
                py[i] = py[j]
                py[j] = yy
                step = pstep[i]
                pstep[i] = pstep[j]
                pstep[j] = step
                ep = eop[i]
                eop[i] = eop[j]
                eop[j] = ep
                bgep = bgeop[i]
                bgeop[i] = bgeop[j]
                bgeop[j] = bgep
        xx = px[i]
        yy = py[i]
        step = pstep[i] * f1
        x1 = xx - step
        x2 = xx + step
        y1 = yy - step
        y2 = yy + step
        for j in range(i + 1, newnp):
            if px[j] < x1 or px[j] > x2:
                continue
            if py[j] < y1 or py[j] > y2:
                continue
            lcs = sqrt((px[j] - xx) ** 2 + (py[j] - yy) ** 2)
            if lcs < step:
                eop[j] = 0
    p = np
    for i in range(np, newnp):
        if eop[i] == 0:
            continue
        p = p + 1
        if (i + 1) == p:
            continue
        bgeop[p - 1] = bgeop[i]
        pstep[p - 1] = pstep[i]
        eop[p - 1] = eop[i]
        px[p - 1] = px[i]
        py[p - 1] = py[i]
    newnp = p
    for i in range(np, newnp):
        k = eop[i]
        if k > ne:
            k = ne
        j = search_1st(i + 1, k)
        if j == 0:
            print("error:search_ist=0/i=", i)
            j = input()
            break
        search_all(i + 1, j)
        if ndel > 200:
            print("ndel=", ndel, "/i=", i)
            k = input()
        check_up(i + 1)
        clear_up(i + 1)
        if (i + 1) % 1000 == 0:
            print("i=", i + 1, ne)
    np = newnp
    print("smooth over,  np=", np, ',  ne=', ne)


def optimize():  # 网格生成了之后要进行一下平滑，用质心代替原来的点
    global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # np点的个数，ne三角形单元的个数， nsearch寻找到第几个单元，px, py代表x坐标，y坐标，ipx, ipy存放点的临时横纵坐标，临时变量，可能放圆的质心
    # nod是每个单元由哪几个点组成，noe每个单元三个相邻的单元是哪几个，# epoch是每个单元的属性，npoch是每个点的属性
    global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx, gy为临时变量
    global ndel, edel, neibn
    # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    global eos, side, nb, nps
    # neibn相邻单元的信息
    global newnp, ecrit, eop, bgeop, pstep
    # newnp代表新生成的节点数
    # ecrit存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    # eop用来存放这个点的对应的单元的信息
    # bgeop用来存放这个点在背景网格的哪一个单元里面
    # pstep用来存放每一点的步长
    global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # bgnp背景网格的点数，bgne背景网格的单元数，bgnod背景网格由哪三个点组成，bgnoe有哪三个相邻单元
    # bgepoch背景网格的属性，bgcx, bgcy, bgcr背景网格对应的外接圆的圆心和半径
    global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    newx = npp.zeros(pmax, float)
    newy = npp.zeros(pmax, float)
    i = 0
    times = 0
    newn = npp.zeros(pmax, float)
    p1 = 0
    p2 = 0
    p3 = 0
    print("optimizing start!")
    for times in range(0, 100):
        for i in range(0, np):
            newx[i] = 0
            newy[i] = 0
            newn[i] = 0
        for i in range(0, ne):
            p1 = nod[0, i]
            p2 = nod[1, i]
            p3 = nod[2, i]
            x = px[p1 - 1] + px[p2 - 1] + px[p3 - 1]
            y = py[p1 - 1] + py[p2 - 1] + py[p3 - 1]
            newn[p1 - 1] = newn[p1 - 1] + 3
            newx[p1 - 1] = newx[p1 - 1] + x
            newy[p1 - 1] = newy[p1 - 1] + y
            newn[p2 - 1] = newn[p2 - 1] + 3
            newx[p2 - 1] = newx[p2 - 1] + x
            newy[p2 - 1] = newy[p2 - 1] + y
            newn[p3 - 1] = newn[p3 - 1] + 3
            newx[p3 - 1] = newx[p3 - 1] + x
            newy[p3 - 1] = newy[p3 - 1] + y
        for i in range(nps, np):
            px[i] = newx[i] / newn[i]
            py[i] = newy[i] / newn[i]


main()
