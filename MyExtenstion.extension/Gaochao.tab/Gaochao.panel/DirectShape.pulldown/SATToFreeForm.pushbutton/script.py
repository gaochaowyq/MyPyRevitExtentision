# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import  sys
import rpw
import pyrevit
from rpw import db,doc
from pyrevit import revit,DB,UI,forms,HOST_APP
import System
from System.Collections.Generic import List
from pyrevit.framework import Stopwatch


picked = revit.pick_element()
stopwatch = Stopwatch()

sat_import = picked


geo_elem = sat_import.get_Geometry(DB.Options())
solids = []
for geo in geo_elem:


    if isinstance(geo, DB.Solid):
        print(geo)
        solids.append(geo)
    if isinstance(geo, DB.GeometryInstance):
        for i in geo.GetSymbolGeometry():
            print(i)
            solids.append(i)
        #solids.append(geo)

# create freeform from solids
with revit.Transaction("Convert ACIS to FreeFrom"):
    for solid in solids:
        DB.FreeFormElement.Create(revit.doc, solid)

print("Conversion completed in: {}".format(stopwatch.Elapsed))