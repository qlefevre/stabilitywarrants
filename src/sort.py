import operator
from datetime import datetime

import csv
import utils
from utils import formatNumber
from utils import toNumber


# Mnémo.	Code ISIN	Sous-jacent 	Barrière	Borne haute	Maturité	Maturité jours	Achat	Vente	Prix sous-jacent	Plage	Cible	Ecart Cible	Ecart Cible ABS
def transformRow(row):
    maturite = row['maturite'].partition(' ')[0]
    maturitedate = datetime.strptime(maturite, '%d/%m/%Y')
    maturitejours = (maturitedate - datetime.today()).days + 1

    borneBasse = toNumber(row['borne basse'])
    borneHaute = toNumber(row['borne haute'])
    prixsousjacent = toNumber(row['prix sous-jacent'])

    plage = borneHaute - borneBasse
    cible = borneBasse + 2 / 3 * plage
    ecartcible = prixsousjacent / cible * 100 - 100

    newRow = {
        'isin': row['isin'],
        'sous-jacent': row['sous-jacent'],
        'borne basse': formatNumber(borneBasse),
        'borne haute': formatNumber(borneHaute),
        'maturite': maturite,
        'maturite jours': maturitejours,
        'achat': formatNumber(toNumber(row['achat'])),
        'vente': formatNumber(toNumber(row['vente'])),
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
    stabilitywarrants_raw_csv = utils.download_file('sw/sg/%Y/%m/stabilitywarrants-%Y-%m-%d.csv')
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
        fieldnames = ['isin', 'sous-jacent', 'borne basse', 'borne haute', 'maturite', 'maturite jours',
                      'achat',
                      'vente', 'prix sous-jacent', 'plage', 'cible', 'ecart cible', 'ecart cible abs']
        writer = csv.DictWriter(writecsvfile, fieldnames=fieldnames, extrasaction='ignore', delimiter=';')
        writer.writeheader()
        for row in lines:
            writer.writerow(row)
    utils.upload_file(stabilitywarrants_csv, 'csv/%Y/%m/stabilitywarrants-%Y-%m-%d.csv')

    return {
        "body": "sort ok",
        "statusCode": 200
    }


if __name__ == '__main__':
    handle(None, None)
