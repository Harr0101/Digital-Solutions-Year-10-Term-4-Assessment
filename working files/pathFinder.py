
OPPOSITEdIR = {"north":"south","east":"west","south":"north","west":"east"}

class Graph():
    def __init__(self,name):
        self.sides = {}
        self.name = name
        self.pathFindingCounter = 9999
        self.pathFrom = None
        self.pathFindingDirection = None

    def addSide(self,side,direction):
        self.sides[direction] = side
        side.sides[OPPOSITEdIR[direction]] = self


    def pathfind(self,target):
        self.pathFindingCounter = 0
        open_list = [self]

        while open_list:
            current = open_list.pop(0)
            for side in current.sides.items():
                dist = current.pathFindingCounter+1
                analysing = side[1]
                if analysing.count > dist:
                    analysing.count = dist
                    analysing.pathFrom = current
                    analysing.direction = side[0]
                    open_list.append(analysing)
                    if analysing.name == target:
                        cell = analysing

        path = []
        while cell != None:
            path.append(cell)
            cell = cell.pathFrom
        path.reverse()
        path.pop(0)

        return path

a = Graph("a")
b = Graph("b")
c = Graph("c")
d = Graph("d")
e = Graph("e")
f = Graph("f")

a.addSide(b,"east")
b.addSide(c,"east")
c.addSide(d,"south")
b.addSide(e,"north")
e.addSide(f,"west")

path = f.pathfind("a")

for i in path:
    print(i.direction)


