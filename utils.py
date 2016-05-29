import re


def parse_search_request(search_request):
    return {'journals': re.findall(r"journals='([\d\w:/.]+)'", search_request),
            'publications': re.findall(r"publications='([\d\w:/.]+)'", search_request),
            'year': re.findall(r"year=([\d]{4})", search_request),
            }
