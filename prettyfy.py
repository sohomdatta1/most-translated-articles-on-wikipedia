import json
import datetime

all_articles = json.load(open('alldata.json'))
table = ''
c = 1
for article in all_articles:
    qid = article[0]
    name = article[1]
    sitelinks = article[2]
    if ':' in name or name == 'Main Page':
        continue
    else:
        table += f'<tr><td>{c}</td><td><a href="https://wikidata.org/wiki/Q{qid}">Q{qid}</a></td><td><a href="https://en.wikipedia.org/wiki/{name}">{name}</a></td><td>{sitelinks}</td></tr>'
    c += 1

boilerplate = open('boilerplate.html').read()
boilerplate = boilerplate.replace('{TABLE}', table)
boilerplate = boilerplate.replace('{TIMESTAMP}', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'))
with open('pretty.html', 'w') as f:
    f.write(boilerplate)