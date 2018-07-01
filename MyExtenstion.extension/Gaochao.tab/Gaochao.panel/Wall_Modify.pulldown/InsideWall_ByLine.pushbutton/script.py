# -*- coding: utf-8 -*-
__doc__="分析设计中内墙与外墙的量"
import rpw
from rpw import revit, DB, UI,db,doc,ui
from System.Collections.Generic import List

#Wall Selection
selection = ui.Selection()
Line=selection.elements[0]
Wall_curves =List[DB.Curve]()
curve=Line.GeometryCurve
Wall_curves.Add(Line.GeometryCurve)
print(Wall_curves)
@rpw.db.Transaction.ensure('Make Wall')
def make_wall():
    level = db.Collector(of_category='Levels', is_type=False, where=lambda x: x.parameters['Name'] == 'Level 1')[0]
    levelid=level.Id

    DB.Wall.Create(doc,curve,levelid,False)

make_wall()
