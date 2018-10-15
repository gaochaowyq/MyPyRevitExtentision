# -*- coding: utf-8 -*-
__doc__ = "返回选择物体的类型"
import rpw
from rpw import db, doc
from System.Collections.Generic import List
from pyrevit import revit, DB, HOST_APP, UI
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList
import json
import pickle
from Helper import *
import math
import clr
from pyrevit import forms
from pyrevit.framework import Stopwatch


def verify_selection(selected_elems, doc):
    if doc.IsFamilyDocument:
        if len(selected_elems) == 1 \
                and selected_elems[0].GetType() is DB.DirectShape:
            return True
        else:
            forms.alert('More than one element is selected or selected '
                        'element is not an ACIS Solid.', exitscript=True)
    else:
        forms.alert('Please select one imported ACIS SAT DirectShape '
                    'while in Family Editor.', exitscript=True)
    return False


stopwatch = Stopwatch()
selection = revit.get_selection()

if True:
    stopwatch.Start()
    sat_import = selection.first
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