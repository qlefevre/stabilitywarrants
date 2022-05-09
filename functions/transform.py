import csv
import operator
from datetime import datetime

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
    perfMin = 0
    perfMax = 0
    if prixsousjacent != 0:
        perfMin = round((1-(borneBasse / prixsousjacent)) * 100, 2)
        perfMax = round((borneHaute/prixsousjacent-1)*100, 2)

    achat = toNumber(row['achat'])
    pvpotentielles = 0
    if achat != 0:
        pvpotentielles = round((10/achat-1)*100, 2)

    newRow = {
        'issuer': row['issuer'],
        'mnemo': row['mnemo'],
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
        'perf min': perfMin,
        'perf max': perfMax,
        '+/- potentielles': pvpotentielles,
        '_num_plage': plage,
        '_num_ecart_cible_abs': abs(ecartcible)
    }
    return newRow


def handle(event, context):
    """
       Transforme le fichier CSV
    """
    print('Transforme le fichier CSV')
    stabilitywarrants_raw_csv = utils.download_file(
        'sw/all/%Y/%m/stabilitywarrants-all-%Y-%m-%d.csv')
    stabilitywarrants_csv = utils.create_temp_file()
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
        fieldnames = ['issuer', 'mnemo', 'isin', 'sous-jacent', 'borne basse', 'borne haute', 'maturite', 'maturite jours',
                      'achat', 'vente', 'prix sous-jacent', 'plage', 'cible', 'ecart cible', 'ecart cible abs',
                      'perf min', 'perf max', '+/- potentielles']
        writer = csv.DictWriter(
            writecsvfile, fieldnames=fieldnames, extrasaction='ignore', delimiter=';')
        writer.writeheader()
        for row in lines:
            writer.writerow(row)
    utils.upload_file(stabilitywarrants_csv,
                      'csv/%Y/%m/stabilitywarrants-%Y-%m-%d.csv')

    return {
        "body": "sort ok",
        "statusCode": 200
    }


if __name__ == '__main__':
    handle(None, None)
