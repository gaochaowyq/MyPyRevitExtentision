# -*- coding: utf-8 -*-
__doc__="DepthMap Analysis"
import clr
import time
import  sys
import rpw
import pyrevit
from rpw import db,doc,uidoc,ui
from pyrevit import revit,DB,UI,forms,HOST_APP
import System
from System.Collections.Generic import List
from pyrevit.framework import Stopwatch
uiapp = __revit__
######################################
options=DB.Options()
#allWallsInView = DB.FilteredElementCollector(doc, doc.ActiveView.Id).ToElements()

#for i in allElementsInView:
#    print(i)
def GetElementSolid(Element):
    Solids=[]
    geo=Element.get_Geometry(options)
    for i in geo:
        if type(i) != DB.GeometryInstance:
            if i.Volume!=0:
                Solids.append(i)
    return Solids
def GetFamilyInstanceSolid(Element):
    Solids=[]
    geo=Element.get_Geometry(options)
    for i in geo:
        if type(i)== DB.GeometryInstance:
            c=i.GetInstanceGeometry()
            for d in c:
                if d.Volume != 0:
                    Solids.append(d)
        elif type(i)== DB.Solid:
            if i.Volume!=0:
                Solids.append(i)
    return Solids
allWlassInView=db.Collector(view=doc.ActiveView,of_category='OST_Walls',is_type=False).get_elements(wrapped=False)

#Solids=[GetFamilyInstanceSolid(i) for i in allWlassInView]
AllCount=len(allWlassInView)

Complated=0

with db.Transaction('UnCutElement'):
    for c in allWlassInView:
        Cutting=DB.SolidSolidCutUtils.GetCuttingSolids (c)
        for z in Cutting:
            DB.SolidSolidCutUtils.RemoveCutBetweenSolids(doc,c,doc.GetElement(z))

@rpw.db.Transaction.ensure('UnCutAndUnJoinElement')
def UnCutOrUnJoinElement(Elements):
    for i in Elements:
        JoinedElements = DB.JoinGeometryUtils.GetJoinedElements(doc,i)
        for z in JoinedElements:
            DB.JoinGeometryUtils.UnjoinGeometry(doc, i, doc.GetElement(z))
        print("{}:UnJoined".format(i.Id))


UnCutOrUnJoinElement(allWlassInView)






