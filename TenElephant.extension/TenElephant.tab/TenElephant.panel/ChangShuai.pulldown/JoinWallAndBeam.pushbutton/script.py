# -*- coding: utf-8 -*-
__doc__="链接墙体与梁"
from pyrevit.framework import List
import rpw
from rpw import db
import System
from pyrevit import forms
from pyrevit import revit, DB,UI
from pyrevit import HOST_APP
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



walls = db.Collector(of_class='Wall',is_not_type=True).get_elements(wrapped=False)
beams = db.Collector(of_category='OST_StructuralFraming',is_not_type=True).get_elements(wrapped=False)

wallsSolid=[GetElementSolid(i) for i in walls]
beamsSolid=[GetElementSolid(i) for i in beams]



with db.Transaction('ChageWall'):
    for w in walls:
        for b in beams:
            try:
                wSolid=GetElementSolid(w)[0]
                bSolid = GetElementSolid(b)[0]
                result=DB.BooleanOperationsUtils.ExecuteBooleanOperation (wSolid,bSolid,DB.BooleanOperationsType.Intersect)
                if result.Volume>0.0001:
                    DB.JoinGeometryUtils.JoinGeometry(curdoc,w,b)
                    print("Id{}与Id{}成功剪切".format(w.Id, b.Id))

            except:
                print("Id{}或Id{}有问题请查看".format(w.Id,b.Id))



#HOST_APP.uiapp.PostCommand(UI.RevitCommandId.LookupPostableCommandId(UI.PostableCommand.JoinGeometry))










