# Python program to read
# json file
from datetime import datetime
from datetime import timedelta
import csv
import urllib.request
from utils import create_temp_file
from utils import upload_file


class OHLC:
    def __init__(self, open_, high, low, close):
        self.open = open_
        self.high = high
        self.low = low
        self.close = close

    def __repr__(self):
        return 'OHLC '+str(self.open)+' '+str(self.high)+' '+str(self.low)+' '+str(self.close)


class PivotPoint:
    def __init__(self, ohlc, name, period):
        self.ohlc = ohlc
        self.period = period
        self.name = name
        l, h, c = ohlc.low, ohlc.high, ohlc.close
        self.p = round((h + l + c) / 3)
        self.low = ohlc.low
        self.high = ohlc.high

    def r1(self):
        return round((2 * self.p) - self.low)

    def s1(self):
        return round((2 * self.p) - self.high)

    def r2(self):
        return round(self.p + (self.high - self.low))

    def s2(self):
        return round(self.p - (self.high - self.low))

    def r3(self):
        return round(self.r1() + (self.high - self.low))

    def s3(self):
        return round(self.s1() - (self.high - self.low))

    def __repr__(self):
        return 'Pivot Point s3 '+str(self.s3())+' s2 '+str(self.s2())+' s1 '+str(self.s1())+' p '+str(self.p)+' r1 '+str(self.r1())+' r2 ' + str(self.r2())+' r3 ' + str(self.r3())

    def json(self):
        return '{"period":"'+self.period+'", "name":"'+self.name+'", "pivotpoint" : { "S3": '+str(self.s3())+', "S2": '+str(self.s2()) + ', "S1": '+str(self.s1())+', "P": '+str(self.p)+', "R1": '+str(self.r1())+', "R2": '+str(self.r2()) + ', "R3": '+str(self.r3())+' }}'


def extract_ohlc(values):
    # for x in range(len(values)):
    # print(values[x])
    # plus haut de la période
    high = round(max(map(lambda val: val['price'], values)))
    # plus bas de la période
    low = round(min(map(lambda val: val['price'], values)))
    open_ = round(values[0]['price'])
    close = round(values[-1]['price'])
    return OHLC(open_, high, low, close)


def twenty_day_ohlc(pohlcs):
    ohlcs = pohlcs[-4:]
    open_ = ohlcs[0].open
    close = ohlcs[3].close
    low = min(map(lambda ohlc: ohlc.low, ohlcs))
    high = max(map(lambda ohlc: ohlc.high, ohlcs))
    return OHLC(open_, high, low, close)


def pivot_point(name, symbol):
    content = '"'+name+'":['
    # calcul des dates
    now = datetime.now()
    previous_month_idx = (now.month+11) % 12
    previous_month = datetime(now.year, previous_month_idx, 1)
    current_month = datetime(now.year, now.month, 1)
    to30days = datetime(now.year, now.month, now.day)
    from30days = to30days - timedelta(30)

    print('PP '+name)

    # mois précédent
    url_last_month = '  https://query1.finance.yahoo.com/v7/finance/download/%5E'+symbol+'?period1=' + \
        str(int(datetime.timestamp(previous_month)))+'&period2=' + \
        str(int(datetime.timestamp(current_month)-86400)) + \
        '&interval=1mo&events=history'
    print(url_last_month)
    # mois courant
    url_current_month = '  https://query1.finance.yahoo.com/v7/finance/download/%5E'+symbol+'?period1=' + \
        str(int(datetime.timestamp(from30days)))+'&period2=' + \
        str(int(datetime.timestamp(to30days)))+'&interval=1wk&events=history'
    print(url_current_month)

    print('PP month')
    csv_last_month, headers = urllib.request.urlretrieve(url_last_month)
    with open(csv_last_month, newline='') as readcsvfile:
        reader = csv.DictReader(readcsvfile, delimiter=',')
        for row in reader:
            ohlc_last_month = OHLC(round(float(row['Open']), 2), round(float(
                row['High']), 2), round(float(row['Low']), 2), round(float(row['Close']), 2))
            print('  '+str(ohlc_last_month))
            pivot_point_last_month = PivotPoint(
                ohlc_last_month, name, 'Mensuel')
            print('  '+str(pivot_point_last_month))
            content += pivot_point_last_month.json()+','

    print('PP 20 days')
    ohlcs20days = []
    csv_current_month, headers = urllib.request.urlretrieve(url_current_month)
    with open(csv_current_month, newline='') as readcsvfile:
        reader = csv.DictReader(readcsvfile, delimiter=',')
        for row in reader:
            if(row['Volume'] != '0' and row['Volume'] != 'null'):
                ohlc20day = OHLC(round(float(row['Open']), 2), round(float(
                    row['High']), 2), round(float(row['Low']), 2), round(float(row['Close']), 2))
                ohlcs20days.append(ohlc20day)
    # lignes trouvées
    print('  '+str(ohlcs20days))
    # transforme les 4 semaines en 1 mois
    ohlc_20days_computed = twenty_day_ohlc(ohlcs20days)
    print('  '+str(ohlc_20days_computed))
    pivot_point_20days = PivotPoint(ohlc_20days_computed, name, '20 jours')
    print('  '+str(pivot_point_20days))
    content += pivot_point_20days.json()+']'
    return content


def handle(event, context):
    """
       Calcule les points pivots en mensuel et sur 4 semaines glissantes
    """
    print('Calcule les points pivots en mensuel et sur 4 semaines glissantes')
    content = '{'+pivot_point('CAC 40', 'FCHI')+',' + pivot_point('DAX', 'GDAXI') + \
        ',' + pivot_point('S&P 500', 'GSPC')+',' + \
        pivot_point('NASDAQ 100', 'IXIC')+'}'
    print('json')
    print(content)
    pivotpoint_json = create_temp_file()
    with open(pivotpoint_json, 'w', encoding='utf8') as file_json:
        file_json.write(content)
    upload_file(pivotpoint_json, 'json/%Y/%m/pivotpoint-%Y-%m-%d.json')


if __name__ == '__main__':
    handle(None, None)
