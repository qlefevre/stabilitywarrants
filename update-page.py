import re

page = ''
with open('page.html', 'r') as file_page:
    page = file_page.read()
json = ''
with open('output.json', 'r') as file_json:
    json = file_json.read()
page = re.sub(r'this.warrants = \[[^\]]+]', 'this.warrants = ' + json, page)
with open('page.html', 'w') as file_page:
    file_page.write(page)
