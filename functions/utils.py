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
    zip_file = zipfile.ZipFile(fname)
    strings = [el.text for e, el in iterparse(zip_file.open(
        'xl/sharedStrings.xml')) if el.tag.endswith('}t')]
    rows = []
    row = {}
    value = ''
    for inconnu, el in iterparse(zip_file.open('xl/worksheets/sheet1.xml')):
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
    url = 'https://s3.nl-ams.scw.cloud'
    bucket = 'testqle'

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Replace year, month and day
    object_name = datetime.today().strftime(object_name)

    print('upload   ' + url + '/' + bucket + '/' + object_name)

    # Upload the file
    s3_client = boto3.client('s3',
                             region_name='nl-ams',
                             endpoint_url=url,
                             aws_access_key_id=os.environ.get(
                                 'AWS_ACCESS_KEY_ID'),
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
    s3_client.put_bucket_cors(
        Bucket='testqle', CORSConfiguration=cors_configuration)
    with open(file_name, 'rb') as f_in:
        with gzip.open(file_name + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    try:
        extra_args = {'ACL': 'public-read', 'ContentEncoding': 'gzip'}
        s3_client.upload_file(file_name + '.gz', bucket,
                              object_name, extra_args)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(object_name):
    object_name = datetime.today().strftime(object_name)
    url = 'https://testqle.s3.nl-ams.scw.cloud/' + object_name
    print('download ' + url)
    downloaded_file, headers = urllib.request.urlretrieve(url)
    if headers.get('Content-Encoding') == 'gzip':
        ungzipped = create_temp_file()
        with gzip.open(downloaded_file, 'rb') as f_in:
            with open(ungzipped, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        downloaded_file = ungzipped
    return downloaded_file


def create_temp_file():
    """Create temporary file

    Returns:
        str: le nom du fichier temporaire
    """
    new_file = tempfile.NamedTemporaryFile(delete=False)
    new_file.close()
    return new_file.name


def to_number(value: str):
    if value == '-':
        value = '0'
    result = value.partition(' ')[0].replace(',', '.')
    result = result if "." not in result else result.rstrip('0').rstrip('.')
    return int(result) if result.isdigit() else round(float(result), 2)


def format_number(value: float):
    result = round(value, 2)
    return int(result) if float(result).is_integer() else ('%0.2f' % result).replace('.', ',')


def extract_string(value: str) -> str:
    """Extracts number from string

    Example: 
      7600,0000 POINTS -> 7600
      7800,00 Points -> 7800
      13,0000 EUR -> 13
      22,50 EUR -> 22
      7,5000 -> 7,50
      
    Args:
      value: string containing a number

    Returns:
      the number from string
    """
    result = value.partition(' ')[0]
    result = result.replace(',0000', '')
    result = result.replace(',00', '')
    if ',' in result and '00' in result:
        result = result[:-2]
    return result


def clean_name(name: str):
    name = name.replace('.', '')
    name = name.replace(' SA', '').replace(' SE', '')
    name = name.split(' NV')[0]
    name = name.split('®')[0]
    return name
