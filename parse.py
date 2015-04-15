#!/usr/bin/python

"""
Parses a list of Allegro.pl pages showing offers of SSD drives and sorts them
by price per gigabyte.

Example usage:

# this is actually one line
seq 10 | xargs -I{} wget "http://allegro.pl/listing/listing.php?category=123540
&limit=180&offerTypeBuyNow=1&order=d&p={}&string=ssd+-wymiana+-adapter+-sshd
&search_scope=category-123540&bmatch=seng-v6-p-sm-isqm-4-e-0402" -Op{}

./parse.py p? p??
"""

from lxml import html
import sys

PER_GB_TAG = u'Pojemno\u015b\u0107 dysku (GB)'

per_gb = []
for filename in sys.argv[1:]:
    t = html.parse(filename)
    items = t.xpath('//header/h2/a/../../../../..')
    for i in items:
        price_elements = i.xpath('.//span [@class="buy-now dist"]')
        if len(price_elements) < 1 or len(price_elements[0]) < 1:
            continue
        price = price_elements[0][0].tail.rstrip()
        if price == '':
            continue
        price = float(price.replace(',', '.').replace(' ', ''))
        details = {}
        for dl in i.xpath('.//dl'):
            if len(dl) < 2:
                continue
            details[dl[0].text_content()] = float(dl[1].text_content())
        title = i.xpath('.//h2/a/span')[0].text
        if PER_GB_TAG not in details or details[PER_GB_TAG] == 0:
            continue
        per_gb += [(price / details[PER_GB_TAG], price,
                    details[PER_GB_TAG], title)]

import pprint
pprint.pprint(sorted(per_gb)[:10])
