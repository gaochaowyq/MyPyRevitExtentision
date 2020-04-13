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
import random
from pyrevit import forms
from pyrevit.framework import Stopwatch
curview = revit.active_view
curdoc=revit.doc

<<<<<<< HEAD
selections = revit.pick_elements()

output=[]

count=0
for i in selections:
    locaiton=i.Location
    curve=locaiton.Curve
    length=CovertToMM(curve.Length)

    if length>3000:
        startpoint=curve.GetEndPoint(0)
        endpoint = curve.GetEndPoint(1)
        flow=random.randint(10,20)
        name=count
        index=count
        out={"startpoint":[0.1*CovertToMM(startpoint.X),0.1*CovertToMM(startpoint.Y),0.1*CovertToMM(startpoint.Z)],
             "endpoint":[0.1*CovertToMM(endpoint.X),0.1*CovertToMM(endpoint.Y),0.1*CovertToMM(endpoint.Z)],
             'flow':flow,"name":name,"index":index,'id':i.Id.IntegerValue}
        output.append(out)
    count+=1

with open('c:/pipelocaiton.json','w') as f :
    c=json.dumps(output,ensure_ascii=False)
    f.write(c)



"""
print(selection)
print(selection.UniqueId)

=======
import os
import sys
print(sys.path)

"""
selection = revit.pick_element()
>>>>>>> 6abd85293f4d93b2471d78ef71d0ba6a2c94bd75

options = DB.Options()

Geometry=selection.get_Geometry(options)


for i in Geometry:
    print(i)


<<<<<<< HEAD
=======

>>>>>>> 6abd85293f4d93b2471d78ef71d0ba6a2c94bd75
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
"""
