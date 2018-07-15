# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import rpw
from rpw import db,doc
from System.Collections.Generic import List
from pyrevit import revit, DB
import json
import pickle


picked=revit.pick_element()

wrapedelement=db.Element(picked)

print(wrapedelement.type.parameters['Keynote'].builtin)



