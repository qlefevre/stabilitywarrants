import urllib.request

import utils
from utils import extract_number


def handle(event, context):
    """Download stability warrants from Société Générale

    Args:
        event : l'évènement associé à cette fonction lambda
        context : le contexte associé à cette fonction lambda
    """
    print('Download stability warrants from Société Générale')

    url = 'https://bourse.societegenerale.fr/EmcWebApi/api/ProductSearch/Export?PageNum=1&ProductClassificationId=8'
    print('download ' + url)

    stabilitywarrants_sg_xlsx, headers = urllib.request.urlretrieve(url)
    stabilitywarrants_sg_csv = utils.create_temp_file()
    stabilitywarrants_cf_csv = utils.create_temp_file()
    with open(stabilitywarrants_cf_csv, 'w') as cf_csv_file:
        cf_csv_file.write('issuer;mnemo;isin;sous-jacent;borne basse;borne haute;'
                          + 'maturite;achat;vente;prix sous-jacent\n')
        with open(stabilitywarrants_sg_csv, 'w') as csv_file:
            rows = utils.xlsx(stabilitywarrants_sg_xlsx)
            for idx, row in enumerate(rows):
                csv_file.write(
                    row['A'] + ';' + row['B'] + ';' +
                    row['C'] + ';' + row['D'] + ';'
                    + row['E'] + ';' + row['F'] + ';' +
                    row['G'] + ';' + row['H'] + ';'
                    + row['I'] + ';' + row['J'] + '\n')
                if idx > 0:
                    cf_csv_file.write(
                        'SG;'+row['A']+';'+row['B'] + ';' +
                        utils.clean_name(row['C']) + ';'
                        + extract_number(row['D']) + ';'
                        + extract_number(row['E']) + ';'
                        + extract_number(row['F']) + ';'
                        + extract_number(row['G']) + ';'
                        + extract_number(row['H']) + ';'
                        + row['J'].partition(' ')[0] + '\n')

    utils.upload_file(stabilitywarrants_sg_xlsx,
                      'raw/sg/xlsx/%Y/%m/stabilitywarrants-raw-sg-%Y-%m-%d.xslx')
    utils.upload_file(stabilitywarrants_sg_csv,
                      'raw/sg/csv/%Y/%m/stabilitywarrants-raw-sg-%Y-%m-%d.csv')
    utils.upload_file(stabilitywarrants_cf_csv,
                      'sw/sg/%Y/%m/stabilitywarrants-sg-%Y-%m-%d.csv')


if __name__ == '__main__':
    handle(None, None)
