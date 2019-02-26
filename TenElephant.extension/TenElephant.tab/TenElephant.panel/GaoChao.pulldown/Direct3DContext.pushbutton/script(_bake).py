# -*- coding: utf-8 -*-
__doc__="DepthMap Analysis"
import clr
import time
import  sys
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
class RenderingPassBufferStorage:
    def __init__(self,displayStyle):
        self.DisplayStyle = displayStyle
        self.Line=[]
        self.FormatBits=''
        self.PrimitiveCount=''
        self.VertexBufferCount=''
        self.IndexBufferCount=''
        self.VertexBuffer=''
        self.IndexBuffer=''
        self.VertexFormat=''
        self.EffectInstance=''




class RevitElementDrawingServer(DB.DirectContext3D.IDirectContext3DServer):
    def __init__(self,uiDoc,elem,offset):
        self.m_guid = System.Guid.NewGuid()
        self.m_uiDocument = uiDoc
        self.m_element = elem
        self.m_offset = offset
# Control When This Server is Working  Such As invoked for 3Dview
    def CanExecute(self):
        return True
    def GetApplicationId(self):
        return ""
    def GetBoundingBox(self):
        return None
    def GetDescription(self):
        return ("Duplicates graphics from a Revit element.")
    def GetName(self):
        return ("Revit Element Drawing Server")
    def GetServerId(self):
        return self.m_guid
    def GetServiceId(self):
        return DB.ExternalService.ExternalServices.BuiltInExternalServices.DirectContext3DService
    def GetSourceId(self):
        return ""
    def GetVendorId(self):
        return "ADSK"
    def RenderScene(self,what,that):
        vertexBuffer=DB.DirectContext3D.VertexBuffer(2)
        vertexBuffer.Map(2)
        vertexBuffer.GetVertexStreamPosition().AddVertex(DB.DirectContext3D.VertexPositon(DB.XYZ(0,0,0)))
        vertexBuffer.GetVertexStreamPosition().AddVertex(DB.DirectContext3D.VertexPositon(DB.XYZ(0, 0, 100)))
        vertexBuffer.Unmap()
        vertexCount=2
        indexBuffer=DB.DirectContext3D.IndexBuffer(2)
        indexBuffer.Map(2)
        indexBuffer.GetIndexStreamLine().AddLine(DB.DirectContext3D.IndexLine(0,1))
        indexBuffer.Unmap()
        indexCount=2
        VertexFormatBits=DB.DirectContext3D.VertexFormatBits.Position
        vertexFormat=DB.DirectContext3D.VertexFormat(VertexFormatBits)
        effectInstance=DB.DirectContext3D.EffectInstance(VertexFormatBits)
        primitiveType=DB.DirectContext3D.PrimitiveType.LineList
        start=0
        primitiveCount=0

        DB.DirectContext3D.DrawContext.FlushBuffer(
        vertexBuffer,
        vertexCount,
        indexBuffer,
        indexCount,
        vertexFormat,
        effectInstance,
        primitiveType,
        start,
        primitiveCount
        )

    def UseInTransparentPass(self):
        return True
    def UsesHandles(self):
        return False
    #Line StartPoint EndPoint
    def CreateBufferStorageForElement(self,Line,displayStyle):
        m_EdgeBufferStorage=RenderingPassBufferStorage(displayStyle)
        m_EdgeBufferStorage.VertexBufferCount=2
        m_EdgeBufferStorage.PrimitiveCount=1


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

b=AddMultipleRevitElementServers(uidoc)





