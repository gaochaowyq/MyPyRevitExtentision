# -*- coding: utf-8 -*-
__doc__ = "返回选择物体的类型"
import rpw
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList
from System.Collections.Generic import List
from pyrevit import revit, DB, HOST_APP, UI
import json
import pickle
from Helper import *
import math
from pyrevit import forms
from pyrevit.framework import Stopwatch



def verify_selection(selected_elems, doc):

    return True

stopwatch = Stopwatch()
selection = revit.pick_element()


sat_import = selection
geo_elem = sat_import.get_Geometry(DB.Options())
solids = []
for geo in geo_elem:
    if isinstance(geo, DB.Solid):
        if geo.Volume > 0.0:
            solids.append(geo)
# create freeform from solids
with revit.Transaction("Convert ACIS to FreeFrom"):
    for solid in solids:
        DB.FreeFormElement.Create(revit.doc, solid)

print("Conversion completed in: {}".format(stopwatch.Elapsed))