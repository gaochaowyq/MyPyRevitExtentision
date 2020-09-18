## -*- coding: utf-8 -*-
__doc__="通过房间属性中包含的室内做法，创建内墙。"
import rpw
import pyrevit
from rpw import db,doc
from pyrevit import revit,DB,UI,forms,HOST_APP,_HostApplication
from System.Collections.Generic import List
from Autodesk.Revit.DB.Architecture import Room
from Helper import *
#
hostapp = _HostApplication()
if hostapp.app.Language.ToString()=="English_USA":
    ParameterName=LG_EUN()
elif hostapp.app.Language.ToString()=="Chinese_Simplified":
    ParameterName = LG_CHS()


def OffsetLines(Lines,Distance):
    CurveLoop = DB.CurveLoop.Create(Lines)
    NewCurve = DB.CurveLoop.CreateViaOffset(CurveLoop, CovertToFeet(Distance), DB.XYZ(0, 0, 1))
    result=[]
    for i in NewCurve.GetCurveLoopIterator():
        result.append(i)
    return result
def EdgeArrayArrayToList(EdgeArray):
    _List=List[DB.Curve]()
    for i in EdgeArray:
        for c in i:
            _List.Add(c.AsCurve())
    return _List

#Select Room
Rooms= revit.get_selection()

selected_switch =forms.CommandSwitchWindow.show(["创建建筑楼板","创建内墙","创建吊顶"],
                                   message='选择要创建的构件')

class MassSelectionFilter(UI.Selection.ISelectionFilter):
    # standard API override function
    def AllowElement(self, element):
        if element.Category.Name == "Rooms" or element.Category.Name == "房间":
            return True
        else:
            return False

    # standard API override function
    def AllowReference(self, refer, point):
        return False
try:
    msfilter = MassSelectionFilter()
    refs = HOST_APP.uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, msfilter)
    return_values =[HOST_APP.doc.GetElement(ref)for ref in refs]
    Rooms.set_to(return_values)
    revit.uidoc.RefreshActiveView()
except Exception as e:
    print(e)
############################################################################

class BAT_Room:
    def __init__(self,Room):
        self.Room=Room
        self.WrapedRoom=db.Element(self.Room)
        self.RoomLevelId=self.Room.Level.Id
        self.RoomLevel = self.Room.Level
    @property
    def RoomName(self):
        p=DB.BuiltInParameter.ROOM_NAME
        Name=self.Room.get_Parameter(p).AsString()
        return Name
    @property
    def RoomHeight(self):
        p = DB.BuiltInParameter.ROOM_HEIGHT
        try:
            Heigth = self.Room.get_Parameter(p).AsDouble()
            print("{RoomName}房间高度为{Height}".format(RoomName=Room.RoomName, Height=Heigth))
            return Heigth
        except Exception as e:
            print("{Room}不能获取房间高度：{Problem}".format(Room=self.RoomName, Problem=e))
    @property
    def RoomBase(self):
        RoomBaseOffset = self.Room.get_Parameter(DB.BuiltInParameter.ROOM_LOWER_OFFSET).AsInteger()
        return RoomBaseOffset
    @property
    def WallFinishType(self):
        try:
            WallFinishName=self.WrapedRoom.parameters[ParameterName.Room_Wall_Finish].value
            param_id = DB.ElementId(DB.BuiltInParameter.SYMBOL_NAME_PARAM)
            parameter_filter = db.ParameterFilter(param_id, equals=WallFinishName)
            WallType = db.Collector(of_category='OST_Walls', parameter_filter=parameter_filter,
                                    is_type=True).get_first()


            WallType=WallType.unwrap()
            return WallType

        except Exception as e:
            print("{roomname} 没有设置墙体类型,使用默认墙体".format(roomname=self.RoomName))
            defaultWallTypeId =doc.GetDefaultElementTypeId(DB.ElementTypeGroup.WallType)
            WallType=doc.GetElement(defaultWallTypeId)
            return WallType

    @property
    def FloorFinishType(self):
        try:
            WallFinishName=self.Room.get_Parameter(DB.BuiltInParameter.ROOM_FINISH_FLOOR)
            param_id = DB.ElementId(DB.BuiltInParameter.SYMBOL_NAME_PARAM)
            parameter_filter = db.ParameterFilter(param_id, equals=WallFinishName.AsString())
            FloorType = db.Collector(of_category='OST_Floors', parameter_filter=parameter_filter,
                                    is_type=True).get_first(wrapped=False)
            return FloorType

        except Exception as e:
            print("{Room}不能获取建筑楼面类型：{Problem}".format(Room=self.RoomName, Problem=e))

    @property
    def CeilingFinishType(self):
        try:
            WallFinishName=self.Room.get_Parameter(DB.BuiltInParameter.ROOM_FINISH_CEILING)
            param_id = DB.ElementId(DB.BuiltInParameter.SYMBOL_NAME_PARAM)
            parameter_filter = db.ParameterFilter(param_id, equals=WallFinishName.AsString())
            CeilingType = db.Collector(of_category='OST_Ceilings', parameter_filter=parameter_filter,
                                    is_type=True).get_first(wrapped=False)

            return CeilingType
        except Exception as e:
            print("{Room}不能获取吊顶类型：{Problem}".format(Room=self.RoomName,Problem=e))

    @property
    def WallFinishTypeId(self):
        try:
            return  self.WallFinishType.Id
        except Exception as e:
            print("{Room}不能获取墙面类型ID：{Problem}".format(Room=self.RoomName, Problem=e))
    def RoomBoundary(self):
        room_boundary_options = DB.SpatialElementBoundaryOptions()
        room_boundary = self.Room.GetBoundarySegments(room_boundary_options)
        Index=[]

        Length=[]
        for i in room_boundary:
            CurveLoop = DB.CurveLoop.Create([j.GetCurve() for j in i])
            Length.append(CurveLoop.GetExactLength())
        newLength=sorted(Length)
        _room_boundary=[room_boundary[Length.index(i)] for i in newLength]

        return _room_boundary

    def RoomFaceWall(self):
        room_SpatialElementGeometry=DB.SpatialElementGeometryCalculator(doc).CalculateSpatialElementGeometry(self.Room)
        RoomFace=room_SpatialElementGeometry.GetGeometry().Faces
        edgeLoop = []
        edgeNormal = []
        _WallId=[]

        for i in RoomFace:
            SpatialElementGeometryResults = room_SpatialElementGeometry.GetBoundaryFaceInfo(i)

            if len(SpatialElementGeometryResults)>0:
                if SpatialElementGeometryResults[0].SubfaceType==DB.SubfaceType.Side:
                    #surface=SpatialElementGeometryResults[0].GetBoundingElementFace()
                    WallId=SpatialElementGeometryResults[0].SpatialBoundaryElement.HostElementId
                    _edgeLoop=i.GetEdgesAsCurveLoops()
                    _FaceNormal=i.FaceNormal
                    edgeLoop.append(_edgeLoop)
                    edgeNormal.append(_FaceNormal)
                    _WallId.append(WallId)
        return [edgeLoop,edgeNormal,_WallId]



    def ParaForMakeWall(self):
        Wall_Surface = List[DB.Curve]()
        Aj_WallId = List[DB.ElementId]()
        for boundary_segment, Room_Aj_WallId in zip(self.Offseted_RoomBoundary()[0], self.Offseted_RoomBoundary()[1]):
            try:
                Aj_WallId.Add(Room_Aj_WallId)
                #Wall_curves.Add(boundary_segment)  # 2015, dep 2016
            except AttributeError:
                #Wall_curves.Add(boundary_segment)  # 2017
                pass
        return [Wall_Surface,Aj_WallId]

    def MakeWall(self):
        @rpw.db.Transaction.ensure('Make Wall')
        def make_wall():
            walls=[]
            wallfaces=self.RoomFaceWall()
            # l:EdgeLoop->[List<CurveLoop>]  n:edgeNormal w:_WallId
            for l,n,w in zip(wallfaces[0],wallfaces[1],wallfaces[2]):
                transform=DB.Transform.CreateTranslation(self.WallFinishType.Width/2*(-n))
                newLines=List[DB.Curve]()
                for i in l:
                    newCurveLoop=DB.CurveLoop.CreateViaTransform(i,transform)
                    CurveInterator=newCurveLoop.GetCurveLoopIterator()
                    for c in CurveInterator:
                        newLines.Add(c)
                OldWall = doc.GetElement(w)
                #TODO There are some proble
                try:
                    NewWall = DB.Wall.Create(doc, newLines, self.WallFinishTypeId, self.RoomLevelId, None)
                    NewWall.get_Parameter(DB.BuiltInParameter.WALL_ATTR_ROOM_BOUNDING).Set(0)
                except:
                    NewWall=None
                try:
                    DB.JoinGeometryUtils.JoinGeometry(doc, NewWall, OldWall)
                    walls.append(NewWall)
                except:
                    if NewWall!=None:
                        doc.Delete(NewWall.Id)
                    walls.append(None)
            return walls
        wall=make_wall()
        @rpw.db.Transaction.ensure('Modify Wall')
        def modify_wall():
            for i,j in zip(wall,self.RoomFaceWall()[1]):
                if i!=None:
                    if i.Orientation.DotProduct(j)>0 :
                        i.Flip()
                        print("墙体方向被翻转")
                    else:
                        pass
                else:
                    pass
        modify_wall()


    def MakeFloor(self):
        @rpw.db.Transaction.ensure('MakeFloor')
        def make_floor():
            Floor_CurveArray = DB.CurveArray()
            for boundary_segment in self.RoomBoundary()[0]:
                Floor_CurveArray.Append(boundary_segment.GetCurve())
                #Floor_CurveArray.Append(Wall_curves)
            FloorType =self.FloorFinishType
            level =self.RoomLevel

            _doc = pyrevit._HostApplication(__revit__).doc.Create
            try:
                self.NewFloor=_doc.NewFloor(Floor_CurveArray,FloorType,level,None)
                self.NewFloor.get_Parameter(DB.BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM).Set(self.RoomBase)
                print("{RoomName}建筑楼板被创建".format(RoomName=self.RoomName))
            except Exception as e:
                self.NewFloor=None
                print("{RoomName}建筑楼板未能被创建:{Problem}".format(RoomName=Room.RoomName, Problem=e.__traceback__))
        @rpw.db.Transaction.ensure('MakeFloor')
        def make_floor_Open(Floor):
            _doc = HOST_APP.doc.Create
            boundary=[]
            BoundaryArea=[i for i in self.RoomBoundary()]
            for i in range(0,len(self.RoomBoundary())):
                if i!=0:
                    boundary.append(self.RoomBoundary()[i])
            for boundary_segment in boundary:
                Open_CurveArray = DB.CurveArray()
                for i in boundary_segment:
                    Open_CurveArray.Append(i.GetCurve())
                try:
                    _doc.NewOpening(Floor, Open_CurveArray, True)
                    print("OpeningCreated")
                except Exception as e:
                    print(e)
        make_floor()
        if self.NewFloor!=None:
            make_floor_Open(self.NewFloor)


###############################################
    def MakeCeiling(self):
        @rpw.db.Transaction.ensure('MakeFloor')
        def make_ceiling():

            Wall_curves =List[DB.Curve]()
            for boundary_segment in self.Offseted_RoomBoundary():
                try:
                    Wall_curves.Add(boundary_segment)       # 2015, dep 2016
                except AttributeError:
                    Wall_curves.Add(boundary_segment)  # 2017
            CeilingType =self.CeilingFinishType
            level =self.RoomLevel
            Floor_CurveArray=DB.CurveArray()
            for i in Wall_curves:
                Floor_CurveArray.Append(i)
            _doc = pyrevit._HostApplication(__revit__).doc.Create

            _doc.NewFloor(Floor_CurveArray,CeilingType,level,None)
        try:
            make_ceiling()
            print("{RoomName} 吊顶被创建".format(RoomName=Room.RoomName))
        except Exception as e:
            print(e)
            print("{RoomName} 吊顶未被创建".format(RoomName=Room.RoomName))


for _Room in Rooms:
    Room=BAT_Room(_Room)
    if selected_switch=="创建内墙":
        Room.MakeWall()
    elif selected_switch=="创建建筑楼板":
        Room.MakeFloor()
    else:
        print("{}功能还没有开放,敬请期待".format(selected_switch))
    #Room.MakeCeiling()



