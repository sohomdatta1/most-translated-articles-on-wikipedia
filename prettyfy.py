import json

all_articles = json.load(open('alldata.json'))
for article in all_articles:
    qid = article[0]
    name = article[1]
    sitelinks = article[2]
    if ':' in name:
        continue
    else:
        print(f'<tr><td><a href="https://wikidata.org/wiki/Q{qid}">Q{qid}</a></td><td><a href="https://en.wikipedia.org/wiki/{name}">{name}</a></td><td>{sitelinks}</td></tr>')