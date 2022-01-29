import gzip
import logging
import os
import shutil
import tempfile
import urllib.request
from datetime import datetime

import boto3
from botocore.exceptions import ClientError


def xlsx(fname):
    import zipfile
    from xml.etree.ElementTree import iterparse
    z = zipfile.ZipFile(fname)
    strings = [el.text for e, el in iterparse(z.open('xl/sharedStrings.xml')) if el.tag.endswith('}t')]
    rows = []
    row = {}
    value = ''
    for e, el in iterparse(z.open('xl/worksheets/sheet1.xml')):
        if el.tag.endswith('}v'):  # <v>84</v>
            value = el.text
        if el.tag.endswith('}c'):  # <c r="A3" t="s"><v>84</v></c>
            if el.attrib.get('t') == 's':
                value = strings[int(value)]
            letter = el.attrib['r']  # AZ22
            while letter[-1].isdigit():
                letter = letter[:-1]
            row[letter] = value
            value = ''
        if el.tag.endswith('}row'):
            rows.append(row)
            row = {}
    return rows


def upload_file(file_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Replace year, month and day
    object_name = datetime.today().strftime(object_name)

    # Upload the file
    s3_client = boto3.client('s3',
                             region_name='nl-ams',
                             endpoint_url='https://s3.nl-ams.scw.cloud',
                             aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                             aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

    # Define the configuration rules
    cors_configuration = {
        'CORSRules': [{
            'AllowedHeaders': ['Authorization'],
            'AllowedMethods': ['GET'],
            'AllowedOrigins': ['*'],
            'ExposeHeaders': ['GET'],
            'MaxAgeSeconds': 3000
        }]
    }
    s3_client.put_bucket_cors(Bucket='testqle', CORSConfiguration=cors_configuration)
    with open(file_name, 'rb') as f_in:
        with gzip.open(file_name+'.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    try:
        response = s3_client.upload_file(file_name+'.gz', 'testqle', object_name,
            ExtraArgs={'ACL': 'public-read', 'ContentEncoding': 'gzip'})
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(object_name):
    object_name = datetime.today().strftime(object_name)
    url = 'https://testqle.s3.nl-ams.scw.cloud/' + object_name
    file, headers = urllib.request.urlretrieve(url)
    if headers.get('Content-Encoding') == 'gzip':
        ungzipped = createTempFile()
        with gzip.open(file, 'rb') as f_in:
            with open(ungzipped, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        file = ungzipped
    return file


def createTempFile():
    file = tempfile.NamedTemporaryFile(delete=False)
    file.close()
    return file.name


def toNumber(value: str):
    str = value.partition(' ')[0].replace(',', '.')
    str = str if "." not in str else str.rstrip('0').rstrip('.')
    return int(str) if str.isdigit() else round(float(str), 2)


def formatNumber(value: float):
    val = round(value, 2)
    return int(val) if float(val).is_integer() else ('%0.2f' % val).replace('.', ',')

def extractString(value: str):
    str = value.partition(' ')[0]
    str = str.replace(',0000','')
    if ',' in str:
        str = str[:-2]
    return str