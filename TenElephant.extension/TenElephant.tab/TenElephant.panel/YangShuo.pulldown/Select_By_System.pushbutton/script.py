# -*- coding: utf-8 -*-
__doc__ = "根据系统选择构件"
from pyrevit.framework import List
from pyrevit import forms
from pyrevit import revit, DB
from rpw import UI, db, doc
import rpw

from pyrevit.forms import CommandSwitchWindow
import subprocess as sp

#根据Accessmbly Code 筛选构件
title="根据系统名称选择构件"
description="根据系统名称选择构件"
value=rpw.ui.forms.TextInput(title, default=None, description=description, sort=True, exit_on_close=True)
MEP_System_Name=value.split("+")

print([MEP_System_Name])


#RBS_PIPING_SYSTEM_TYPE_PARAM
def Select_By_MEPSystem():
    curview = revit.activeview

    elements = DB.FilteredElementCollector(revit.doc, curview.Id) \
        .WhereElementIsNotElementType() \
        .ToElementIds()

    element_to_isolate = []
    for elid in elements:
        el = revit.doc.GetElement(elid)
        try:
            if el.get_Parameter(DB.BuiltInParameter.RBS_PIPING_SYSTEM_TYPE_PARAM).AsValueString() in (MEP_System_Name):
                element_to_isolate.append(el)
            elif el.get_Parameter(DB.BuiltInParameter.RBS_DUCT_SYSTEM_TYPE_PARAM).AsValueString() in (MEP_System_Name):
                element_to_isolate.append(el)
        except Exception as e:
            pass
    return  element_to_isolate




# element_to_id.sort()


# selected=element_to_id[-1]



Element=Select_By_MEPSystem()
revit.get_selection().set_to(Element)

























