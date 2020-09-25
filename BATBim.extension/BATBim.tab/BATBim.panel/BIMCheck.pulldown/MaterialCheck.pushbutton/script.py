# -*- coding: utf-8 -*-
__doc__="将Rhino的实体导入Revit"

from pyrevit import script
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
output = script.get_output()

if hostapp.app.Language.ToString()=="English_USA":
    ParameterName=LG_EUN()
elif hostapp.app.Language.ToString()=="Chinese_Simplified":
    ParameterName = LG_CHS()

def GetWallLayeredMaterial(Wall):
    materialNames=';'
    materialIds=[]
    wallType=Wall.WallType
    if wallType.Kind==DB.WallKind.Basic:
        wallCompoundStructure=wallType.GetCompoundStructure()
        layerCount=wallCompoundStructure.LayerCount
        for i in range(0,layerCount):
            materialId=wallCompoundStructure.GetMaterialId(i)
            materialIds.append(materialId)

            if materialId.IntegerValue==-1:
                return None
            else:
                materialNames+=doc.GetElement(materialId).Name
        return materialNames
    else:
        return "Not Layered Wall"


def GetFloorLayeredMaterial(Floor):
    materialNames = ';'
    materialIds = []
    floorType = Floor.FloorType
    floorCompoundStructure = floorType.GetCompoundStructure()
    layerCount = floorCompoundStructure.LayerCount
    for i in range(0, layerCount):
        materialId = floorCompoundStructure.GetMaterialId(i)
        materialIds.append(materialId)

        if materialId.IntegerValue == -1:
            return None
        else:
            materialNames += doc.GetElement(materialId).Name
    return materialNames

def GetElementMaterial(Element):
    materialNames = ';'
    materialIds = []
    materials = Element.GetMaterialIds(False)

    wrappedElement=db.Element(Element)

    for c in materials:
        if c.IntegerValue == -1:
            return None
        else:
            materialNames += doc.GetElement(c).Name
    return materialNames
def GetFamilyInstanceMaterial(FamilyInstance):
    materialNames = ';'
    materialIds = []
    family = FamilyInstance.Symbol.Family
    familyDoc = doc.EditFamily(family)
    collector = DB.FilteredElementCollector(familyDoc)
    collection =collector.OfClass(DB.GenericForm).ToElements()
    for i in collection:
        materialId=i.get_Parameter(DB.BuiltInParameter.MATERIAL_ID_PARAM).AsElementId()
        material = doc.GetElement(materialId)
        if material != None:
            materialName= material.Name
            materialNames+=materialName
        else:
            return None
    return materialNames

def GetPipeMaterial(Pipe):
    materialNames = ';'
    materialIds = []
    materialId=Pipe.get_Parameter(DB.BuiltInParameter.RBS_PIPE_MATERIAL_PARAM).AsElementId()
    material=doc.GetElement(materialId)
    if material!=None:
        materialNames = material.Name
        return materialNames
    else:
        return None

def GetDuctMaterial(Duct):
    materialNames = ';'
    materialIds = []
    MEPSystem=Duct.MEPSystem
    MEPSystemTypeId=MEPSystem.GetTypeId()

    MEPSystemType=doc.GetElement(MEPSystemTypeId)
    """
    Wraped=db.Element(MEPSystemType)

    print(Wraped.parameters['Material'].builtin)
    parameters=MEPSystemType.Parameters
    """

    #for i in parameters:
    #    print(i.AsValueString())


    materialId = MEPSystemType.get_Parameter(DB.BuiltInParameter.MATERIAL_ID_PARAM).AsElementId()
    material=doc.GetElement(materialId)
    if material!=None:
        materialNames = material.Name
        return materialNames
    else:
        return None


#Read Rhino File

allElementsInView=db.Collector(view=doc.ActiveView,is_type=False).get_elements(wrapped=False)

#allElementsInView=DB.FilteredElementCollector(doc)
NoProblem=[]
Problem=[]


for i in allElementsInView:
    materialNames =';'
    name = i.Name
    wrappedElement = db.Element(i)
    try:
        assemblyCode = wrappedElement.type.parameters[ParameterName.UNIFORMAT_CODE].value
    except:
        assemblyCode = None
    if isinstance(i,DB.View3D):
        continue
    elif isinstance(i,DB.Wall):
        materialNames=GetWallLayeredMaterial(i)
    elif isinstance(i,DB.Floor):
        materialNames=GetFloorLayeredMaterial(i)
    elif isinstance(i, DB.FamilyInstance):
        materialNames = GetFamilyInstanceMaterial(i)
    elif isinstance(i,DB.Plumbing.Pipe):
        materialNames=GetPipeMaterial(i)
    elif isinstance(i,DB.Mechanical.Duct):
        materialNames=GetDuctMaterial(i)
    else:
        #print(dir(i))
        #materialNames = GetElementMaterial(i)
        continue

    if name==None or name=='' or assemblyCode==None or assemblyCode=='' or materialNames==None:

        _output='<div style="background:red">name:{},assemblyCode:{},materials:{},Id:{}</div>'.format(name,assemblyCode,materialNames,i.Id)
        Problem.append([_output,i.Id])
        #output.print_html(_output)

    else:
        _output = '<div style="">name:{},assemblyCode:{},materials:{},Id:{}</div>'.format(name,assemblyCode,materialNames,i.Id)
        NoProblem.append([_output])

for i in Problem:
    output.print_html(i[0])
    print(output.linkify(i[1]))

for i in NoProblem:
    output.print_html(i[0])

