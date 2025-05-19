#!/usr/bin/python
# -*- coding: UTF-8 -*-
# licensed under CC-Zero: https://creativecommons.org/publicdomain/zero/1.0

from os.path import expanduser
from time import strftime

import time
import mariadb
import requests as r
import json

def make_report() -> str:
    db = mariadb.connect(
        host='wikidatawiki.analytics.db.svc.wikimedia.cloud',
        database='wikidatawiki_p',
        default_file=f'{expanduser("~")}/replica.my.cnf'
    )
    cur = db.cursor(dictionary=True)

    query = """SELECT ips_item_id, COUNT(*) AS cnt
FROM wb_items_per_site 
WHERE ips_site_id NOT LIKE '%wikisource'
  AND ips_site_id NOT LIKE '%wikibooks'
  AND ips_site_id NOT LIKE '%wikivoyage'
  AND ips_site_id NOT LIKE '%wikiquote'
  AND ips_site_id != 'commonswiki'
  AND ips_site_id NOT LIKE '%wikiversity'
  AND ips_site_id NOT LIKE 'species'
  AND ips_site_id NOT LIKE '%wikinews'
GROUP BY ips_item_id
ORDER BY cnt DESC LIMIT 50000"""
    cur.execute(query)

    text = ''

    alldata = []
    print('Fetched data from database.')

    for row in cur:
        qid = row.get('ips_item_id')
        cnt = row.get('cnt')

        if qid is None or cnt is None:
            continue
        
        alldata.append((qid, cnt))

    alldata_with_names = []
    
    for i in range(0, len(alldata), 100):
        print(i)
        tt = alldata[i:i+100]
        qids = [x[0] for x in tt]
        query = 'SELECT ips_item_id, ips_site_page FROM wb_items_per_site WHERE ips_item_id IN ({}) AND ips_site_id = \'enwiki\''.format(','.join(['%s' for _ in tt]))
        cur.execute(query, qids)
        time.sleep(1)
        for row in cur:
            qid = row.get('ips_item_id')
            site = row.get('ips_site_page').decode('utf-8')
            ll = 0
            for x in tt:
                if x[0] == qid:
                    ll = x[1]
                    break
            alldata_with_names.append((qid, site, ll))

    alldata_with_names.sort(key=lambda x: x[2], reverse=True)
    cur.close()
    db.close()
    json.dump(alldata_with_names, open('alldata.json', 'w+'))

    return text


def main() -> None:
    make_report()


if __name__ == '__main__':
    main()
