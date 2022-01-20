import urllib.request

"""
Download stability warrants from Société Générale 
"""
url = 'https://bourse.societegenerale.fr/EmcWebApi/api/ProductSearch/Export?PageNum=1&ProductClassificationId=8'

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
            letter = el.attrib['r'] # AZ22
            while letter[-1].isdigit():
                letter = letter[:-1]
            row[letter] = value
            value = ''
        if el.tag.endswith('}row'):
            rows.append(row)
            row = {}
    return rows


urllib.request.urlretrieve(url, "import-sg.xlsx")
with open('import-sg.csv', 'w') as file_csv:
	rows = xlsx('import.xlsx');
	for row in rows:
		file_csv.write(row['A']+';'+row['B']+';'+row['C']+';'+row['D']+';'+row['E']+';'+row['F']+';'+row['G']+';'+row['H']+';'+row['J']+'\n')
