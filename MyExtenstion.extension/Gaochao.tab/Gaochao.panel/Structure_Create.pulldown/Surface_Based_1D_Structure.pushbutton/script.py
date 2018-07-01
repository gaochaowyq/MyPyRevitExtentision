# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import rpw
from rpw import revit, DB, UI,db,doc
from System.Collections.Generic import List
import json

from scriptutils.userinput import CommandSwitchWindow
import subprocess as sp

#make One D Structure


Selection=rpw.ui.Pick().pick_face()


		