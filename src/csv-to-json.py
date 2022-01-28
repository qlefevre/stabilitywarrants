import json

import csv
import utils

def handle(event, context):
    """
    Transforme le fichier final csv en json
    """
    stabilitywarrants_csv = utils.download_file('csv/%Y/%m/stabilitywarrants-%Y-%m-%d.csv')
    stabilitywarrants_json = utils.createTempFile()
    with open(stabilitywarrants_csv, 'r') as file_csv:
        fieldnames = ['mnémo', 'isin', 'sous-jacent', 'borne basse', 'borne haute', 'maturité', 'maturité jours',
                      'achat',
                      'vente', 'prix sous-jacent', 'plage', 'cible', 'ecart cible', 'ecart cible abs']
        reader = csv.DictReader(file_csv, fieldnames, delimiter=';')

        with open(stabilitywarrants_json, 'w', encoding='utf8') as file_json:
            file_json.write('[')
            for index, row in enumerate(reader):
                if (index != 0):
                    file_json.write(',')
                json.dump(row, file_json, ensure_ascii=False, separators=(',', ':'))
            file_json.write(']')
    utils.upload_file(stabilitywarrants_json, 'json/%Y/%m/stabilitywarrants-%Y-%m-%d.json')

    return {
        "message": "csv to json ok"
    }


if __name__ == '__main__':
    handle(None, None)
