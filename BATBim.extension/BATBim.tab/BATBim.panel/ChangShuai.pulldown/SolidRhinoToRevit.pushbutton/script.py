# -*- coding: utf-8 -*-
__doc__="将Rhino的实体导入Revit"
import rpw
import os
import clr
from rpw.extras.rhino import Rhino as rc
from rpw import db
from pyrevit import revit, DB, HOST_APP, UI,_HostApplication,forms
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList,select_file
from Helper import LG_EUN,LG_CHS,CovertToFeet
from System.Collections.Generic import List
import csv
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
hostapp = _HostApplication()
app=__revit__.Application

if hostapp.app.Language.ToString()=="English_USA":
    ParameterName=LG_EUN()
elif hostapp.app.Language.ToString()=="Chinese_Simplified":
    ParameterName = LG_CHS()

#Read Rhino File
finlename=forms.pick_file(file_ext='3dm', files_filter='', init_dir='', restore_dir=True, multi_file=False, unc_paths=False)
Materials = rpw.db.Collector(of_category='OST_Materials', is_type=False).get_elements(wrapped=False)
Materials_options = {t.Name: t for t in Materials}
Category={ "常规模型":DB.BuiltInCategory.OST_GenericModel,
                     "墙":DB.BuiltInCategory.OST_Walls,
                     "结构框架": DB.BuiltInCategory.OST_StructuralFraming}

FamilyTemplateNames={"常规模型":"Metric Generic Model.rft"}


#信息输入部分
components = [
Label('材质'),
ComboBox('Material', Materials_options),
Label('类型'),
ComboBox('FamilyTemplateName', FamilyTemplateNames),
Label('Rhino图层'),
TextBox('Layer', Text="Default"),
Button('确定')

]
form = FlexForm('结构', components)
form.show()
Value=form.values

Mat=Value['Material'].Id

FamilyTemplateName=Value['FamilyTemplateName']
print(FamilyTemplateName)

_familyTemplatePath=app.FamilyTemplatePath


RhinoFile=rc.FileIO.File3dm.Read(finlename)

def GetOBjectByLayer(RehinoFile,LayerName):
    Objects=RehinoFile.Objects.FindByLayer(LayerName)
    return Objects
RhinoOBject=GetOBjectByLayer(RhinoFile,Value['Layer'])
#Mesh=[i.Geometry for i in RhinoOBject]
Mesh=[i for i in RhinoOBject]
meshNames=[]
for i in Mesh:
    meshNames.append(i.Name)
print(meshNames)
    #print(rc.Geometry.Brep.GetVolume)


# ShapeImportert
shaperImporter=DB.ShapeImporter()
shaperImporter.InputFormat=DB.ShapeImporterSourceFormat.Rhino
with db.Transaction('UnCutElement'):
    solids=shaperImporter.Convert(doc,finlename)
    for i in solids:
        print(i)


#geo_elem = sat_import.get_Geometry(DB.Options())
#for geo in geo_elem:
#    if isinstance(geo, DB.Solid):
#        solids.append(geo)
#    if isinstance(geo, DB.GeometryInstance):
#        for i in geo.GetSymbolGeometry():
#            solids.append(i)
#       #solids.append(geo)

# create freeform from solids
#with revit.Transaction("Convert ACIS to FreeFrom"):
#    for solid in solids:
#        DB.FreeFormElement.Create(revit.doc, solid)


print(solids)
"""
@rpw.db.Transaction.ensure('SolidToRevit')
def SolidToRevit(solid,name,code):
    #roomName = Room.Id.ToString()
    solid = solid

    #build = FlipSolidNormal(solid[0])

    newSolid = solid
    new = List[DB.GeometryObject]()
    new.Add(newSolid)

    directShapeLibrary = DB.DirectShapeLibrary.GetDirectShapeLibrary(doc)
    directShapeType = DB.DirectShapeType.Create(doc, name, DB.ElementId(Category))
    directShapeType.SetShape(new)

    directShapeType.Parameter[DB.BuiltInParameter.UNIFORMAT_CODE].Set(code)

    directShapeLibrary.AddDefinitionType(name, directShapeType.Id)

    ds = DB.DirectShape.CreateElementInstance(doc, directShapeType.Id, directShapeType.Category.Id, name,DB.Transform.Identity)
    print("done")
"""

"""
for i in range(0,len(meshNames)):
    SolidToRevit(solids[i],meshNames[i],'10.10.{}'.format(i))
"""

#templateFileName ='C:\ProgramData\Autodesk\RVT 2019\Family Templates\English\Metric Generic Model.rft'










def CreateSolidFamily(solid,template,familyname,**kwargs):
    parameters=kwargs.get('parameters')
    #Create Family
    with revit.Transaction("Create New Family"):
        fdoc = app.NewFamilyDocument(template)
    #Family Transaction
    with DB.Transaction(fdoc) as e:
        e.Start("create")
        revitSolid=DB.FreeFormElement.Create(fdoc, solid)
        familyMgr = fdoc.FamilyManager
        m=revitSolid.get_Parameter(DB.BuiltInParameter.MATERIAL_ID_PARAM)
        mf=familyMgr.AddParameter("MyColumnFinish", DB.BuiltInParameterGroup.PG_MATERIALS, DB.ParameterType.Material, False)
        familyMgr.AssociateElementParameterToFamilyParameter(m,mf)
        if parameters!=None:
            for i,j in parameters:
                print(i,j)
        e.Commit()
    opt = DB.SaveAsOptions()
    opt.OverwriteExistingFile = True
    newFamilyPath="c:/Temp/{}.rfa".format(familyname)
    fdoc.SaveAs(newFamilyPath, opt)
    fdoc.Close()
    return newFamilyPath

def LoadFamily(familyPath):

    with revit.Transaction("Convert ACIS to FreeFrom"):
        r = clr.Reference[DB.Family]()
        family=doc.LoadFamily(familyPath,r)
        familySymbolIds= r.GetFamilySymbolIds()

        for i in familySymbolIds:
            familySymbol=doc.GetElement(i)
            familySymbol.Activate()
            break


        st = DB.Structure.StructuralType.UnknownFraming

        doc.Create.NewFamilyInstance(DB.XYZ(), familySymbol, st)

template=os.path.join(_familyTemplatePath,FamilyTemplateName)

for i in range(0,3):

    path=CreateSolidFamily(solids[i],template,meshNames[i])
    LoadFamily(path)