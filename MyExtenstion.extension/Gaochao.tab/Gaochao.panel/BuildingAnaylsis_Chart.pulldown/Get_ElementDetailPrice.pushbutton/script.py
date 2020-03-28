# -*- coding: utf-8 -*-
__doc__="获取被选择物体的详细定额组成"
from rpw import revit, DB, UI,db,doc

from Helper import *

from Helper import *


from ElementPrice import ElementPrice

picked = revit.pick_elements()

#Get Price By Element
bPrice=[]

for i in picked:

	elementprice=ElementPrice(i).GetAllPrice()
	bPrice.append(elementprice)






from pyrevit import script

output = script.get_output()

result1=[]
c=0
for i in bPrice:
	c+=1
	a=['{}'.format(c),i.get('coder'),i.get('coder_name'),i.get('unit'),i.get('quality'),
	   i.get('unitprice'),i.get('totalprice'),i.get('totalrengonprice'),i.get('totalcailiaoprice'),
	   i.get('totaljixieprice')]

	result1.append(a)
print(result1)

# formats contains formatting strings for each column
# last_line_style contains css styling code for the last line
output.print_table(table_data=result1,
				   title="单位工程概算表",
				   columns=["序号","定额编号","子目名称","单位","数量", "单价","合价",'人工价格',"材料价格","机械价格"],
				   last_line_style='color:red;')



