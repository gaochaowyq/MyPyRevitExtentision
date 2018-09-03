# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import rpw
from rpw import db,doc
from System.Collections.Generic import List
from pyrevit import revit, DB
import json
import pickle

"""
picked=revit.pick_element()

wrapedelement=db.Element(picked)

element=picked.get_Parameter(DB.BuiltInParameter.ROOM_FINISH_FLOOR)
print(element.AsString())

print(wrapedelement.parameters['Ceiling Finish'].builtin)
"""

"""
@rpw.db.Transaction.ensure('JoinWalls')
def JoinWalss(Wall1,Wall2):
    DB.JoinGeometryUtils.JoinGeometry(doc,Wall1,Wall2)
picked1Id=DB.ElementId(353548)

picked2Id=DB.ElementId(353853)

picked1=doc.GetElement(picked1Id)
picked2=doc.GetElement(picked2Id)

JoinWalss(picked1,picked2)
"""
picked=revit.pick_element()

print(picked.WallType.FamilyName)




