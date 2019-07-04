# encoding=utf8
####
from rpw import db
from pyrevit import revit, DB, HOST_APP, UI,_HostApplication
from Helper import LG_EUN,LG_CHS,CovertToMM

doc = __revit__.ActiveUIDocument.Document
hostapp = _HostApplication(__revit__)
if hostapp.app.Language.ToString()=="English_USA":
	ParameterName=LG_EUN()
elif hostapp.app.Language.ToString()=="Chinese_Simplified":
	ParameterName = LG_CHS()




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

    
class BAT_Beam():
    def __init__(self,Beam):
        self.Beam=Beam
        self.WrapedBeam=db.Element(Beam)
    @property
    def StartPoint(self):
        return self.Beam.Location.Curve.GetEndPoint(0)
    @property
    def EndPoint(self):
        return self.Beam.Location.Curve.GetEndPoint(1)
    def MoveToFloor(self,Floor):
        _Floor=BAT_Floor(Floor)
        TopSurfaces=_Floor.GetTopPlane()

        Proj1=TopSurfaces[0].Project(self.StartPoint)
        Proj2= TopSurfaces[0].Project(self.EndPoint)
        if Proj1!=None and Proj2!=None:
            Distance1 = Proj1.Distance
            Distance2 = Proj2.Distance
            with db.Transaction('Move Beam To Floor'):
                SLO = self.WrapedBeam.parameters[ParameterName.BEAM_Start_Level_Offset].value
                ELO = self.WrapedBeam.parameters[ParameterName.BEAM_End_Level_Offset].value
                self.WrapedBeam.parameters[ParameterName.BEAM_Start_Level_Offset] = Distance1 + SLO
                self.WrapedBeam.parameters[ParameterName.BEAM_End_Level_Offset] = Distance2 + ELO
                print("梁被排布在板底")
        else:
            print("梁不在板内，请重新放置梁")



class BAT_Floor():
    def __init__(self,Floor):
        self.Floor=Floor
        self.WrapedBeam=db.Element(Floor)
    def GetTopPlane(self):
        TopReference=DB.HostObjectUtils.GetTopFaces(self.Floor)
        TopSurface = [self.Floor.GetGeometryObjectFromReference(i) for i in TopReference]
        return TopSurface












