import json

import requests


class CosSourceError(Exception):
    def __init__(self, message):
        self.message = message


def get_journals(source):
    response = requests.get(get_endpoint(source))
    journals = json.loads(response.content.decode('utf-8'))

    journals_titles = []
    for journal in journals:
        journals_titles.append(journal.get('Journal Title'))

    return journals_titles


def get_endpoint(source):
    if source == 'https://cos.io/top/':
        return 'https://cos.io/static/topjournals.json'
    else:
        raise CosSourceError('Unknown source.')
