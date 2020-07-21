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


selections = revit.pick_element()

print(selections.UniqueId)