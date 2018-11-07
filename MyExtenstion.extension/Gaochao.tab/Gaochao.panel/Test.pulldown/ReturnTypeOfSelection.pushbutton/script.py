# -*- coding: utf-8 -*-
__doc__ = "返回选择物体的类型"
import rpw
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList
from System.Collections.Generic import List
from rpw import doc
from pyrevit import revit, DB, HOST_APP, UI
import json
import pickle
from Helper import *
import math
from pyrevit import forms
from pyrevit.framework import Stopwatch

OST_WALL=DB.Category.GetCategory(doc,DB.BuiltInCategory.OST_Walls)

selection = revit.pick_element()
print(DB.BuiltInCategory.OST_Walls)
if selection.Category==OST_WALL:
    print(selection.Category.Name)