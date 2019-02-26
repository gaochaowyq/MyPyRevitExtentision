# -*- coding: utf-8 -*-
__doc__="DepthMap Analysis"
import clr
import time
import  sys
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReferenceToFileAndPath(r'C:\Users\2016028\source\repos\CssclassTest\CssclassTest\bin\Debug\CssclassTest.dll')
from  CssclassTest import RevitElementDrawingServer
import rpw
import pyrevit
from rpw import db,doc,uidoc
from pyrevit import revit,DB,UI,forms,HOST_APP
import System
from System.Collections.Generic import List
from pyrevit.framework import Stopwatch
m_offset = DB.XYZ(0, 100, 45)

######################################

m_servers =[]
m_documents =[]

picked=revit.pick_elements()
def AddMultipleRevitElementServers(uidoc):
    references =picked
    directContext3DService = DB.ExternalService.ExternalServiceRegistry.GetService(DB.ExternalService.ExternalServices.BuiltInExternalServices.DirectContext3DService)
    msDirectContext3DService = directContext3DService
    serverIds = msDirectContext3DService.GetActiveServerIds()
    #Create one server per element.
    for reference in references:
        elem =reference

        revitServer =RevitElementDrawingServer(uidoc, elem, m_offset)
        directContext3DService.AddServer(revitServer)
        m_servers.append(revitServer)

        serverIds.Add(revitServer.GetServerId())

        msDirectContext3DService.SetActiveServers(serverIds)

        #m_documents.append(uidoc.Document)
        uidoc.UpdateAllOpenViews()

#c=RevitElementDrawingServer(uidoc,picked[0],DB.XYZ(0,0,10))
for i in range(0,1000):
    m_offset = DB.XYZ(1000, 100, 10+i)
    b=AddMultipleRevitElementServers(uidoc)




