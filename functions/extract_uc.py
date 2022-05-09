import csv
import gzip
import io
import urllib.parse
import urllib.request

import utils
from utils import extract_string


def handle(event, context):
    """
    Download stability warrants from Unicredit
    """
    print('Download stability warrants from Unicredit')

    url = 'https://www.bourse.unicredit.fr/fr.omr-search.csv'
    print('download ' + url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        + ' Chrome/97.0.4692.71 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
        + '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip'
    }
    values = {
        'page': '1',
        'rows': '30',
        'zeichnungsProducts': '0',
        'intradayIssued': '0',
        'maturityOpenEnd': '0',
        'bewertungsTagOpenEnd': '0',
        'capitalProtected': '0',
        'secondaryMarket': '0',
        'newIssuance': '0',
        'knockedOutProducts': '0',
        'productgroup': '136162747',
        'initialPaymentDateColumn': '0',
        'barrierStatusColumn': '0',
        'secIdColumn': '1',
        'basiswertColumn': '1',
        'underlyingPriceColumn': '1',
        'underlyingExchangeColumn': '1',
        'paymentCurrencyColumn': '0',
        'bewertungsTagColumn': '1',
        'riskIndicatorColumn': '1',
        'knockoutBarrierLevelLowerColumn': '1',
        'knockoutBarrierLevelUpperColumn': '1',
        'bidColumn': '1',
        'askColumn': '1',
        'changeperColumn': '1',
        'idnumColumn': '1',
        'secondaryMarketColumn': '1',
        'productFinder': 'default'
    }
    data = urllib.parse.urlencode(values).encode('ascii')
    req = urllib.request.Request(url, data, headers)
    stabilitywarrants_uc_csv = utils.create_temp_file()
    stabilitywarrants_cf_csv = utils.create_temp_file()
    with urllib.request.urlopen(req) as response:
        content = gzip.decompress(response.read())
        data = content.decode('iso-8859-1').replace('\r\n', '\r')
        with open(stabilitywarrants_uc_csv, 'w') as file_csv:
            file_csv.write(data)
        datacsv = data[data.find('ISIN'):]
        with open(stabilitywarrants_cf_csv, 'w') as file_csv:
            file_csv.write(
                'issuer;mnemo;isin;sous-jacent;borne basse;borne haute;maturite;achat;vente;prix sous-jacent\n')
            reader = csv.DictReader(io.StringIO(
                datacsv, newline='\r'), delimiter=';')
            for row in reader:
                file_csv.write(transform_row(row))
    utils.upload_file(stabilitywarrants_uc_csv,
                      'raw/uc/csv/%Y/%m/stabilitywarrants-raw-uc-%Y-%m-%d.csv')
    utils.upload_file(stabilitywarrants_cf_csv,
                      'sw/uc/%Y/%m/stabilitywarrants-uc-%Y-%m-%d.csv')


def transform_row(row):
    data = 'UC;'+row['Mnémo'] + ';'+row['ISIN'] + ';' + utils.clean_name(row['Sous-jacent']) + ';' + extract_string(
        row['Niveau de la barrière basse']) + ';'
    data += extract_string(row['Niveau de la borne haute']) + ';' + \
        row['Date d\'observation finale'].replace('.', '/') + ';'
    data += extract_string(row['Achat']) + ';' + extract_string(row['Vente']) + ';' + extract_string(
        row['Prix du sous-jacent']) + '\n'
    return data


if __name__ == '__main__':
    handle(None, None)
