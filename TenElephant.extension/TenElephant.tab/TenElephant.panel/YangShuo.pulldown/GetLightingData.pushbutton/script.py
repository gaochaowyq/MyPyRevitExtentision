# -*- coding: utf-8 -*-
__doc__="创建"
from pyrevit.framework import List
import rpw
from pyrevit import forms
from pyrevit import revit, DB
from pyrevit import HOST_APP
from Element.Elements import BAT_Lighting
import csv
curview = revit.activeview
curdoc=revit.doc
picked=revit.pick_elements()

Data=[]
header=["LihgtNmae","IESName"]

for i in picked:
    data={}
    light=BAT_Lighting(i)
    data["LihgtNmae"]=light.GetFullNameWithId().encode("utf-8")
    data["IESName"] = light.GetIES().encode("utf-8")
    Data.append(data)

with open(r"c:\lightdata.csv","w") as f:
    fieldnames =header
    writer = csv.DictWriter(f,delimiter=',',lineterminator='\n',fieldnames=fieldnames)
    for i in Data:
        print(i)
        writer.writerow(i)










