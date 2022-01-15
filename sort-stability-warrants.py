import csv
from datetime import datetime
import operator
import urllib.request

def toNumber(value: str):
	str =  value.partition(' ')[0].replace(',','.')
	str = str if "." not in str else str.rstrip('0').rstrip('.')
	return int(str) if str.isdigit() else round(float(str),2)
	
def formatNumber(value: float):
	val = round(value,2)
	return int(val) if float(val).is_integer() else ('%0.2f' % val).replace('.',',')
	
	
# Mnémo.	Code ISIN	Sous-jacent 	Barrière	Borne haute	Maturité	Maturité jours	Achat	Vente	Prix sous-jacent	Plage	Cible	Ecart Cible	Ecart Cible ABS
def transformRow(row):

	maturite = row['Maturité'].partition(' ')[0]
	maturitedate = datetime.strptime(maturite, '%d/%m/%Y')
	maturitejours = (maturitedate-datetime.today()).days
	
	borneBasse=toNumber(row['Barrière'])
	borneHaute=toNumber(row['Borne haute'])
	prixsousjacent=toNumber(row['Prix sous-jacent'])
	
	plage=borneHaute-borneBasse
	cible=borneBasse+2/3*plage
	ecartcible=prixsousjacent/cible*100-100
	
	newRow = {'mnémo':row['Mnémo.'],
	'isin':row['Code ISIN'],
	'sous-jacent':row['Sous-jacent '],
	'borne basse':formatNumber(borneBasse),
	'borne haute':formatNumber(borneHaute),
	'maturité':maturite,
	'maturité jours':maturitejours,
	'achat':formatNumber(toNumber(row['Achat'])),
	'vente':formatNumber(toNumber(row['Vente'])),
	'prix sous-jacent':formatNumber(prixsousjacent),
	'plage':formatNumber(plage),
	'cible':formatNumber(cible),
	'ecart cible':formatNumber(ecartcible),
	'ecart cible abs':formatNumber(abs(ecartcible)),
	'_num_plage':plage,
	'_num_ecart_cible_abs':abs(ecartcible)
	}
	return newRow

lines = []
with open('import.csv', newline='') as readcsvfile:
#with urllib.request.urlopen('https://bourse.societegenerale.fr/EmcWebApi/api/ProductSearch/Export?PageNum=1&ProductClassificationId=8') as readcsvfile:
	reader = csv.DictReader(readcsvfile, delimiter=';')
	for row in reader:
		lines.append(transformRow(row))
# tri sous jacent, plage, ecart cible absolu
lines = sorted(lines, key = operator.itemgetter('_num_ecart_cible_abs'))
lines = sorted(lines, key = operator.itemgetter('_num_plage'),reverse=True)
lines = sorted(lines, key = operator.itemgetter('sous-jacent'))
with open('output.csv', 'w', newline='') as writecsvfile:
	fieldnames = ['mnémo','isin','sous-jacent','borne basse','borne haute','maturité','maturité jours','achat','vente','prix sous-jacent','plage','cible','ecart cible','ecart cible abs']
	writer = csv.DictWriter(writecsvfile, fieldnames=fieldnames,extrasaction='ignore', delimiter=';')
	writer.writeheader()
	for row in lines:
		writer.writerow(row)

