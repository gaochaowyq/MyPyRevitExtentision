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
curview = revit.active_view 
curdoc=revit.doc
picked=revit.pick_element()
options=DB.Options()
categoryId =DB.ElementId(DB.BuiltInCategory.OST_GenericModel)

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




walls = db.Collector(of_class='Wall',is_not_type=True).get_elements(wrapped=False)




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
@rpw.db.Transaction.ensure('JoinWallAndConcreteFraming')
def JoinWallAndConcreteFraming(walls):
    for w in walls:
        try:
            #wSolid=GetElementSolid(w)[0]
            wBox=w.BoundingBox[curview]
            #ds = DB.DirectShape.CreateElement(curdoc, categoryId)
            #ListGeometry=List[DB.GeometryObject]()
            #ListGeometry.Add(wBox)
            #ds.AppendShape(ListGeometry)
            #print("Createed")
            outLine=DB.Outline(wBox.Min,wBox.Max)

            boundingBoxIntersectsFilter=DB.BoundingBoxIntersectsFilter(outLine)

            collector=DB.FilteredElementCollector(curdoc)

            elements = collector.WherePasses(boundingBoxIntersectsFilter).OfCategory(DB.BuiltInCategory.OST_StructuralFraming).ToElements()
            for i in elements:
                bSolid=GetFamilyInstanceSolid(i)
                wSolid=GetElementSolid(w)
                if len(bSolid)!=0:
                    result=DB.BooleanOperationsUtils.ExecuteBooleanOperation (wSolid[0],bSolid[0],DB.BooleanOperationsType.Intersect)
                    if result.Volume>0.0001:
                        DB.JoinGeometryUtils.JoinGeometry(curdoc,w,i)
                        print("ID{}与ID{}".format(w.Id,i.Id))
                else:
                    print("ID{}没有实体".format(i.Id))

        except Exception as e:
            print(e)
            print("ID:{}墙体有问题".format(w.Id))


#print(picked.Symbol.Parameter[DB.BuiltInParameter.FAMILY_STRUCT_MATERIAL_TYPE].AsValueString())

JoinWallAndConcreteFraming(walls)
print("完成所有剪切")








