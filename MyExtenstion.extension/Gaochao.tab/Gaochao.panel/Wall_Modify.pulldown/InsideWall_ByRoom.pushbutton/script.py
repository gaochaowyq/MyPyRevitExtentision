# -*- coding: utf-8 -*-
__doc__="分析设计中内墙与外墙的量"

from System.Collections.Generic import List
import clr
import System
import sys

clr.AddReference("RevitAPI")
import Autodesk
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
# Import RevitNodes
clr.AddReference("RevitNodes")

# Import Revit elements
from Revit.Elements import *
import Revit

clr.ImportExtensions(Revit.GeometryConversion)


import rpw
import pyrevit
from rpw import db,doc
from pyrevit import revit,DB,UI
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
    #covert to dynamo geometry
    #try:
    Lines=[i.ToProtoType() for i in Lines]
    #except:
    #    print("ToProtoType is Failed")
    #    raise GetRevitServiceError
    polyline=PolyCurve.ByJoinedCurves(Lines)
    OffstedPolyline=PolyCurve.Offset(polyline,Distance,False)
    result = PolyCurve.Explode(OffstedPolyline)
    result = [i.ToRevitType() for i in result]
    return result

#GetAllRoomAndWallFinish
#Rooms=db.Collector(of_category='OST_Rooms').get_elements(wrapped=False)
#Select All Room
Rooms= revit.get_selection()
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
    selection_list = revit.pick_rectangle(pick_filter=msfilter)

    filtered_list = []
    for el in selection_list:
        filtered_list.append(el.Id)

    Rooms.set_to(filtered_list)
    revit.uidoc.RefreshActiveView()
except Exception:
    pass
############################################################################

class BAT_Room:
    def __init__(self,Room):
        self.Room=Room
        self.WrapedRoom=db.Element(self.Room)
        self.RoomLevelId=self.Room.Level.Id
        self.RoomLevel = self.Room.Level
        print("Get Room {}".format(self.RoomName))
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
        except:
            print("{RoomName}房间无法获取高度".format(RoomName=Room.RoomName))
            raise
        return Heigth
    @property
    def RoomBase(self):
        return None
    @property
    def WallFinishType(self):
        try:
            WallFinishName=self.WrapedRoom.parameters['Wall Finish'].value
            param_id = DB.ElementId(DB.BuiltInParameter.SYMBOL_NAME_PARAM)
            parameter_filter = db.ParameterFilter(param_id, equals=WallFinishName)
            WallType = db.Collector(of_category='OST_Walls', parameter_filter=parameter_filter,
                                    is_type=True).get_first()
            if WallType:
                return WallType
            else:
                raise WallTypeError(self.RoomName)
        except WallTypeError as e:
            print(e)
    @property
    def FloorFinishType(self):
        try:
            WallFinishName=self.Room.get_Parameter(DB.BuiltInParameter.ROOM_FINISH_FLOOR)
            param_id = DB.ElementId(DB.BuiltInParameter.SYMBOL_NAME_PARAM)
            parameter_filter = db.ParameterFilter(param_id, equals=WallFinishName.AsString())
            FloorType = db.Collector(of_category='OST_Floors', parameter_filter=parameter_filter,
                                    is_type=True).get_first(wrapped=False)
            if FloorType:
                return FloorType
            else:
                raise GetElementError("Floor")
        except Exception as e:
            print(e)
            print("Cant Get Floor Type")

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
            print(e)

    @property
    def WallFinishTypeId(self):
        if self.WallFinishType is not None:
            return  self.WallFinishType.Id
        else:
            return None
    def RoomBoundary(self):
        room_boundary_options = DB.SpatialElementBoundaryOptions()
        room_boundary = self.Room.GetBoundarySegments(room_boundary_options)[0]
        return room_boundary


    def Offseted_RoomBoundary(self):
        try:
            room_boundary =self.RoomBoundary()
            Room_Aj_WallId=[i.ElementId for i in room_boundary]

            lines = [i.GetCurve() for i in room_boundary]

            Wall_Width = CovertToMM(self.WallFinishType.Width)

            polyline = OffsetLines(lines, -(Wall_Width / 2))
            return [polyline,Room_Aj_WallId]
        except Exception as e:
            print("{RoomName}内墙轮廓线生成失败，请查看单位设置是否为mm:{Problem}".format(RoomName=Room.RoomName,Problem=e))

    def MakeWall(self):
        @rpw.db.Transaction.ensure('Make Wall')
        def make_wall():
            Wall_curves =List[DB.Curve]()
            Aj_WallId=List[DB.ElementId]()
            for boundary_segment,Room_Aj_WallId in zip(self.Offseted_RoomBoundary()[0],self.Offseted_RoomBoundary()[1]):
                try:
                    Aj_WallId.Add(Room_Aj_WallId)
                    Wall_curves.Add(boundary_segment)       # 2015, dep 2016
                except AttributeError:
                    Wall_curves.Add(boundary_segment)  # 2017

            WallType =self.WallFinishType

            level =self.RoomLevelId
            for i,j in zip(Wall_curves,Aj_WallId):
                try:
                    OldWall = doc.GetElement(j)
                    OldWall = OldWall.GetTypeId()
                    OldWall = doc.GetElement(OldWall)
                    FamilyName=OldWall.get_Parameter(DB.BuiltInParameter.ALL_MODEL_FAMILY_NAME).AsString()
                    if FamilyName=="Curtain Wall" or FamilyName=="玻璃幕墙":
                        pass
                    elif FamilyName==None:
                        pass
                    else:
                        WallID=WallType.Id
                        NewWall=DB.Wall.Create(doc,i,WallID,level,self.RoomHeight,0,False,False)
                        NewWall.get_Parameter(DB.BuiltInParameter.WALL_ATTR_ROOM_BOUNDING).Set(0)

                        DB.JoinGeometryUtils.JoinGeometry(doc, NewWall, OldWall)
                except Exception as e:
                    print(e)
        try:
            make_wall()
            print("{RoomName} 内墙面被创建".format(RoomName=Room.RoomName))
        except Exception as e:
            print(e)
            print("{RoomName} 内墙未被创建".format(RoomName=Room.RoomName))
    def MakeFloor(self):
        @rpw.db.Transaction.ensure('MakeFloor')
        def make_floor():

            Wall_curves =List[DB.Curve]()
            lines = [i.GetCurve() for i in self.RoomBoundary()]
            for boundary_segment in lines:
                try:
                    Wall_curves.Add(boundary_segment)       # 2015, dep 2016
                except AttributeError:
                    Wall_curves.Add(boundary_segment)  # 2017

            FloorType =self.FloorFinishType



            level =self.RoomLevel
            Floor_CurveArray=DB.CurveArray()
            for i in Wall_curves:
                Floor_CurveArray.Append(i)
            _doc = pyrevit._HostApplication(__revit__).doc.Create

            _doc.NewFloor(Floor_CurveArray,FloorType,level,None)
        try:
            make_floor()
            print("{RoomName} 建筑楼面被创建".format(RoomName=Room.RoomName))
        except Exception as e:
            print(e)
            print("{RoomName} 建筑楼面未被创建".format(RoomName=Room.RoomName))

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
    Room.MakeWall()
    Room.MakeFloor()
    #Room.MakeCeiling()



