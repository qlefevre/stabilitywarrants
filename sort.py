import operator
from datetime import datetime

import csv
import utils
from utils import formatNumber
from utils import toNumber


# Mnémo.	Code ISIN	Sous-jacent 	Barrière	Borne haute	Maturité	Maturité jours	Achat	Vente	Prix sous-jacent	Plage	Cible	Ecart Cible	Ecart Cible ABS
def transformRow(row):
    maturite = row['Maturité'].partition(' ')[0]
    maturitedate = datetime.strptime(maturite, '%d/%m/%Y')
    maturitejours = (maturitedate - datetime.today()).days + 1

    borneBasse = toNumber(row['Barrière'])
    borneHaute = toNumber(row['Borne haute'])
    prixsousjacent = toNumber(row['Prix sous-jacent'])

    plage = borneHaute - borneBasse
    cible = borneBasse + 2 / 3 * plage
    ecartcible = prixsousjacent / cible * 100 - 100

    newRow = {
        'mnémo': row['Mnémo.'],
        'isin': row['Code ISIN'],
        'sous-jacent': row['Sous-jacent '],
        'borne basse': formatNumber(borneBasse),
        'borne haute': formatNumber(borneHaute),
        'maturité': maturite,
        'maturité jours': maturitejours,
        'achat': formatNumber(toNumber(row['Achat'])),
        'vente': formatNumber(toNumber(row['Vente'])),
        'prix sous-jacent': formatNumber(prixsousjacent),
        'plage': formatNumber(plage),
        'cible': formatNumber(cible),
        'ecart cible': formatNumber(ecartcible),
        'ecart cible abs': formatNumber(abs(ecartcible)),
        '_num_plage': plage,
        '_num_ecart_cible_abs': abs(ecartcible)
    }
    return newRow


def handle(event, context):
    stabilitywarrants_raw_csv = utils.download_file('raw/sg/csv/%Y/%m/stabilitywarrants-sg-%Y-%m-%d.csv')
    stabilitywarrants_csv = utils.createTempFile()
    lines = []
    with open(stabilitywarrants_raw_csv, newline='') as readcsvfile:
        reader = csv.DictReader(readcsvfile, delimiter=';')
        for row in reader:
            lines.append(transformRow(row))
    # tri sous jacent, plage, ecart cible absolu
    lines = sorted(lines, key=operator.itemgetter('_num_ecart_cible_abs'))
    lines = sorted(lines, key=operator.itemgetter('_num_plage'), reverse=True)
    lines = sorted(lines, key=operator.itemgetter('sous-jacent'))
    with open(stabilitywarrants_csv, 'w', newline='') as writecsvfile:
        fieldnames = ['mnémo', 'isin', 'sous-jacent', 'borne basse', 'borne haute', 'maturité', 'maturité jours',
                      'achat',
                      'vente', 'prix sous-jacent', 'plage', 'cible', 'ecart cible', 'ecart cible abs']
        writer = csv.DictWriter(writecsvfile, fieldnames=fieldnames, extrasaction='ignore', delimiter=';')
        writer.writeheader()
        for row in lines:
            writer.writerow(row)
    utils.upload_file(stabilitywarrants_csv, 'csv/%Y/%m/stabilitywarrants-%Y-%m-%d.csv')

    return {
        "message": "sort ok"
    }


if __name__ == '__main__':
    handle(None, None)
