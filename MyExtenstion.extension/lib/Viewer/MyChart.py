# -*- coding: utf-8 -*-
import json
from pyrevit.output import charts
from pyrevit import script

__context__ = 'zerodoc'
output = script.get_output()
output.set_width(600)
test1_types = [charts.LINE_CHART,
               charts.BAR_CHART,
               charts.RADAR_CHART]

test2_types = [charts.BUBBLE_CHART]

test3_types = [charts.POLAR_CHART]

test4_types = [charts.PIE_CHART,
               charts.DOUGHNUT_CHART]

#Input Information
# Element.Title
#element.labels
#self.element.data
class MyCharts:
    def __init__(self,element,charttype=charts.PIE_CHART):
        #element
        #element.title=''
        #element.labels=[]
        # element.data=[]

        self.element=element
        self.chartype=charttype

    def get_test_chart(self,chart_type):
        chart = output.make_chart()
        chart.type = chart_type
        # chart.set_style('height:150px')
        # chart.options.maintainAspectRatio = True
        chart.options.title = {'display': True,
                               'text': '{}'.format(self.element.title),
                               'fontSize': 18,
                               'fontColor': '#000',
                               'fontStyle': 'bold'}
        return chart

    def test1_chart(self):
        chart = self.get_test_chart(self.chartype)
        # chart.options.scales = {'yAxes': [{'stacked': True}]}
        # chart.set_height(100)
        chart.data.labels =[i for i in self.element.labels ]

        set_a = chart.data.new_dataset('set_a')
        set_a.data =self.element.data

        #set_b = chart.data.new_dataset('set_b')
        #set_b.data = [2, 29, 5, 5, 2, 3, 10,11]
        # set_b.set_color(0xFF, 0xCE, 0x56, 0.8)
        # set_b.fill = False

        chart.randomize_colors()
        chart.draw()
    def ToJson(self):
        labels = [i for i in self.element.labels]
        set_a= self.element.data

        out={'labels':labels,'data':set_a,'titel':self.element.title}


        return out
