import json



class Input(object):
    def __init__(self,Filename):
        self.Filename=Filename
        with open(self.Filename, 'r') as f:
            c = f.read()
            c = json.loads(c)
        self.Input=c

    def GetModlePart(self):
        return self.Input['storey_20655995-0095-4e0f-846d-59afad2fdc81']['json']
    def GetWalls(self):
        return self.GetModlePart()['walls']
    def GetPoints(self):
        return self.GetModlePart()['corners']
    def AdDict(self):
        class Mydic:
            def __init__(self,Input):
                self.__dict__=Input
        c=Mydic(self.Input)
        return c

class Point(Input):
    def __init__(self,id,Filename):
        self.id=id
        super(Point,self).__init__(Filename)

    def getpoint(self):
        points=self.GetPoints()[self.id]['pos']
        point=points.split(" ")
        point1=map(float,point)
        ccc=[x for x in point1]
        return ccc

class Wall(object):
    def __init__(self,wall,Filename):
        self.wall=wall
        self.Filename=Filename
    def startpoint(self):
        id=self.wall['start']
        return Point(id,self.Filename).getpoint()
    def endpoint(self):
        id = self.wall['end']
        return Point(id,self.Filename).getpoint()
    def level(self):
        return 'Level1'
    def thickness(self):
        pass
    def hight(self):
        return float(self.wall['height'])
    def id(self):
        return self.wall

#mm=input()
#walls=[]
#for i in mm.GetWalls():
#    if i.startswith( 'wall' ):

#        ccc=Wall(mm.GetWalls()[i])
#        walls.append(ccc)
#print(walls)

#cc=Input('C:\Users\sxu10002\Desktop\Tem\storeyJson.json')

#c=cc.AdDict()
#print(c.__dict__)
class A:
    def __init__(self,c):
        self.c=c
    def draw(self):
        return self.what()

class B(A):
    def __new__(cls, *args, **kwargs):
        cls.c=4
        return cls
    def what(self):
        print(self.c)

class T(A):
    def what(self):
        print('This is not well')
C=B('dfe')
C.draw()