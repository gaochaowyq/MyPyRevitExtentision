# encoding=utf8
####
from rpw import db
from Helper import *




class _Room(db.Room):
    @property
    def Area(self):
        Area=self.parameters['Area'].value
        return CovertToM2(Area)
    @property
    def Height(self):
        heigth=self.parameters['Unbounded Height'].value
        return CovertToMM(heigth)
    @property
    def Volume(self):
        return self.parameters['Volume'].value

    @property
    def Index(self):
        return self.parameters['Number'].value

    @property
    def name(self):
        name=self.parameters['Name'].value
        return name.encode('GB2312').decode('GB2312','strict')

    def __str__(self):
        return "{roomname}".format(roomname=self.name)

class Room(_Room):
    def __init__(self,room,Rule=None):
        super(self.__class__,self).__init__(room)

    @property
    def AreaRatio(self):
        return  self.parameters['AreaRatio'].value

    @property
    def Area_All(self):
        Area = self.parameters['Area'].value
        return CovertToM2(Area)


    @property
    def Area_ByRatio(self):
        Area=self.parameters['Area'].value
        return CovertToM2(Area)*self.AreaRatio
    @property
    def Area_ByNoRatio(self):
        Area=self.parameters['Area'].value
        return CovertToM2(Area)*(1-self.AreaRatio)

    











