# -*- coding: utf-8 -*-
__doc__="分析设计中内墙与外墙的量"
from System.Collections.Generic import List
import sys
import rpw
from rpw import revit, DB, UI,db,doc,ui
from System.Collections.Generic import List
import json
from scriptutils import this_script
from scriptutils.userinput import CommandSwitchWindow
import subprocess as sp
from pyrevit.coreutils.console import charts
from Autodesk.Revit.DB.Architecture import Room
from collections import namedtuple

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
Wall_type_id = Wall_type.Id
@rpw.db.Transaction.ensure('Make Wall')
def make_wall(new_wall):
    Wall_curves =List[DB.Curve]()

    for boundary_segment in new_wall.boundary:
        try:
            Wall_curves.Add(boundary_segment.Curve)       # 2015, dep 2016
        except AttributeError:
            Wall_curves.Add(boundary_segment.GetCurve())  # 2017

    WallType = new_wall.Walltype_id

    level =new_wall.base_level_id
    for i in Wall_curves:
        WallID=Wall_type.Id
        DB.Wall.Create(doc,i,WallID,level,1000,0,False,False)
        print("Done")






NewWall = namedtuple('NewWall', ['Walltype_id', 'boundary', 'base_level_id'])
new_walls = []
room_boundary_options = DB.SpatialElementBoundaryOptions()

for room in selected_rooms:
    room_level_id = room.Level.Id
    # List of Boundary Segment comes in an array by itself.
    room_boundary = room.GetBoundarySegments(room_boundary_options)[0]
    new_wall = NewWall(Walltype_id=Wall_type_id, boundary=room_boundary,base_level_id=room_level_id)
    new_walls.append(new_wall)
for new_floor in new_walls:
    make_wall(new_floor)
