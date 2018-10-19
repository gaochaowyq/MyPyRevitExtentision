# -*- encoding: utf-8 -*-
__doc__ = "设置构件价格"
import csv
import rpw
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList
from System.Collections.Generic import List
from pyrevit import revit, DB, HOST_APP, UI
import json
import pickle
from Helper import *
import math
from pyrevit import forms
from pyrevit.framework import Stopwatch
from Element.Elements import Room
from pyrevit import script
from Viewer.MyChart import _MyCharts

selected_switch =forms.CommandSwitchWindow.show(["初始化面积计算比例","建筑面积分析","计容面积分析","不计容面积分析"],
                                   message='请选择要执行的操作')

rooms= rpw.db.Collector(of_category='OST_Rooms', is_type=False).get_elements(wrapped=False)
template={'labels':[],'data':[],"titel":"房间面积分析"}

class Rooms:
	def __init__(self,rooms):
		self.rooms=rooms
		self.WrapedRooms=[Room(i) for i in rooms]
		self.template = {'labels': [], 'data': [], "titel": "房间面积分析 {}平方米 "}
	def Group(self):
		#{"room1":[WrapedRoom,WrapedRooms],"room2":[WrapedRoom,WrapedRoom]}
		NewGroup={}
		for i in self.WrapedRooms:
			name=i.name
			if NewGroup.get(name):
				NewGroup.get(name).append(i)
			else:
				NewGroup.setdefault(name,[i])
		return NewGroup
	def CreateDefaultRule(self):

		with open(r'd:\text.csv', 'wb') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			#spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
			for i in self.WrapedRooms:
				spamwriter.writerow([i.name.encode('utf8'), i.Area, i.Index,i.AreaRatio])

	def Result(self,Com="All"):
		#Comment =All、ByRatio、ByNoRatio
		Category={"All":"建筑总面积","ByRatio":"计容面积","ByNoRatio":"不计容面积"}
		_Com="Area_"+Com
		for name, WrapedRooms in self.Group().items():
			self.template.get('labels').append(name)
			areas = [i.__getattribute__(_Com) for i in WrapedRooms]
			self.template.get('data').append(sum(areas))
		TotalArea = sum(self.template.get('data'))
		self.template.__setitem__('titel', "建筑面积分析({Type}){area}平方米 ".format(area=TotalArea,Type=Category[Com]))
		return self.template


	def init(self):
		for i in self.WrapedRooms:
			with rpw.db.Transaction("Chage"):
				if i.Height>=2200:
					i.parameters['AreaRatio'].value=1
					print ("{roomname}AreaRation 设置为{value}".format(roomname=i.name,value=1))
				else:
					i.parameters['AreaRatio'].value = 0.5
					print ("{roomname}AreaRation 设置为{value}".format(roomname=i.name, value=0.5))





c=Rooms(rooms)

for i in c.WrapedRooms:
	if i.AreaRatio:
		pass
	else:
		forms.alert('请先初始化面积计算比例', exitscript=True)

if selected_switch == "初始化面积计算比例":
	c.init()
elif selected_switch == "建筑面积分析":
	Result=c.Result(Com="All")
	Chart=_MyCharts(Result)
	Chart.draw()
elif selected_switch == "计容面积分析":
	Result=c.Result(Com="ByRatio")
	Chart=_MyCharts(Result)
	Chart.draw()
elif selected_switch == "不计容面积分析":
	Result=c.Result(Com="ByNoRatio")
	Chart=_MyCharts(Result)
	Chart.draw()