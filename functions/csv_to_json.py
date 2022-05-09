import csv
import json

import utils


def fix_number_and_properties(row):
    # suppression des espaces dans les noms
    row = {x.replace(' ', ''): v
           for x, v in row.items()}
    for key in row:
        if row[key].replace(',', '', 1).replace('.', '', 1).replace('-', '', 1).isdigit():
            row[key] = float(row[key].replace(',', '.', 1))
    return row


def handle(event, context):
    """
    Transforme le fichier final csv en json
    """
    print('Transforme le fichier final csv en json')

    stabilitywarrants_csv = utils.download_file(
        'csv/%Y/%m/stabilitywarrants-%Y-%m-%d.csv')
    stabilitywarrants_json = utils.create_temp_file()
    with open(stabilitywarrants_csv, 'r') as file_csv:
        fieldnames = file_csv.readline().strip().split(';')
        file_csv.seek(0)
        reader = csv.DictReader(file_csv, fieldnames, delimiter=';')

        with open(stabilitywarrants_json, 'w', encoding='utf8') as file_json:
            file_json.write('[')
            for index, row in enumerate(reader):
                if index > 0:
                    if index > 1:
                        file_json.write(',')
                    row = fix_number_and_properties(row)
                    json.dump(row, file_json, ensure_ascii=False,
                              separators=(',', ':'))
            file_json.write(']')
    utils.upload_file(stabilitywarrants_json,
                      'json/%Y/%m/stabilitywarrants-%Y-%m-%d.json')

    return {
        "message": "csv to json ok"
    }


if __name__ == '__main__':
    handle(None, None)
