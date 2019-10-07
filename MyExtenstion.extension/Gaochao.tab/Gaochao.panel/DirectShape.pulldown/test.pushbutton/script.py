# -*- coding: utf-8 -*-
__doc__ = "返回选择物体的类型"
import sys
import rpw
import pyrevit
from rpw import db, doc
from pyrevit import revit, DB, UI, forms, HOST_APP
import System
from System.Collections.Generic import List

picked = revit.pick_element()
_vertices=[]
_faces=[]
_LENGTH = 0

"""
EntitySchemaGuid=picked.GetEntitySchemaGuids()
schemaBuilder = DB.ExtensibleStorage.SchemaBuilder(System.Guid("d64e3bab-7b93-415a-a20a-4d09ec106aaa"))
schemaBuilder.SetReadAccessLevel(DB.ExtensibleStorage.AccessLevel.Public)
schemaBuilder.SetWriteAccessLevel(DB.ExtensibleStorage.AccessLevel.Public)
# schemaBuilder.SetVendorId("ADSK")
schemaBuilder.SetSchemaName("LastTrySchema")
fieldBuilder = schemaBuilder.AddSimpleField("LastTrySchema", DB.XYZ().GetType())
fieldBuilder.SetUnitType(DB.UnitType.UT_Length)
fieldBuilder.SetDocumentation("a wall.")
schema = schemaBuilder.Finish()

with revit.Transaction("Convert ACIS to FreeFrom"):
    ds = DB.DirectShape.CreateElement(doc, categoryId)
    ds.SetShape(new)
    ds.Name = "MyShape"
"""
# solids.append(geo)


Solid = []

options=DB.Options()
options.DetailLevel=DB.ViewDetailLevel.Fine
options.IncludeNonVisibleObjects=True
print(picked.Name)

"""
for i in picked.get_Geometry(options):

    # for c in i.GetInstanceGeometry():
    #		print(c)\
    if isinstance(i, DB.Solid):
        print(i)
        if i.Volume != 0:
            Solid.append(i)
    if isinstance(i, DB.GeometryInstance):
        print(i)
        for c in i.GetInstanceGeometry():
            if c.Volume!=0:
                Solid.append(c)
    if isinstance(i, DB.Line):
        print(i)
"""
def CombineMullion(CurtainGrid):

    uGridIds=CurtainGrid.GetMullionIds()

    Mullions=[doc.GetElement( i ) for i in uGridIds]

    Geometrys=[i.Geometry[DB.Options()] for i in Mullions]
    #MullionIds=[i.FindInserts(True,True,True,True) for i in GridLines]
    GESExport(Geometrys[0])

    #print(Geometrys)

def GESExport(GE):
    global _LENGTH
    GeometryObject=[i for i in GE]
    for i in GeometryObject:
        if isinstance(i,DB.Curve):
            pass
        elif isinstance(i, DB.Edge):
            pass
        elif isinstance(i, DB.Face):
            pass
        elif isinstance(i, DB.GeometryElement):
            GESExport(i)
        elif isinstance(i, DB.GeometryInstance):
            GESExport(i.GetInstanceGeometry())
        elif isinstance(i, DB.Mesh):
            pass
        elif isinstance(i, DB.Point):
            pass
        elif isinstance(i, DB.PolyLine):
            pass
        elif isinstance(i, DB.Profile):
            pass
        elif isinstance(i, DB.Solid):
            faces=i.Faces
            meshs=[i.Triangulate() for i in faces]
            for c in meshs:
                v=MeshToNumber(c)[0]
                f=MeshToNumber(c)[1]
                _LENGTH+=len(v)

                for i in v:
                    _vertices.append(i)
                for i in f:
                    _faces.append(i+_LENGTH)
        else:
            raise ()

def MeshToNumber(Mesh):
    vertices=[]
    for c in Mesh.Vertices:
        vertices.append(c.X)
        vertices.append(c.Y)
        vertices.append(c.Z)

    faces=[]
    NumTri=Mesh.NumTriangles
    for i in range(0,NumTri):
        Mt=Mesh.Triangle[i]
        index=Mt.Index
        #faces.append(0)
        faces.append(int(index[0]))
        faces.append(int(index[1]))
        faces.append(int(index[2]))

    return [vertices,faces]






CombineMullion(picked.CurtainGrid)

print(_faces)
#print(_vertices)
# new=List[DB.GeometryObject]()
# new.Add(c)
# categoryId =DB.ElementId(DB.BuiltInCategory.OST_GenericModel)

# create freeform from solids
@rpw.db.Transaction.ensure('Create Mesh From Rhino')
def CreateMesh(GeometricalObjects):
    ds = DB.DirectShape.CreateElement(doc, DB.ElementId(DB.BuiltInCategory.OST_GenericModel))
    ds.ApplicationId = "Application id"
    ds.ApplicationDataId = "Geometry object id"

    ds.SetShape(GeometricalObjects)
    print("Id:{id} 创建成功".format(id=ds.Id))


#_Solid=Solid[-1]
#for i in range(1,len(Solid)):
#    try:
#        _Solid=DB.BooleanOperationsUtils.ExecuteBooleanOperation(_Solid,Solid[i],DB.BooleanOperationsType.Union)
#    except:
#        pass


#CreateMesh([_Solid])
