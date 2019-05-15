import random

class Array2D:
    """
        说明：
            1.构造方法需要两个参数，即二维数组的宽和高
            2.成员变量w和h是二维数组的宽和高
            3.使用：‘对象[x][y]’可以直接取到相应的值
            4.数组的默认值都是1(不可以走) 0 (可以走)
    """
    def __init__(self,w,h):
        self.w=w
        self.h=h
        self.data=[]
        self.data=[[4 for y in range(h)] for x in range(w)]


    def showArray2D(self):
        for y in range(self.h):
            for x in range(self.w):
                print(self.data[x][y],end=' ')
            print("")

    def __getitem__(self, item):
        return self.data[item]


class Point:
    """
    表示一个点
    """
    def __init__(self,x,y):
        self.x=x;self.y=y

    def __eq__(self, other):
        if self.x==other.x and self.y==other.y:
            return True
        return False
    def __str__(self):
        return "x:"+str(self.x)+",y:"+str(self.y)


class AStar:
    """
    AStar算法的Python3.x实现
    """

    class Node:  # 描述AStar算法中的节点数据
        def __init__(self, point, endPoint, g=0):
            self.point = point  # 自己的坐标
            self.father = None  # 父节点
            self.g = g  # g值，g值在用到的时候会重新算
            self.h = (abs(endPoint.x - point.x) + abs(endPoint.y - point.y)) * 10  # 计算h值
            # self.val = value

    def __init__(self, map2d, startPoint, endPoint, nopassTag=1):
        """
        构造AStar算法的启动条件
        :param map2d: Array2D类型的寻路数组
        :param startPoint: Point或二元组类型的寻路起点
        :param endPoint: Point或二元组类型的寻路终点
        :param passTag: int类型的可行走标记（若地图数据!=passTag即为障碍）
        :nopassTag: 1 cannot pass anyway
        """
        # 开启表
        self.openList = []
        # 关闭表
        self.closeList = []
        # 寻路地图
        self.map2d = map2d
        # 起点终点
        if isinstance(startPoint, Point) and isinstance(endPoint, Point):
            self.startPoint = startPoint
            self.endPoint = endPoint
        else:
            self.startPoint = Point(*startPoint)
            self.endPoint = Point(*endPoint)

        # 可行走标记
        self.nopassTag = nopassTag

    def getMinNode(self):
        """
        获得openlist中F值最小的节点
        :return: Node
        """
        currentNode = self.openList[0]
        for node in self.openList:
            if node.g + node.h < currentNode.g + currentNode.h:
                currentNode = node
        return currentNode

    def pointInCloseList(self, point):
        for node in self.closeList:
            if node.point == point:
                return True
        return False

    def pointInOpenList(self, point):
        for node in self.openList:
            if node.point == point:
                return node
        return None

    def endPointInCloseList(self):
        for node in self.openList:
            if node.point == self.endPoint:
                return node
        return None

    def searchNear(self, minF, offsetX, offsetY):
        """
        搜索节点周围的点
        :param minF:F值最小的节点
        :param offsetX:坐标偏移量
        :param offsetY:
        :return:
        """
        # 越界检测
        if minF.point.x + offsetX < 0 or minF.point.x + offsetX > self.map2d.w - 1 or minF.point.y + offsetY < 0 or minF.point.y + offsetY > self.map2d.h - 1:
            return
        # 如果是障碍，就忽略
        if self.map2d[minF.point.x + offsetX][minF.point.y + offsetY] == self.nopassTag:
            return
        # 如果在关闭表中，就忽略
        currentPoint = Point(minF.point.x + offsetX, minF.point.y + offsetY)
        if self.pointInCloseList(currentPoint):
            return
        # 设置单位花费
        if offsetX == 0 or offsetY == 0:
            step = 10
        else:
            step = 14
        # 如果不再openList中，就把它加入openlist
        currentNode = self.pointInOpenList(currentPoint)
        if not currentNode:
            currentNode = AStar.Node(currentPoint, self.endPoint, g=minF.g + step)
            currentNode.father = minF
            self.openList.append(currentNode)
            return
        # 如果在openList中，判断minF到当前点的G是否更小
        if minF.g + step < currentNode.g:  # 如果更小，就重新计算g值，并且改变father
            currentNode.g = minF.g + step
            currentNode.father = minF

    def start(self):
        """
        开始寻路
        :return: None或Point列表（路径）
        """
        # 判断寻路终点是否是障碍
        if self.map2d[self.endPoint.x][self.endPoint.y] == self.nopassTag:
            return None

        # 1.将起点放入开启列表
        startNode = AStar.Node(self.startPoint, self.endPoint)
        self.openList.append(startNode)
        # 2.主循环逻辑
        while True:
            # 找到F值最小的点
            minF = self.getMinNode()
            # 把这个点加入closeList中，并且在openList中删除它
            self.closeList.append(minF)
            self.openList.remove(minF)
            # 判断这个节点的上下左右节点
            # 'B'----bricks *** tricky
            # '#'----ladders *** go up and down  2
            # '-'----wires *** go left and right and down  3
            # ''
            if self.map2d[minF.point.x][minF.point.y] == 2:
                # up and down
                self.searchNear(minF, 0, -1) # up
                self.searchNear(minF, 0, 1) # down
            elif self.map2d[minF.point.x][minF.point.y] == 3:
                self.searchNear(minF, 0, 1)
                self.searchNear(minF, -1, 0)
                self.searchNear(minF, 1, 0)
            elif self.map2d[minF.point.x][minF.point.y] == 4:
                self.searchNear(minF, 0, 1)
            else:
                self.searchNear(minF, 0, -1)
                self.searchNear(minF, 0, 1)
                self.searchNear(minF, -1, 0)
                self.searchNear(minF, 1, 0)
            # 判断是否终止
            point = self.endPointInCloseList()
            if point:  # 如果终点在关闭表中，就返回结果
                # print("关闭表中")
                cPoint = point
                pathList = []
                while True:
                    if cPoint.father:
                        pathList.append(cPoint.point)
                        cPoint = cPoint.father
                    else:
                        # print(pathList)
                        # print(list(reversed(pathList)))
                        # print(pathList.reverse())
                        return list(reversed(pathList))
            if len(self.openList) == 0:
                return None


def Astar(map):

    # file = open('./Processed/Level 7.txt','r')

    # file = open('level.txt')
    #
    # map=list()
    # for line in file:
    #     map.append(line)

    gold_locations = list()
    # for i, words in enumerate(map):
    #     if 'G' in words:
    #
    #         print(words.index('G'), i)
    # print(len(map))
    map2d=Array2D(len(map[0]), len(map))

    # 'B'----bricks *** tricky
    # '#'----ladders *** go up and down  2
    # '-'----wires *** go left and right and down  3  but
    # 'none' ==== 4, only go down
    # ''

    # row loop
    for i, words in enumerate(map): # y pixel
        for j, word in enumerate(words):
            if word == 'G':
                gold_locations.append(Point(j, i))
                # print(j, i)
            elif word == '#':
                # map2d[j][i - 1] = 0
                map2d[j][i] = 2
                # map2d[j][i]

            # elif word == 'b' or word == 'B':
            #     map2d[j][i - 1] = 0
            elif word == '-':
                map2d[j][i] = 3
            elif word == 'M':
                start = Point(j, i)
                # map2d[j][i] = '*'
                # print('my loca',j, i)

    # print(map)  column
    for i in range(len(map[0])):
        j = 0
        while j < len(map):
            # print(j,'in loop')
            if map[j][i] == '#':
                map2d[i][j - 1] = 0
                # print(i,' revise  ', j)
                while j < len(map) and map[j][i] == '#':
                    j += 1
                    # print(j, 'in while')
            j += 1
                    # p2d[j][i]
    # map2d.showArray2D()
    for i in range(len(map[0])):
        j = 0
        while j < len(map):
            # print(j)
            if map[j][i] == 'b' or map[j][i] == 'B':
                map2d[i][j - 1] = 0
                while map[j][i] == 'B' or map[j][i] == 'b':
                    j += 1
                    if j == len(map):
                        break
            j += 1
            # print(j)
            # if map[j][i] == '-':
            #     j += 1
            #     while map2d[i][j] == 1:
            #         map2d[i][j] = 4
            #         j += 1


    finpath=list()
    # map2d[25][5]='*'
    # map2d.showArray2D()

    totalpoint = 0
    totalloc = 0
    for i in range(len(map)):
        for j in range(len(map[0])):
            if random.random() > 0.1:
                continue
            totalloc += 1
            aStar=AStar(map2d, start, Point(j, i))
            pathList=aStar.start()
            if pathList == None:
                continue
            else:
                totalpoint += 1

    fin_res = totalpoint / totalloc
    '''print('Totalpoint is', totalpoint, 'out of', totalloc, ', final:', fin_res)
                print("-------------------------------")'''



    for loc in gold_locations:
        aStar=AStar(map2d, start, loc)
        pathList=aStar.start()
        #遍历路径点,在map2d上以'8'显示
        if pathList == None:
            #print("Cannot find a path")
            break
        finpath.append(pathList)
        # for point in pathList:
        #     map2d[point.x][point.y]='*'
        start = loc

    for path in finpath:
        for point in path:
            map2d[point.x][point.y]='*'
    #显示地图当前样子
    '''map2d.showArray2D()
            
                print("-------------------------------")'''



    # from PIL import Image
    # from PIL import ImageDraw
    # im = Image.open('./Original/Level 7.png')
    # each = 10
    # im = im.resize(((len(map[0])) * each, (len(map) + 3)* each ),Image.ANTIALIAS)
    # width, height = im.size
    # print(width, height)
    # # each = (height + width) / (len(map)+len(map[0]))
    # print(each)
    #
    # draw=ImageDraw.Draw(im)
    # # draw.point((1,2), fill = None)
    # for path in finpath:
    #     for point in path:
    #         draw.ellipse((point.x*each, point.y*each, (point.x+1)*each, (point.y+1)*each), fill=None, outline=None)
    #         # point.x*each][point.y]='*'
    # im.show()

    return fin_res



# how to use the api exampel
# map is the list of string
# astar.Astar(map)
