#!/usr/bin/python
# -*- coding: UTF-8 -*-
#licensed under CC-Zero: https://creativecommons.org/publicdomain/zero/1.0

from os.path import expanduser
from time import strftime

import time
import mariadb
import requests as r
import pywikibot as pwb
import json


HEADER = 'A list of items with the most sitelinks. Data as of <onlyinclude>{update_timestamp}</onlyinclude>.\n\n{{| class="wikitable sortable" style="width:100%; margin:auto;"\n|-\n! Item !! Sitelinks\n'
TABLE_ROW = '|-\n| {{{{Q|{qid}}}}} || {cnt}\n'
FOOTER = '|}\n\n[[Category:Wikidata statistics|Most sitelinked items]] [[Category:Database reports|Most sitelinked items]]'


def make_report() -> str:
    db = mariadb.connect(
        host='wikidatawiki.analytics.db.svc.wikimedia.cloud',
        database='wikidatawiki_p',
        default_file=f'{expanduser("~")}/replica.my.cnf'
    )
    cur = db.cursor(dictionary=True)

    query = 'SELECT ips_item_id, COUNT(*) AS cnt FROM wb_items_per_site GROUP BY ips_item_id ORDER BY cnt DESC LIMIT 50000'
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
    cur.close()
    db.close()
    json.dump(alldata_with_names, open('alldata.json', 'w+'))

    return text


def main() -> None:
    make_report()


if __name__ == '__main__':
    main()
