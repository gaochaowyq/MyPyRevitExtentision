# -*- coding: utf-8 -*-
__doc__="Make Selected Room As Solid Geometry With flip normal"
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
from Helper import CovertToM2

######################################
options=DB.Options()
def GetElementSolid(Element):
    Solids=[]
    geo=Element.get_Geometry(options)
    for i in geo:
        if type(i) != DB.GeometryInstance:
            if i.Volume!=0:
                Solids.append(i)
    return Solids

class ElementParameter():

    @staticmethod
    def Value(Element,Name):
        parameters=Element.GetParameters(Name)

    @staticmethod
    def ParameterValue(Parameter):
        StorageType=Parameter.StorageType
        if StorageType==DB.StorageType.Integer:
            pass
        elif StorageType==DB.StorageType.Double:
            pass
        elif StorageType==DB.StorageType.String:
            pass
        elif StorageType==DB.StorageType.ElementId:
            pass
        else:
            pass









# by TessellatedShapeBuilder
"""
class FlipSolidNormal_Old:
    def __init__(self,Solid):
        self.solid=Solid
        self.builder = DB.TessellatedShapeBuilder()
        self.builder.Target = DB.TessellatedShapeBuilderTarget.Solid
        self.builder.Fallback = DB.TessellatedShapeBuilderFallback.Mesh

    def BuildMesh(self):
        face=self.solid.Faces


        for i in face:
            self.OffsetWallSurface(i)

    def OffsetWallSurface(self,Face):
        mesh=Face.Triangulate(1)
        #Index=mesh.Triangle
        Vertices=mesh.Vertices
        materialId=Face.MaterialElementId

        #Normal=Face.ComputeNormal(DB.UV(0, 0)).Normalize()

        #trans=DB.Transform.CreateTranslation(Normal*Distance)
        #Vertices=[trans.OfPoint(i) for i in Vertices]
        loopVertices = List[DB.XYZ]()
        self.builder.OpenConnectedFaceSet(True)
        for i in range(mesh.NumTriangles):
            triangle=mesh.Triangle[i]
            loopVertices.Add(Vertices[triangle.Index[0]])
            loopVertices.Add(Vertices[triangle.Index[1]])
            loopVertices.Add(Vertices[triangle.Index[2]])

            self.builder.AddFace(DB.TessellatedFace(loopVertices, materialId))
            loopVertices.Clear()

        self.builder.CloseConnectedFaceSet()

    def Result(self):
        self.builder.Build()

        result = self.builder.GetBuildResult()
        return result
"""


class FlipSolidNormal:
    def __init__(self,Solid):
        self.solid=Solid
        self.materialId = Solid.Faces[0].MaterialElementId

        solidOrShellTessellationControls=DB.SolidOrShellTessellationControls()

        solidOrShellTessellationControls.LevelOfDetail=0.5
        try:
            self.triangulatedSolidOrShell=DB.SolidUtils.TessellateSolidOrShell(self.solid,solidOrShellTessellationControls)
        except Exception as e:
            return 


        self.points=[]
        self.transIndex=[]

        self.builder = DB.TessellatedShapeBuilder()
        self.builder.Target = DB.TessellatedShapeBuilderTarget.AnyGeometry
        self.builder.Fallback = DB.TessellatedShapeBuilderFallback.Mesh

    def meshSolid(self):
        shellComponentCount=self.triangulatedSolidOrShell.ShellComponentCount
        self.builder.OpenConnectedFaceSet(True)
        for i in range(0,shellComponentCount):
            triangulatedShellComponent=self.triangulatedSolidOrShell.GetShellComponent(i)
            triangleCount=triangulatedShellComponent.TriangleCount
            for t in range(0,triangleCount):
                loopVertices = List[DB.XYZ]()
                triangle=triangulatedShellComponent.GetTriangle(t)
                loopVertices.Add(triangulatedShellComponent.GetVertex(triangle.VertexIndex0))
                loopVertices.Add(triangulatedShellComponent.GetVertex(triangle.VertexIndex1))
                loopVertices.Add(triangulatedShellComponent.GetVertex(triangle.VertexIndex2))
                self.builder.AddFace(DB.TessellatedFace(loopVertices, self.materialId))
        self.builder.CloseConnectedFaceSet()
        self.builder.Build()

        result = self.builder.GetBuildResult()

        print(result)
        return result
########################################
#selection = revit.pick_element_by_category("Rooms")

allRooms=db.Collector(of_category='OST_Rooms',is_type=False).get_elements(wrapped=False)
with db.Transaction('UnCutElement'):
    directShapeLibrary = DB.DirectShapeLibrary.GetDirectShapeLibrary(doc)

    directShapeLibrary.Reset()





@rpw.db.Transaction.ensure('SolidRoom')
def SolidRoom(Room):
    roomName = Room.Id.ToString()
    solid = GetElementSolid(Room)

    build = FlipSolidNormal(solid[0])

    newSolid = build.meshSolid().GetGeometricalObjects()
    new = List[DB.GeometryObject]()
    new.Add(newSolid[0])

    directShapeLibrary = DB.DirectShapeLibrary.GetDirectShapeLibrary(doc)
    directShapeType = DB.DirectShapeType.Create(doc, roomName, DB.ElementId(DB.BuiltInCategory.OST_Mass))
    directShapeType.SetShape(new)

    directShapeType.Parameter[DB.BuiltInParameter.UNIFORMAT_CODE].Set("14-90.03")

    directShapeLibrary.AddDefinitionType(roomName, directShapeType.Id)

    ds = DB.DirectShape.CreateElementInstance(doc, directShapeType.Id, directShapeType.Category.Id, roomName,DB.Transform.Identity)
    #ds.SetTypeId(directShapeType.Id)
    ds.Parameter[DB.BuiltInParameter.ALL_MODEL_MARK].Set("Room："+roomName)
    ds.Name = roomName

    wrapedNewRoom=db.Element(ds)

    wrapedNewRoom.parameters['Area']=round(CovertToM2(Room.Area),1)

    wrapedNewRoom.parameters['Price'] = Room.Area*10000

    wrapedNewRoom.parameters['BAT_Area'] = db.Element(Room).parameters['BAT_Area'].value

    wrapedNewRoom.parameters['InterWallType'] = Room.Parameter[DB.BuiltInParameter.ROOM_FINISH_WALL].AsString()

    print("done")


for i in allRooms:
    try:
        SolidRoom(i)
    except Exception as e:
        print(e)
        print("Room:{} Failed".format(i.Id))








