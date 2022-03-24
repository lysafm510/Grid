import numpy as npp
from math import sqrt

# *******************************************************************
# 1. 初始化背景网格
#
# 这个文件完全不需要动，会直接对初始的背景网格delaunay三角化
# 只需要修改以下输入和输出文件！
#
# 输入：<自定义>的背景网格的各点坐标
background_grid_file = "bggridt.dat"

# 输出：
background_nod_file = "bg_nod.dat"
background_noe_file = "bg_noe.dat"


# *******************************************************************

def not_empty(s):
    return s and s.strip()


def delaunay():
    """
    背景网格delaunay三角化
    :return:
    """
    global px, py, pmax, emax, nsearch, ne, np, edel, ndel, delmax, fm2, neibn, ecrit, eos, bmax, nb, nps
    global centx, centy, length
    emax = 200000
    pmax = 100000
    delmax = 1000
    bmax = 2000
    fm2 = 10 ** -8
    px = npp.zeros(pmax, float)  # x坐标，y坐标
    py = npp.zeros(pmax, float)
    xmax = 0.0
    xmin = 0.0
    ymax = 0.0
    ymin = 0.0
    nsearch = 0  # 寻找到第几个单元
    np = 0  # 点的个数
    ne = 0  # 三角形单元的个数
    ndel = 0
    edel = npp.zeros(delmax, int)  # 引入一个新的点之后，看有多少个单元包含这个点，ndel是外接圆包含这个点的单元数，edel是被删掉的单元
    neibn = npp.zeros(delmax, int)  # 相邻单元的信息
    ecrit = npp.zeros(emax, int)  # 存放判断每一个单元是不是正常的数组，正常的就放一个正数，不正常的就放一个负数
    eos = npp.zeros((2, bmax), int)
    nb = 0  # nb是边界数目
    nps = 0  # nps可能是边界点数

    bgg = open(background_grid_file, "r")
    bggcount = 0
    for line in bgg.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        px[bggcount] = current_line[0]
        py[bggcount] = current_line[1]

        if bggcount == 0:
            xmax = px[bggcount]
            xmin = px[bggcount]
            ymax = py[bggcount]
            ymin = py[bggcount]
        else:
            if xmax < px[bggcount]:
                xmax = px[bggcount]
            if xmin > px[bggcount]:
                xmin = px[bggcount]
            if ymax < py[bggcount]:
                ymax = py[bggcount]
            if ymin > py[bggcount]:
                ymin = py[bggcount]
        bggcount = bggcount + 1
    np = bggcount
    nps = np
    bgg.close()

    centx = (xmax + xmin) / 2
    centy = (ymax + ymin) / 2
    len_x = xmax - xmin
    len_y = ymax - ymin
    length = max(len_x, len_y)
    length = 1.2 * length
    convex_hull()  # 先引入四个点把整个边界都给框起来，用凸多边形把边界包住
    ne = 2
    lastnp = -1
    nsearch = 0
    for i in range(lastnp + 1, np):  # 把背景网格的点连成网络
        j = search_1st(i + 1, ne)  # 搜寻第一个三角形单元，遵循某个路径
        search_all(i + 1, j)  # 以第一个找的三角形单元为基础，再把其他所有的都搜出来
        check_up(i + 1)  # 最后是个多边形包住这个点，多边形的每一条边和这个点相连成新的单元
        clear_up(i + 1)  # 在数组里面，把所有刚才删除的单元给清掉，再对新的单元重新排序
    delete_outside()  # 把边界外面引入的四个点全部删掉，删掉以后剩下的就是我们真正需要的
    save_data()


def search_1st(p, start):  # 按照某个路径寻找第一个点
    global px, py, nsearch, epoch, cx, cy, cr, xce, yce, edel, ndel
    epoch = npp.zeros(emax, int)  # epoch是每个单元的属性，npoch是每个点的属性
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
    nsearch = nsearch + 1  # nsearch: 寻找到第几个单元
    ending = 0
    current = start
    for i in range(0, ne):
        if epoch[current - 1] == nsearch:
            break
        gcx = cx[current - 1]
        gcy = cy[current - 1]
        gcr = cr[current - 1]
        dcp = sqrt((x - gcx) ** 2 + (y - gcy) ** 2)
        if dcp < gcr:
            ending = current
            break
        epoch[current - 1] = nsearch
        dep = -1
        next = 0
        for j in range(0, 3):
            k = noe[j, current - 1]
            if k < 1 or k == last or epoch[k - 1] == nsearch:
                continue
            gcx = cx[k - 1]
            gcy = cy[k - 1]
            gcr = cr[k - 1]
            dcp = sqrt((x - gcx) ** 2 + (y - gcy) ** 2)
            if dcp < gcr:
                ending = current
                break
            centroid(k)
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


def search_all(p, ending):  # 以刚才那个为基准找所有的
    global ndel, edel, px, py, cx, cy, cr, fm2
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


def convex_hull():  # 先引入四个点把整个边界都给框起来，用凸多边形把边界包住
    global gx, gy, noe, nod, cx, cy, cr, gx, gy, ipx, ipy
    ipx = npp.zeros(4, float)  # 坐标
    ipy = npp.zeros(4, float)
    nod = npp.empty((3, emax), int)
    noe = npp.empty((3, emax), int)
    gx = npp.zeros(3, float)  # 一个三角形三个点的坐标
    gy = npp.zeros(3, float)
    cx = npp.zeros(emax, float)
    cy = npp.zeros(emax, float)
    cr = npp.zeros(emax, float)

    ipx[0] = centx - 0.65 * length  # 左下角为0，逆时针1，2，3
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
    noe[0, 0] = 2  # 左下角为-1，顺时针-2，-3，-4; 左下角三角形为1，右上角三角形为2
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


def circumcircle():
    """
    计算外接圆的圆心和半径的
    """
    global gcx, gcy, gcr
    arr = npp.zeros([2, 2], float)
    ver = npp.zeros(2, float)
    verx = npp.zeros(2, float)

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


def axeqb(arr1, verb1, num, verx1):
    """
    解方程用的
    """
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


def centroid(e):
    """
    计算e这个单元的质心
    """
    global ipx, ipy, px, py, nod
    global xce, yce
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


def in_or_out(p, e):
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


def area(p1, p2, p3):  # 计算三角形的面积，判断点在三角形的内部还是外部
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


def distance(p1, p2, p3, n):  # 计算p1和p2的距离，p3是三维时候的变量，实际上p3没用到，比如判断一个点是否在外接圆里面，就要求它和圆心的距离
    global ipx, ipy, px, py
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


def check_up(p):  # 找到所有单元之后，判断哪些单元要删除
    global epoch, edel, nsearch, ndel
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


def clear_up(p):  # 把该删除的单元都删除掉，把编号都更新，要么就是用新的单元来填充，要么就是把后面的单元号往前推
    global edel, noe, nod, neibn, ecrit, ne, gx, gy, cx, cy, cr
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


# *****************************************************************************************
def delete_outside():  # 在边界点引进来之后，把外面那四个点及其组成的单元全部删掉
    '''
    nod 文件就直接删带负号的，统计一下一共删了多少个文件
    :return:
    '''
    global nod, noe, ne
    for m in range(0, ne):
        for i in range(0, ne):
            flag = False
            for j in range(0, 3):
                if (nod[j, i] < 0):
                    flag = True
                    nod = npp.delete(nod, i, axis=1)
                    noe = npp.delete(noe, i, axis=1)
                    ne = ne - 1
                    for k in range(0, ne):
                        for e in range(0, 3):
                            if (noe[e, k] == (i + 1)):
                                noe[e, k] = 0
                            if (noe[e, k] > (i + 1)):
                                noe[e, k] = noe[e, k] - 1
                    break
            if flag == True:
                break


# ******************************************************************************

def save_data():
    """
    保存数据
    """
    i = 0
    no1 = open(background_nod_file, "w")
    no2 = open(background_noe_file, "w")
    for i in range(0, ne):
        no1.write(str(nod[0, i]) + " ")
        no1.write(str(nod[1, i]) + " ")
        no1.write(str(nod[2, i]) + "\n")
        no2.write(str(noe[0, i]) + " ")
        no2.write(str(noe[1, i]) + " ")
        no2.write(str(noe[2, i]) + "\n")
    no1.close()
    no2.close()


delaunay()
