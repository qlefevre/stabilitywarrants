import csv
import json

"""
Transforme le fichier final csv en json
"""
with open('output.csv', 'r') as file_csv:
    fieldnames = ['mnémo', 'isin', 'sous-jacent', 'borne basse', 'borne haute', 'maturité', 'maturité jours', 'achat',
                  'vente', 'prix sous-jacent', 'plage', 'cible', 'ecart cible', 'ecart cible abs']
    reader = csv.DictReader(file_csv, fieldnames, delimiter=';')

    with open('output.json', 'w', encoding='utf8') as file_json:
        file_json.write('[')
        for index, row in enumerate(reader):
            if (index != 0):
                file_json.write(',')
            json.dump(row, file_json, ensure_ascii=False)
        file_json.write(']')
