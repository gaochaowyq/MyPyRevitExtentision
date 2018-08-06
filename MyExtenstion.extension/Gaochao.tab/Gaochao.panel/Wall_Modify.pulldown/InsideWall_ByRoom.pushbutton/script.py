# -*- coding: utf-8 -*-
__doc__="分析设计中内墙与外墙的量"
from System.Collections.Generic import List
import clr
clr.AddReference('ProtoGeometry')
# Import RevitNodes
clr.AddReference("RevitNodes")
import Revit

# Import Revit elements
from Revit.Elements import *

# Import DocumentManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
# Import ToProtoType, ToRevitType geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)
import sys
from Autodesk.DesignScript.Geometry import *
import rpw
from rpw import revit, DB, UI,db,doc,ui
from System.Collections.Generic import List
import json
#from pyrevit import this_script
from pyrevit.forms import CommandSwitchWindow
import subprocess as sp
#from pyrevit.coreutils.console import charts
from Autodesk.Revit.DB.Architecture import Room
from collections import namedtuple
from Helper import *

"""
#Wall Selection
selection = ui.Selection()

selected_rooms = [e for e in selection.elements if isinstance(e, Room)]
if not selected_rooms:
    UI.TaskDialog.Show('MakeWalls', 'You need to select at lest one Room.')
    sys.exit()
Wall_types = rpw.db.Collector(of_category='OST_Walls', is_type=True).elements
Wall_type_options = {DB.Element.Name.GetValue(t): t for t in Wall_types}

Wall_type = ui.forms.SelectFromList('Make Wall', Wall_type_options,
                                     description='Select Wall Type')
Wall_Width=CovertToMM(Wall_type.Width)
print(Wall_Width)
"""

def OffsetLines(Lines,Distance):
    #covert to dynamo geometry
    Lines=[i.ToProtoType() for i in Lines]
    polyline=PolyCurve.ByJoinedCurves(Lines)
    OffstedPolyline=PolyCurve.Offset(polyline,Distance,False)
    #corvet to revit geometry
    result=PolyCurve.Explode(OffstedPolyline)
    result=[i.ToRevitType() for i in result]
    return result
#GetAllRoomAndWallFinish
Rooms=db.Collector(of_category='OST_Rooms').get_elements(wrapped=False)
class BAT_Room:
    def __init__(self,Room):
        self.Room=Room
        self.WrapedRoom=db.Element(self.Room)
        self.RoomLevelId=self.Room.Level.Id
    @property
    def RoomName(self):
        p=DB.BuiltInParameter.ROOM_NAME
        Name=self.Room.get_Parameter(p).AsString()
        return Name

    @property
    def RoomHeight(self):
        p = DB.BuiltInParameter.ROOM_HEIGHT
        Heigth = self.Room.get_Parameter(p).AsDouble()
        return Heigth
    @property
    def WallFinishType(self):
        try:
            WallFinishName=self.WrapedRoom.parameters['Wall Finish'].value
        except:
            WallFinishName = self.WrapedRoom.parameters['Wall Finish'].value
        param_id = DB.ElementId(DB.BuiltInParameter.SYMBOL_NAME_PARAM)
        parameter_filter = db.ParameterFilter(param_id, equals=WallFinishName)
        WallType = db.Collector(of_category='OST_Walls',parameter_filter=parameter_filter,is_type=True).get_first()

        return  WallType
    @property
    def WallFinishTypeId(self):
        if self.WallFinishType is not None:
            return  self.WallFinishType.Id
        else:
            return None
    def Offseted_RoomBoundary(self):
        room_boundary_options = DB.SpatialElementBoundaryOptions()
        room_boundary =self.Room.GetBoundarySegments(room_boundary_options)[0]
        lines = [i.GetCurve() for i in room_boundary]
        Wall_Width = CovertToMM(self.WallFinishType.Width)
        polyline = OffsetLines(lines, -(Wall_Width / 2))
        return polyline
    def MakeWall(self):
        @rpw.db.Transaction.ensure('Make Wall')
        def make_wall():
            Wall_curves =List[DB.Curve]()
            for boundary_segment in self.Offseted_RoomBoundary():
                try:
                    Wall_curves.Add(boundary_segment)       # 2015, dep 2016
                except AttributeError:
                    Wall_curves.Add(boundary_segment)  # 2017

            WallType =self.WallFinishType

            level =self.RoomLevelId
            for i in Wall_curves:
                WallID=WallType.Id
                DB.Wall.Create(doc,i,WallID,level,self.RoomHeight,0,False,False)
        make_wall()

for _Room in Rooms:
    Room=BAT_Room(_Room)

    if Room.WallFinishType is not None:
        Room.MakeWall()
        print("{RoomName} 内墙面被创建".format(RoomName=Room.RoomName))
    else:
        print("{RoomName} 没有内墙面".format(RoomName=Room.RoomName))

