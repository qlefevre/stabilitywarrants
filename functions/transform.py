import csv
import operator
from datetime import datetime

from utils import create_temp_file
from utils import upload_file
from utils import download_file
from utils import format_number
from utils import to_number


# Mnémo.	Code ISIN	Sous-jacent 	Barrière	Borne haute	Maturité	Maturité jours	Achat
# Vente	Prix sous-jacent	Plage	Cible	Ecart Cible	Ecart Cible ABS
def transform_row(row):
    maturite = row['maturite'].partition(' ')[0]
    maturitedate = datetime.strptime(maturite, '%d/%m/%Y')
    maturitejours = (maturitedate - datetime.today()).days + 1

    borne_basse = to_number(row['borne basse'])
    borne_haute = to_number(row['borne haute'])
    prixsousjacent = to_number(row['prix sous-jacent'])

    plage = borne_haute - borne_basse
    cible = borne_basse + 2 / 3 * plage
    ecartcible = prixsousjacent / cible * 100 - 100
    perf_min = 0
    perf_max = 0
    if prixsousjacent != 0:
        perf_min = round((1-(borne_basse / prixsousjacent)) * 100, 2)
        perf_max = round((borne_haute/prixsousjacent-1)*100, 2)

    new_row = {
        'issuer': row['issuer'],
        'mnemo': row['mnemo'],
        'isin': row['isin'],
        'sous-jacent': row['sous-jacent'],
        'borne basse': format_number(borne_basse),
        'borne haute': format_number(borne_haute),
        'maturite': maturite,
        'maturite jours': maturitejours,
        'achat': format_number(to_number(row['achat'])),
        'vente': format_number(to_number(row['vente'])),
        'prix sous-jacent': format_number(prixsousjacent),
        'plage': format_number(plage),
        'cible': format_number(cible),
        'ecart cible': format_number(ecartcible),
        'ecart cible abs': format_number(abs(ecartcible)),
        'perf min': perf_min,
        'perf max': perf_max,
        '_num_plage': plage,
        '_num_ecart_cible_abs': abs(ecartcible)
    }
    return new_row


def handle(event, context):
    """
       Transforme le fichier CSV
    """
    print('Transforme le fichier CSV')
    stabilitywarrants_raw_csv = download_file(
        'sw/all/%Y/%m/stabilitywarrants-all-%Y-%m-%d.csv')
    stabilitywarrants_csv = create_temp_file()
    lines = []
    with open(stabilitywarrants_raw_csv, newline='') as readcsvfile:
        reader = csv.DictReader(readcsvfile, delimiter=';')
        for row in reader:
            lines.append(transform_row(row))
    # tri sous jacent, plage, ecart cible absolu
    lines = sorted(lines, key=operator.itemgetter('_num_ecart_cible_abs'))
    lines = sorted(lines, key=operator.itemgetter('_num_plage'), reverse=True)
    lines = sorted(lines, key=operator.itemgetter('sous-jacent'))
    with open(stabilitywarrants_csv, 'w', newline='') as writecsvfile:
        fieldnames = ['issuer', 'mnemo', 'isin', 'sous-jacent', 'borne basse', 'borne haute', 'maturite',
                      'maturite jours', 'achat', 'vente', 'prix sous-jacent', 'plage', 'cible', 'ecart cible',
                      'ecart cible abs', 'perf min', 'perf max', '+/- potentielles']
        writer = csv.DictWriter(
            writecsvfile, fieldnames=fieldnames, extrasaction='ignore', delimiter=';')
        writer.writeheader()
        for row in lines:
            writer.writerow(row)
    upload_file(stabilitywarrants_csv,
                'csv/%Y/%m/stabilitywarrants-%Y-%m-%d.csv')

    return {
        "body": "sort ok",
        "statusCode": 200
    }


if __name__ == '__main__':
    handle(None, None)
