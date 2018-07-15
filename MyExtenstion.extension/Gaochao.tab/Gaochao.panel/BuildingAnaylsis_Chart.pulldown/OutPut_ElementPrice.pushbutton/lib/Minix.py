# -*- encoding: utf-8 -*-
import rpw
from rpw import db,doc
from pyrevit import DB
from Helper import *

class MixPipe(object):
	def Name(self):
		UnwrapedElement=[i.unwrap() for i in self.Elements()]
		Diameter=[]
		for i in self.Elements():
			try:
				try:
					Diameter.append(CovertToMM(i.parameters['Diameter'].value))
				except:
					Diameter.append(CovertToMM(i.parameters['直径'].value))
			except:
				Diameter.append("Connection")
		
		return ["{} {}mm".format(i.Name.encode('GB2312'),z) for i,z in zip(UnwrapedElement,Diameter)]


class MixConduit(object):
	def Name(self):
		#UnwrapedElement=[i.unwrap() for i in self.Elements()]
		try:
			return ["{}{}".format(i.type.parameters['Type Name'].value.encode('GB2312'),i.parameters['Size'].value) for i in self.Elements()]
		except:
			return ["{}{}".format(i.type.parameters["类型名称"].value.encode('GB2312'), i.parameters['尺寸'].value) for i in self.Elements()]


