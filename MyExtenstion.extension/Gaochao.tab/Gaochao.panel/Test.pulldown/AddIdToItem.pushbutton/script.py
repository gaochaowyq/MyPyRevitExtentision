from __future__ import unicode_literals
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
import  json



AllElement=revit.pick_elements()



@rpw.db.Transaction.ensure('Add Element Id To Element')
def AddElementId():
    for i in AllElement:
        try:
            i=db.Element(i)
            i.parameters["ID"].value=i.unwrap().Id
            print(i.parameters["ID"].value)
        except Exception as  e:
            print(e)
Allinformation=[]
for i in AllElement:
    wrapedElement=db.Element(i)
    try:
        information=wrapedElement.parameters.to_dict()
        Allinformation.append(information[0])
    except:
        pass




with open("c:/TempParameter.txt",'wb') as f:
    for i in Allinformation:


        try:
            f.writelines(json.dumps(i,ensure_ascii=False))
        except:
            pass