import logging
import os
import tempfile
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
    try:
        response = s3_client.upload_file(file_name, 'testqle', object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def createTempFile():
    file = tempfile.NamedTemporaryFile(delete=False)
    file.close()
    return file.name
