# -*- coding: utf-8 -*-
__doc__="创建"
from pyrevit.framework import List
import rpw
import System
from pyrevit import forms
from pyrevit import revit, DB
from pyrevit import HOST_APP
curview = revit.activeview
curdoc=revit.doc
#picked=revit.pick_elements()

p = System.Windows.Forms.Cursor.Position
print("This Function Will Coming Soon")

@rpw.db.Transaction.ensure('Make Parts Annotation')
def CreatePipeTage(picked,Position,EnbleY):
    tagMode = DB.TagMode.TM_ADDBY_CATEGORY
    tagorn = DB.TagOrientation.Horizontal
    wall = picked
    # Add the tag to the PickedPoint

    wallRef = DB.Reference(wall)
    newTag = DB.IndependentTag.Create(curdoc, curview.Id,  wallRef, True, tagMode, tagorn, Position)


    newTag.LeaderEndCondition = DB.LeaderEndCondition.Free
    elbowPnt = Position + DB.XYZ(0,EnbleY, 0.0)
    newTag.LeaderElbow = elbowPnt
    headerPnt = Position + DB.XYZ(10, EnbleY, 0.0)
    newTag.TagHeadPosition = headerPnt

StartPoint=[]
Elbow=[]
Head=[]
"""
for i in range(0,len(picked)):
    if i==0:
        midpoint= picked[i].Location
        print(midpoint)
        #StartPoint.append(midpoint)
        #Elbow.append(10)
"""
"""       
    else:
        pipline=picked[i].Location.Curve
        InterResult=pipline.Project(StartPoint[-1])
        point=InterResult.XYZPoint
        Distance=InterResult.Distance
        Elbow.append(10-Distance)
        StartPoint.append(point)
"""
#for i in range(0,len(picked)):
#    CreatePipeTage(picked[i],StartPoint[i],Elbow[i])






