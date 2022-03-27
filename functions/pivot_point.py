# Python program to read
# json file
 
 
import json
from datetime import datetime

class OHLC:
	def __init__(self,open, high, low, close):
		self.open = open
		self.high = high
		self.low = low
		self.close = close
	def __repr__(self):
		return 'OHLC '+str(self.open)+' '+str(self.high)+' '+str(self.low)+' '+str(self.close)

class PivotPoint:
	def __init__(self,ohlc):
		self.ohlc = ohlc
		o,l,h,c = ohlc.open,ohlc.low, ohlc.high, ohlc.close
		self.p = round(( h + l + c) / 3)
		self.l = ohlc.low
		self.h = ohlc.high
	def r1(self): 	
		return  (2 * self.p) - self.l
	def s1(self):
		return (2 * self.p) - self.h
	def r2(self):
		return self.p + (self.h - self.l)
	def s2(self):
		return self.p - (self.h - self.l)
	def r3(self):
		return self.r1() + (self.h - self.l)
	def s3(self):
		return self.s1() - (self.h - self.l)
	def __repr__(self):
		return 'Pivot Point s3 '+str(self.s3())+' s2 '+str(self.s2())+' s1 '+str(self.s1())+' p '+str(self.p)+' r1 '+str(self.r1())+' r2 '+str(self.r2())+' r3 '+ str(self.r3())
	

def extractOhlc(values):
	#for x in range(len(values)):
	#	print(values[x])
	# plus haut de la période
	high = round(max(map(lambda val: val['price'],values)))
	# plus bas de la période
	low = round(min(map(lambda val: val['price'],values)))
	open = round(values[0]['price'])
	close =round( values[-1]['price'])
	ohlc = OHLC(open,high,low,close)
	return ohlc
 
# Chargement des données
f = open('max.json')
data = json.load(f)
f.close()

# Récupère les 20 derniers éléments
last20days = data[-20:]

print('PP 20 days')
ohlc20days = extractOhlc(last20days)
print(ohlc20days)
pivotPoint20days = PivotPoint(ohlc20days)
print(pivotPoint20days)

# principal problème les données avec le plus bas et plus haut

date = datetime.today()
month = (date.month+11)%12
month_pattern = str(date.year)+'-'+str(month).zfill(2)+'-'
lastmonth = list(filter(lambda val: val['time'].startswith(month_pattern), data))

print('PP month')
ohlcLastMonth = extractOhlc(lastmonth)
print(ohlcLastMonth)
pivotPointLastMonth = PivotPoint(ohlcLastMonth)
print(pivotPointLastMonth)