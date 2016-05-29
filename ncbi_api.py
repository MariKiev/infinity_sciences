import requests

from bs4 import BeautifulSoup


def get_uids(journals, terms):
    uids_list = []

    for journal in journals[:6]:
        for term in terms:
            response = requests.get(
                    'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term={}+{}[pdat]'.format(journal, term)
            )
            page = BeautifulSoup(response.text, 'xml')
            uids_list += map(lambda x: x.text, page.find_all('Id'))
    return uids_list


def get_journal_info(uids):
    journals_info = {}
    for uid in uids:
        response = requests.get('http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={}'.format(uid))
        page = BeautifulSoup(response.text, 'xml')
        journal_name = list(map(lambda x: x.text, page.find_all('Item', {'Name': 'FullJournalName'})))
        journals_info.update({journal_name[0]:
              {
                  'authors': list(map(lambda x: x.text, page.find_all('Item', {'Name': 'Author'}))),
                  'pub_date': list(map(lambda x: x.text, page.find_all('Item', {'Name': 'PubDate', 'Type': 'Date'}))),
                  'epub_date': list(map(lambda x: x.text, page.find_all('Item', {'Name': 'EPubDate', 'Type': 'Date'})))
              }
          })
    return journals_info
