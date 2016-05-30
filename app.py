from flask import Flask, render_template, request

from cos import get_journals, CosSourceError
from ncbi_api import get_uids, get_journal_info
from utils import parse_search_request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        parsed_search_request = parse_search_request(request.form.get("search"))
        try:
            journals = []
            for journal in parsed_search_request.get('journals'):
                journals += get_journals(journal)
        except CosSourceError as e:
            return render_template('search.html', message=e.message)
        uids = get_uids(journals, parsed_search_request.get('year'))
        journals_info = get_journal_info(uids)
        return render_template('search.html', journals_info=journals_info)
    return render_template('search.html')


app.secret_key = '76e4c9f65bed8877c782e4032a3f5872b77a421'

if __name__ == "__main__":
    app.run(debug=True)

