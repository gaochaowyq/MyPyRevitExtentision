# -*- coding: utf-8 -*-
__doc__ = "返回选择物体的类型"
import rpw
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList
from System.Collections.Generic import List
from rpw import doc,db
from pyrevit import revit, DB, HOST_APP, UI
import json
import pickle
from Helper import *
import math
from pyrevit import forms
from pyrevit.framework import Stopwatch
curview = revit.activeview
curdoc=revit.doc



selection = revit.pick_elements()
options=DB.Options()
def GetElementSolid(Element):
    Solids=[]
    geo=Element.get_Geometry(options)
    for i in geo:

        if type(i) != DB.GeometryInstance:
            if i.Volume!=0:
                Solids.append(i)
    return Solids

walls=[selection[0]]
beams=[selection[1]]

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

#print(GetElementSolid(selection))

print("完成所有剪切")