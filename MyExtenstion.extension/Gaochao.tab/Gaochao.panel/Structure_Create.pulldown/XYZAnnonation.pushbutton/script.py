# -*- coding: utf-8 -*-
__doc__ = "返回选择物体的类型"
import rpw
from rpw import db
from pyrevit import revit, DB, HOST_APP, UI
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList,select_file
from Helper import *
import csv
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


LocationFile=select_file('CSV(*.csv)|*.csv')

# 信息输入部分
GenericCategory = rpw.db.Collector(of_category='OST_GenericModel', is_type=True).get_elements(wrapped=False)


Framing_type_options = {t.FamilyName : t for t in GenericCategory}

Level_type = db.Collector(of_category='Levels', is_type=False).get_elements(wrapped=False)
Level_type_options = {DB.Element.Name: t for t in Level_type}

components = [

	Label('构件名称'),
	ComboBox('FamilyName', Framing_type_options),

	Button('确定')

]
Structure = []
form = FlexForm('结构', components)
form.show()

Value = form.values

Locations=[]
with open(LocationFile, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        point=[row[0],row[1],row[2],row[3]]
        Locations.append((point))





@rpw.db.Transaction.ensure('AnnonationPoint')
def PlaceAdaptiveCommponent(FamilySymbol,Index,Locations):

    numberOfLocation=len(Locations)

    numberOfPoint = DB.AdaptiveComponentFamilyUtils.GetNumberOfAdaptivePoints(FamilySymbol.Family)
    print(Locations)
    if numberOfLocation!=numberOfPoint:
        print("not same count location for point")
        return
    else:
        instance = DB.AdaptiveComponentInstanceUtils.CreateAdaptiveComponentInstance(doc, FamilySymbol)
        placePointIds = DB.AdaptiveComponentInstanceUtils.GetInstancePlacementPointElementRefIds(instance)
        instanceWraped=db.Element(instance)


        for i in range(0,numberOfPoint):
            point = doc.GetElement(placePointIds[i])
            point.Position = DB.XYZ(CovertToFeet(float(Locations[i][0])), CovertToFeet(float(Locations[i][1])),CovertToFeet(float( Locations[i][2])))
            instanceWraped.parameters['X'].value=float(Locations[i][0])
            instanceWraped.parameters['Y'].value = float(Locations[i][1])
            instanceWraped.parameters['Z'].value = float(Locations[i][2])
            instanceWraped.parameters['Mark'].value = Index

        print("well")

AnnonationType = Value['FamilyName']

for i in range(1,len(Locations)):
    PlaceAdaptiveCommponent(AnnonationType,Locations[i][0],[Locations[i][1:]])





