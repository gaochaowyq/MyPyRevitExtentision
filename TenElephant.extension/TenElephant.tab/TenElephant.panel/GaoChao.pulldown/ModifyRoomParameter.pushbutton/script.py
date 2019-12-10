# -*- coding: utf-8 -*-
__doc__="DepthMap Analysis"
import clr
import time
import  sys
import rpw
import pyrevit
from rpw import db,doc,uidoc
from pyrevit import revit,DB,UI,forms,HOST_APP
import System
from System.Collections.Generic import List
from pyrevit.framework import Stopwatch
from  Helper import *

######################################

#allElementsInView = DB.FilteredElementCollector(doc, doc.ActiveView.Id).ToElements()

#for i in allElementsInView:
#    print(i)

allRoomInView=walls =db.Collector(of_category='OST_Rooms').get_elements(wrapped=True)

"""
categoryId =DB.ElementId(DB.BuiltInCategory.OST_GenericModel)

@rpw.db.Transaction.ensure('Solid Room')
def CreateOpeningForWall(Room):
    options=DB.Options()
    geometry=Room.get_Geometry(options)

    solid = List[DB.GeometryObject]()
    for i in geometry:
        if isinstance(i, DB.Solid) and i.Volume>0:
            solid.Add(i)
    try:
        ds = DB.DirectShape.CreateElement(doc, categoryId)
        ds.SetShape(solid)
        ds.Name = "MyShape"
        new=db.Element(ds)
        new.parameters["Mark"]=Room.Id
        new.parameters["Comments"] ="Room"


    except:
        print(solid)
"""

@rpw.db.Transaction.ensure('CovertRoomValueUnit')
def CovertRoomUnit(Room):
    Room.parameters["mArea"].value = CovertToM2(Room.parameters["Area"].value)

    Room.parameters["mPerimeter"].value =CovertToMM( Room.parameters["Perimeter"].value)
    try:
        Room.parameters["mVolume"].value = Room.parameters["Volume"].value
    except:
        Room.parameters["mVolume"].value =0
    try:
        Room.parameters["mHeight"].value = Room.parameters["Unbounded Height"].value
    except:
        Room.parameters["mHeight"].value = 0

for i in allRoomInView:
    CovertRoomUnit(i)



