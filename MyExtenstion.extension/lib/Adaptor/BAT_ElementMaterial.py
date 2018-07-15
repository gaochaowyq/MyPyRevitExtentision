# -*- coding: utf-8 -*-
from rpw import doc
class BAT_ElementMaterial:
    def __init__(self,element):
        self.element=element
    def getmatids(self):
        return self.element.GetMaterialIds(False)
    def GetMaterialAreaWithName(self):
        c=[]
        for i in self.getmatids():
            b={}
            mat=doc.GetElement(i)
            matarea = self.element.GetMaterialArea(i, False) * 0.09290304
            matname=mat.Name
            b['name']=matname
            b['area']=matarea
            c.append(b)
        return c
