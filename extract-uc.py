from datetime import datetime
import urllib.parse
import urllib.request
import gzip
import utils

"""
Download stability warrants from Unicredit
"""
url = 'https://www.bourse.unicredit.fr/fr.omr-search.csv'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
with open('stabilitywarrants-uc.csv', 'w') as file_csv:
    with urllib.request.urlopen(req) as response:
        content = gzip.decompress(response.read())
        file_csv.write(content.decode('iso-8859-1').replace('\r\n', '\r'))
utils.upload_file('stabilitywarrants-uc.csv','raw/uc/csv/'+datetime.today().strftime('%Y/%m')+'/stabilitywarrants-uc-'+datetime.today().strftime('%Y-%m-%d')+'.csv')
