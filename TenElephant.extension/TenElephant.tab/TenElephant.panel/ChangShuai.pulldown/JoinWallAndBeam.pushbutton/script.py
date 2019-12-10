# -*- coding: utf-8 -*-
__doc__="链接墙体与梁"
from pyrevit.framework import List
import rpw
from rpw import db
import System
from pyrevit import forms
from pyrevit import revit, DB,UI
from pyrevit import HOST_APP
import traceback
curview = revit.activeview
curdoc=revit.doc
#picked=revit.pick_elements()
options=DB.Options()


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
        elif type(i)== DB.Sold:
            if i.Volume!=0:
                Solids.append(i)
    return Solids



    #for i in geo:
    #    print(i)
        #if type(i) != DB.GeometryInstance:
        #    if i.Volume!=0:
         #       Solids.append(i)
    #return Solids



walls = db.Collector(of_class='Wall',is_not_type=True).get_elements(wrapped=False)

#wallsSolid=[GetElementSolid(i) for i in walls]



"""
with db.Transaction('ChageWall'):
    for w in walls:
        for b in beams:
            try:
                wSolid=GetElementSolid(w)[0]
                wBox=wSolid.GetBoundingBox()
                bSolid = GetElementSolid(b)[0]

                result=DB.BooleanOperationsUtils.ExecuteBooleanOperation (wSolid,bSolid,DB.BooleanOperationsType.Intersect)
                if result.Volume>0.0001:
                    DB.JoinGeometryUtils.JoinGeometry(curdoc,w,b)

            except:
                print("Id{}或Id{}有问题请查看".format(w.Id,b.Id))


"""

with db.Transaction('ChageWall'):
    for w in walls:
        try:
            wSolid=GetElementSolid(w)[0]
            wBox=wSolid.GetBoundingBox()

            outLine=DB.Outline(wBox.Min,wBox.Max)

            boundingBoxIntersectsFilter=DB.BoundingBoxIntersectsFilter(outLine)

            collector=DB.FilteredElementCollector(curdoc)

            elements = collector.WherePasses(boundingBoxIntersectsFilter).OfCategory(DB.BuiltInCategory.OST_StructuralFraming).ToElements()


            for i in elements:
                bSolid=GetFamilyInstanceSolid(i)
                if len(bSolid)!=0:
                    result=DB.BooleanOperationsUtils.ExecuteBooleanOperation (wSolid,bSolid[0],DB.BooleanOperationsType.Intersect)
                    if result.Volume>0.0001:
                        DB.JoinGeometryUtils.JoinGeometry(curdoc,w,i)
                else:
                    pass

        except Exception as e:

            print("ID:{}墙体有问题".format(w.Id))
#HOST_APP.uiapp.PostCommand(UI.RevitCommandId.LookupPostableCommandId(UI.PostableCommand.JoinGeometry))

print("完成所有剪切")








