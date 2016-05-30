import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup


def get_uids(journals, terms):
    uids_list = []

    with ThreadPoolExecutor(max_workers=5) as pool:
        results = []
        for journal in journals[:50]:
            for term in terms:
                url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term={}+{}[pdat]'.format(journal, term)
                results.append(pool.submit(make_request, url))

        for future in as_completed(results):
            response = future.result()

            page = BeautifulSoup(response.text, 'xml')
            uids_list += map(lambda x: x.text, page.find_all('Id'))
    return uids_list


def get_journal_info(uids):
    authors_list = []
    results = []
    journals_info = {}
    with ThreadPoolExecutor(max_workers=5) as pool:
        for uid in uids:
            url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={}'.format(uid)
            results.append(pool.submit(make_request, url))

        for future in as_completed(results):
            response = future.result()

            page = BeautifulSoup(response.text, 'xml')
            journal_name = list(map(lambda x: x.text, page.find_all('Item', {'Name': 'FullJournalName'})))
            journals_info.update({journal_name[0]:
                  {
                      'authors': list(map(lambda x: x.text, page.find_all('Item', {'Name': 'Author'}))),
                      'pub_date': list(map(lambda x: x.text, page.find_all('Item', {'Name': 'PubDate', 'Type': 'Date'}))),
                      'epub_date': list(map(lambda x: x.text, page.find_all('Item', {'Name': 'EPubDate', 'Type': 'Date'})))
                  }
              })
            authors_list += list(map(lambda x: x.text, page.find_all('Item', {'Name': 'Author'})))
    print(len(authors_list))
    return journals_info


def make_request(url):
    response = requests.get(url)
    return response

