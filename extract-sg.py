import urllib.request

import utils


def handle(event, context):
    """
    Download stability warrants from Société Générale
    """
    url = 'https://bourse.societegenerale.fr/EmcWebApi/api/ProductSearch/Export?PageNum=1&ProductClassificationId=8'

    stabilitywarrants_sg_xlsx, headers = urllib.request.urlretrieve(url)
    stabilitywarrants_sg_csv = utils.createTempFile()
    with open(stabilitywarrants_sg_csv, 'w') as csv_file:
        rows = utils.xlsx(stabilitywarrants_sg_xlsx)
        for row in rows:
            csv_file.write(
                row['A'] + ';' + row['B'] + ';' + row['C'] + ';' + row['D'] + ';' + row['E'] + ';' + row['F'] + ';' +
                row['G'] + ';' + row['H'] + ';' + row['I'] + ';' + row['J'] + '\n')
    utils.upload_file(stabilitywarrants_sg_xlsx, 'raw/sg/xlsx/%Y/%m/stabilitywarrants-sg-%Y-%m-%d.xslx')
    utils.upload_file(stabilitywarrants_sg_csv, 'raw/sg/csv/%Y/%m/stabilitywarrants-sg-%Y-%m-%d.csv')


if __name__ == '__main__':
    handle(None, None)
