from rpw import db
from pyrevit import revit, DB, HOST_APP, UI,_HostApplication
from Helper import LG_EUN,LG_CHS,CovertToMM

from System.Collections.Generic import List
doc = __revit__.ActiveUIDocument.Document
hostapp = _HostApplication()
if hostapp.app.Language.ToString()=="English_USA":
	ParameterName=LG_EUN()
elif hostapp.app.Language.ToString()=="Chinese_Simplified":
	ParameterName = LG_CHS()
