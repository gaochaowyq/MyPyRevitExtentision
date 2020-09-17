# -*- coding: utf-8 -*-
__doc__="将Rhino导入Revit中的多个实体拆分为单个Generic Family"
import rpw
import os
import clr
from rpw import db
from pyrevit import revit, DB, HOST_APP, UI,_HostApplication,forms
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox,Separator, Button,SelectFromList,select_file,CheckBox
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
#Materials = rpw.db.Collector(of_category='OST_Materials', is_type=False).get_elements(wrapped=False)
#Materials_options = {t.Name: t for t in Materials}
Category={ "常规模型":DB.BuiltInCategory.OST_GenericModel,
                     "墙":DB.BuiltInCategory.OST_Walls,
                     "结构框架": DB.BuiltInCategory.OST_StructuralFraming}

FamilyTemplateNames={"常规模型":"Metric Generic Model.rft"}


#信息输入部分
components = [
#Label('材质'),
#ComboBox('Material', Materials_options),
Label('类型'),
ComboBox('FamilyTemplateName', FamilyTemplateNames),
Label('AssemblyCode'),
TextBox('AssemblyCode', Text="14-10"),
Label('是否为结构框架'),
CheckBox('isFraming','isFraming'),
Button('确定')

]
form = FlexForm('结构', components)
form.show()
Value=form.values


isFraming=Value['isFraming']

assemblyCode=Value['AssemblyCode']


FamilyTemplateName=Value['FamilyTemplateName']


_familyTemplatePath=app.FamilyTemplatePath




#######Get Element Slids
picked=revit.pick_element()

name=picked.Name
_options=DB.Options()
_options.DetailLevel=DB.ViewDetailLevel.Fine
geo_elem = picked.get_Geometry(_options)
solids = []
for geo in geo_elem:
    print(geo)
    if isinstance(geo, DB.Solid):
        print(geo)
        solids.append(geo)
    if isinstance(geo, DB.GeometryInstance):
        for i in geo.GetSymbolGeometry():
            solids.append(i)
#########################










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
        mf=familyMgr.AddParameter("Material", DB.BuiltInParameterGroup.PG_MATERIALS, DB.ParameterType.Material, False)
        familyMgr.AssociateElementParameterToFamilyParameter(m,mf)
        #CreateNewType
        newType=familyMgr.NewType(familyname)
        #Add Assembly code
        assemblyCodeParameter=familyMgr.get_Parameter(DB.BuiltInParameter.UNIFORMAT_CODE)
        familyMgr.Set(assemblyCodeParameter,assemblyCode)
        if parameters!=None:
            for i,j in parameters:
                print(i,j)
        e.Commit()
    opt = DB.SaveAsOptions()
    opt.OverwriteExistingFile = True
    newFamilyPath="D:/Temp/{}.rfa".format(familyname)
    fdoc.SaveAs(newFamilyPath, opt)
    fdoc.Close()
    return newFamilyPath

def LoadFamily(familyPath,MatId):
    with revit.Transaction("LoadRevitFamily"):
        r = clr.Reference[DB.Family]()
        doc.LoadFamily(familyPath,r)
        familySymbolIds= r.GetFamilySymbolIds()

        for i in familySymbolIds:
            familySymbol=doc.GetElement(i)
            familySymbol.Activate()
            material = familySymbol.GetParameters("Material")
            #TODO only for one material
            print(material[0].Set(MatId))
            break
        if isFraming:
            st = DB.Structure.StructuralType.Beam
        else:
            st = DB.Structure.StructuralType.NonStructural

        newFamily=doc.Create.NewFamilyInstance(DB.XYZ(), familySymbol, st)



        #assemblyCodeParameter=newFamily.get_Parameter(DB.BuiltInParameter.UNIFORMAT_CODE)
        #assemblyCodeParameter.Set(assemblyCode)

template=os.path.join(_familyTemplatePath,FamilyTemplateName)

print(template)

print(len(solids))
for i in range(0,len(solids)):

    if solids[i].Faces.Size!=0:
        path=CreateSolidFamily(solids[i],template,"{}{}".format(name,i))
        print(solids[i].Faces.Size)
        matid=solids[i].Faces[0].MaterialElementId
        LoadFamily(path,matid)
