import requests
import os
import csv
import json


def create_short_links():
    linksfile = os.path.join('UrlProc', 'links.txt')
    resultsfile = os.path.join('UrlProc', 'shorten.csv')
    url = """https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyBFWFPvCzfbs_HdJUveJPAWirWRPjizXh8"""
    headers = {'Content-Type': 'application/json'}

    lines = tuple(open(linksfile, 'r').read().split('\n'))
    lines = tuple([line for line in lines if line != ''])

    with open(resultsfile, 'w') as csvfile:
        fieldnames = ['longUrl', 'shortUrl']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for line in lines:
            payload = """{}"longUrl": '{}'{}""".format('{', line, '}')
            res = requests.post(url, data=payload, headers=headers)
            if res.status_code != 200:
                print(res.status_code, res.reason)
            else:
                j = res.text.replace('\n', '')
                o = json.loads(j)
                writer.writerow({'longUrl': o['longUrl'], 'shortUrl': o['id']})


if __name__ == '__main__':
    create_short_links()
