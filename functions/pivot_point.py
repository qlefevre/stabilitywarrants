# Python program to read
# json file
from datetime import datetime
from datetime import timedelta
import csv
import urllib.request
import utils


class OHLC:
    def __init__(self, open, high, low, close):
        self.open = open
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
        o, l, h, c = ohlc.open, ohlc.low, ohlc.high, ohlc.close
        self.p = round((h + l + c) / 3)
        self.l = ohlc.low
        self.h = ohlc.high

    def r1(self):
        return round((2 * self.p) - self.l)

    def s1(self):
        return round((2 * self.p) - self.h)

    def r2(self):
        return round(self.p + (self.h - self.l))

    def s2(self):
        return round(self.p - (self.h - self.l))

    def r3(self):
        return round(self.r1() + (self.h - self.l))

    def s3(self):
        return round(self.s1() - (self.h - self.l))

    def __repr__(self):
        return 'Pivot Point s3 '+str(self.s3())+' s2 '+str(self.s2())+' s1 '+str(self.s1())+' p '+str(self.p)+' r1 '+str(self.r1())+' r2 '+str(self.r2())+' r3 ' + str(self.r3())

    def json(self):
        return '{"period":"'+self.period+'", "name":"'+self.name+'", "pivotpoint" : { "S3": '+str(self.s3())+', "S2": '+str(self.s2())+', "S1": '+str(self.s1())+', "P": '+str(self.p)+', "R1": '+str(self.r1())+', "R2": '+str(self.r2())+', "R3": '+str(self.r3())+' }}'


def extractOhlc(values):
    # for x in range(len(values)):
    #	print(values[x])
    # plus haut de la période
    high = round(max(map(lambda val: val['price'], values)))
    # plus bas de la période
    low = round(min(map(lambda val: val['price'], values)))
    open = round(values[0]['price'])
    close = round(values[-1]['price'])
    return OHLC(open, high, low, close)


def twentyDaysOhlc(pohlcs):
    ohlcs = pohlcs[-4:]
    open = ohlcs[0].open
    close = ohlcs[3].close
    low = min(map(lambda ohlc: ohlc.low, ohlcs))
    high = max(map(lambda ohlc: ohlc.high, ohlcs))
    return OHLC(open, high, low, close)


def pivotPoint(name, symbol):
    content = '"'+name+'":['
    # calcul des dates
    now = datetime.now()
    previousMonthIdx = (now.month+11) % 12
    previousMonth = datetime(now.year, previousMonthIdx, 1)
    currentMonth = datetime(now.year, now.month, 1)
    to30days = datetime(now.year, now.month, now.day)
    from30days = to30days - timedelta(30)

    print('PP '+name)

    # mois précédent
    urlLastMonth = '  https://query1.finance.yahoo.com/v7/finance/download/%5E'+symbol+'?period1=' + \
        str(int(datetime.timestamp(previousMonth)))+'&period2=' + \
        str(int(datetime.timestamp(currentMonth)-86400)) + \
        '&interval=1mo&events=history'
    print(urlLastMonth)
    # mois courant
    urlCurrentMonth = '  https://query1.finance.yahoo.com/v7/finance/download/%5E'+symbol+'?period1=' + \
        str(int(datetime.timestamp(from30days)))+'&period2=' + \
        str(int(datetime.timestamp(to30days)))+'&interval=1wk&events=history'
    print(urlCurrentMonth)

    print('PP month')
    csvLastMonth, headers = urllib.request.urlretrieve(urlLastMonth)
    with open(csvLastMonth, newline='') as readcsvfile:
        reader = csv.DictReader(readcsvfile, delimiter=',')
        for row in reader:
            ohlcLastMonth = OHLC(round(float(row['Open']), 2), round(float(
                row['High']), 2), round(float(row['Low']), 2), round(float(row['Close']), 2))
            print('  '+str(ohlcLastMonth))
            pivotPointLastMonth = PivotPoint(ohlcLastMonth, name, 'Mensuel')
            print('  '+str(pivotPointLastMonth))
            content += pivotPointLastMonth.json()+','

    print('PP 20 days')
    ohlcs20days = []
    csvCurrentMonth, headers = urllib.request.urlretrieve(urlCurrentMonth)
    with open(csvCurrentMonth, newline='') as readcsvfile:
        reader = csv.DictReader(readcsvfile, delimiter=',')
        for row in reader:
            if(row['Volume'] != '0' and row['Volume'] != 'null'):
                ohlc20day = OHLC(round(float(row['Open']), 2), round(float(
                    row['High']), 2), round(float(row['Low']), 2), round(float(row['Close']), 2))
                ohlcs20days.append(ohlc20day)
    # lignes trouvées
    print('  '+str(ohlcs20days))
    # transforme les 4 semaines en 1 mois
    ohlc20daysComputed = twentyDaysOhlc(ohlcs20days)
    print('  '+str(ohlc20daysComputed))
    pivotPoint20days = PivotPoint(ohlc20daysComputed, name, '20 jours')
    print('  '+str(pivotPoint20days))
    content += pivotPoint20days.json()+']'
    return content


def handle(event, context):
    """
       Calcule les points pivots en mensuel et sur 4 semaines glissantes
    """
    print('Calcule les points pivots en mensuel et sur 4 semaines glissantes')
    content = '{'+pivotPoint('CAC 40', 'FCHI')+',' + \
        pivotPoint('DAX', 'GDAXI')+'}'
    print('json')
    print(content)
    pivotpoint_json = utils.createTempFile()
    with open(pivotpoint_json, 'w', encoding='utf8') as file_json:
        file_json.write(content)
    utils.upload_file(pivotpoint_json, 'json/%Y/%m/pivotpoint-%Y-%m-%d.json')


if __name__ == '__main__':
    handle(None, None)
