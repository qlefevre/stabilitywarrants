from datetime import datetime
import urllib.request
import utils

"""
Download stability warrants from Société Générale 
"""
url = 'https://bourse.societegenerale.fr/EmcWebApi/api/ProductSearch/Export?PageNum=1&ProductClassificationId=8'

urllib.request.urlretrieve(url, 'stabilitywarrants-sg.xlsx')
with open('stabilitywarrants-sg.csv', 'w') as file_csv:
	rows = utils.xlsx('stabilitywarrants-sg.xlsx');
	for row in rows:
		file_csv.write(row['A']+';'+row['B']+';'+row['C']+';'+row['D']+';'+row['E']+';'+row['F']+';'+row['G']+';'+row['H']+';'+row['I']+';'+row['J']+'\n')
utils.upload_file('stabilitywarrants-sg.xlsx','raw/sg/xlsx/'+datetime.today().strftime('%Y/%m')+'/stabilitywarrants-sg-'+datetime.today().strftime('%Y-%m-%d')+'.xslx')
utils.upload_file('stabilitywarrants-sg.csv','raw/sg/csv/'+datetime.today().strftime('%Y/%m')+'/stabilitywarrants-sg-'+datetime.today().strftime('%Y-%m-%d')+'.csv')