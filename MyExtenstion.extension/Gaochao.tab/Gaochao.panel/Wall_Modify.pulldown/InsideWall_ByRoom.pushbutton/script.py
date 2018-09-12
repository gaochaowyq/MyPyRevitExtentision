# -*- coding: utf-8 -*-
__doc__="分析设计中内墙与外墙的量"



import rpw
import pyrevit
from rpw import db,doc
from pyrevit import revit,DB,UI,forms,HOST_APP
#######################

#######################
from System.Collections.Generic import List
import json
#from pyrevit import this_script
from pyrevit.forms import CommandSwitchWindow
import subprocess as sp
#from pyrevit.coreutils.console import charts
from Autodesk.Revit.DB.Architecture import Room
from collections import namedtuple
from Helper import *
class BaseError(Exception):
    pass
class GetRevitServiceError(BaseError):
    pass
class OffsetError(BaseError):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return 'PolyLine Offset Have Problem With Distance {}'.format(self.msg)
class WallTypeError(BaseError):
    def __init__(self,RoomName):
        self.msg = RoomName
    def __str__(self):
        return '{}没有设置内墙类型'.format(self.msg)
class RoomOffsetError(BaseError):
    def __init__(self,RoomName):
        self.msg = RoomName
    def __str__(self):
        return '{} Can Not Be Offset'.format(self.msg)
class MakeWallError(BaseError):
    def __init__(self,RoomName):
        self.msg = RoomName
    def __str__(self):
        return '{} Can Not Create Wall'.format(self.msg)
class GetElementError(BaseError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "{} Can Not Get".format(self.msg)



def OffsetLines(Lines,Distance):
    CurveLoop = DB.CurveLoop.Create(Lines)
    NewCurve = DB.CurveLoop.CreateViaOffset(CurveLoop, CovertToFeet(Distance), DB.XYZ(0, 0, 1))
    result=[]
    for i in NewCurve.GetCurveLoopIterator():
        result.append(i)
    return result

#Select Room
Rooms= revit.get_selection()

selected_switch =forms.CommandSwitchWindow.show(["创建建筑楼板","创建内墙","创建吊顶"],
                                   message='选择要创建的构件')

class MassSelectionFilter(UI.Selection.ISelectionFilter):
    # standard API override function
    def AllowElement(self, element):
        if element.Category.Name == "Rooms":
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
            WallFinishName=self.WrapedRoom.parameters['Wall Finish'].value
            param_id = DB.ElementId(DB.BuiltInParameter.SYMBOL_NAME_PARAM)
            parameter_filter = db.ParameterFilter(param_id, equals=WallFinishName)
            WallType = db.Collector(of_category='OST_Walls', parameter_filter=parameter_filter,
                                    is_type=True).get_first()

            return WallType

        except WallTypeError as e:
            print("{Room}不能获取建筑墙面类型：{Problem}".format(Room=self.RoomName, Problem=e))
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
        print(Length)


        return room_boundary

    def Offseted_RoomBoundary(self):
        try:
            room_boundary =self.RoomBoundary()[0]
            Room_Aj_WallId=[i.ElementId for i in room_boundary]
            lines = [i.GetCurve() for i in room_boundary]
            Wall_Width = CovertToMM(self.WallFinishType.Width)

            polyline = OffsetLines(lines, -(Wall_Width / 2))
            return [polyline,Room_Aj_WallId]
        except Exception as e:
            print("{RoomName}内墙轮廓线生成失败，请查看单位或轮廓线的连续性:{Problem}".format(RoomName=Room.RoomName,Problem=e))
    def ParaForMakeWall(self):
        Wall_curves = List[DB.Curve]()
        Aj_WallId = List[DB.ElementId]()
        for boundary_segment, Room_Aj_WallId in zip(self.Offseted_RoomBoundary()[0], self.Offseted_RoomBoundary()[1]):
            try:
                Aj_WallId.Add(Room_Aj_WallId)
                Wall_curves.Add(boundary_segment)  # 2015, dep 2016
            except AttributeError:
                Wall_curves.Add(boundary_segment)  # 2017
        return [Wall_curves,Aj_WallId]

    def MakeWall(self):
        @rpw.db.Transaction.ensure('Make Wall')
        def make_wall():
            _ParaForMakeWall=self.ParaForMakeWall()
            level =self.RoomLevelId
            for i,j in zip(_ParaForMakeWall[0],_ParaForMakeWall[1]):
                try:
                    OldWall = doc.GetElement(j)
                    _OldWall = OldWall.GetTypeId()
                    _OldWall = doc.GetElement(_OldWall)

                    FamilyName=_OldWall.get_Parameter(DB.BuiltInParameter.ALL_MODEL_FAMILY_NAME).AsString()
                    if FamilyName=="Curtain Wall" or FamilyName=="玻璃幕墙":
                        print("{RoomName}玻璃幕墙无内墙".format(RoomName=Room.RoomName))
                    elif FamilyName==None:
                        pass
                    elif FamilyName=="Basic Wall" or FamilyName=="基础墙":
                        WallID=self.WallFinishTypeId
                        NewWall=DB.Wall.Create(doc,i,WallID,level,self.RoomHeight,0,False,False)
                        NewWall.get_Parameter(DB.BuiltInParameter.WALL_ATTR_ROOM_BOUNDING).Set(0)
                        DB.JoinGeometryUtils.JoinGeometry(doc,NewWall,OldWall)
                        print("{RoomName}内墙创建成功".format(RoomName=Room.RoomName))

                except Exception as e:
                    print("{RoomName}内墙创建失败：{Problem}".format(RoomName=Room.RoomName,Problem=e))

        make_wall()


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
                print("{RoomName}建筑楼板未能被创建:{Problem}".format(RoomName=Room.RoomName, Problem=e))
        @rpw.db.Transaction.ensure('MakeFloor')
        def make_floor_Open(Floor):
            _doc = HOST_APP.doc.Create
            boundary=[]
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



