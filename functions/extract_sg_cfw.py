import urllib.request
from utils import create_temp_file
from utils import upload_file
from utils import extract_number
from utils import clean_asset_name
from utils import xlsx


def handle(event, context):
    """Download capped warrants and floored warrants from Société Générale

    Args:
        event : l'évènement associé à cette fonction lambda
        context : le contexte associé à cette fonction lambda
    """
    print('Download capped warrants and floored warrants from Société Générale')

    url = 'https://bourse.societegenerale.fr/EmcWebApi/api/ProductSearch/Export?PageNum=1&ProductClassificationId=12'
    print('download ' + url)

    cappedflooredwarrants_sg_xlsx, headers = urllib.request.urlretrieve(url)
    cappedflooredwarrants_sg_csv = create_temp_file()
    cappedflooredwarrants_cf_csv = create_temp_file()
    with open(cappedflooredwarrants_cf_csv, 'w') as cf_csv_file:
        cf_csv_file.write('issuer;mnemo;isin;sous-jacent;cappe floore;prix exercice;cap;'
                          + 'maturite;achat;vente;prix sous-jacent\n')

        with open(cappedflooredwarrants_sg_csv, 'w') as csv_file:
            rows = xlsx(cappedflooredwarrants_sg_xlsx)
            for idx, row in enumerate(rows):
                csv_file.write(
                    row['A'] + ';' + row['B'] + ';' +
                    row['C'] + ';' + row['D'] + ';' +
                    row['E'] + ';' + row['F'] + ';' +
                    row['G'] + ';' + row['H'] + ';' +
                    row['I'] + ';' + row['J'] + ';' +
                    row['K'] + ';' + row['L'] + '\n')
                if idx > 0:
                    cf_csv_file.write(
                        'SG;'+row['A']+';'+row['B'] + ';' +
                        clean_asset_name(row['C']) + ';'
                        + extract_number(row['D']) + ';'
                        + extract_number(row['F']) + ';'
                        + extract_number(row['G']) + ';'
                        + extract_number(row['E']) + ';'
                        + extract_number(row['J']) + ';'
                        + extract_number(row['K']) + ';'
                        + row['I'].partition(' ')[0] + '\n')

    upload_file(cappedflooredwarrants_sg_xlsx,
                'raw/cf/sg/xlsx/%Y/%m/cappedflooredwarrants-raw-sg-%Y-%m-%d.xslx')
    upload_file(cappedflooredwarrants_sg_csv,
                'raw/cf/sg/csv/%Y/%m/cappedflooredwarrants-raw-sg-%Y-%m-%d.csv')
    upload_file(cappedflooredwarrants_cf_csv,
                'cf/sg/%Y/%m/cappedflooredwarrants-sg-%Y-%m-%d.csv')


if __name__ == '__main__':
    handle(None, None)
