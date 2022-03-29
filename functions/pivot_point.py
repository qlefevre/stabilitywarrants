# Python program to read
# json file
 
 
import json
from datetime import datetime
import csv
import urllib.request

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
 

now = datetime.now()
previousMonthIdx = (now.month+11)%12
previousMonth = datetime(now.year,previousMonthIdx,1)
currentMonth = datetime(now.year,now.month,1)
# mois précédent 
urlLastMonth = 'https://query1.finance.yahoo.com/v7/finance/download/%5EFCHI?period1='+str(int(datetime.timestamp(previousMonth)))+'&period2='+str(int(datetime.timestamp(currentMonth)-86400))+'&interval=1mo&events=history'
print (urlLastMonth)
# mois courant 
urlCurrentMonth = 'https://query1.finance.yahoo.com/v7/finance/download/%5EFCHI?period1='+str(int(datetime.timestamp(currentMonth)))+'&period2='+str(int(datetime.timestamp(currentMonth)))+'&interval=1mo&events=history'
print (urlCurrentMonth)

print('PP month')
csvLastMonth, headers = urllib.request.urlretrieve(urlLastMonth)
with open(csvLastMonth, newline='') as readcsvfile:
	reader = csv.DictReader(readcsvfile, delimiter=',')
	for row in reader:
		ohlcLastMonth = OHLC(round(float(row['Open']),2),round(float(row['High']),2),round(float(row['Low']),2),round(float(row['Close']),2))
		print(ohlcLastMonth)
		pivotPointLastMonth = PivotPoint(ohlcLastMonth)
		print(pivotPointLastMonth)

print('PP 20 days')		
csvCurrentMonth, headers = urllib.request.urlretrieve(urlCurrentMonth)
with open(csvCurrentMonth, newline='') as readcsvfile:
	reader = csv.DictReader(readcsvfile, delimiter=',')
	for row in reader:
		ohlcLastMonth = OHLC(round(float(row['Open']),2),round(float(row['High']),2),round(float(row['Low']),2),round(float(row['Close']),2))
		print(ohlcLastMonth)
		pivotPointLastMonth = PivotPoint(ohlcLastMonth)
		print(pivotPointLastMonth)
 
