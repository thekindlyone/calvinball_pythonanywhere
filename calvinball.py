from flask import Flask, jsonify, render_template, request, url_for, g

app = Flask(__name__)
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import highlight
from datetime import datetime
ix=open_dir("index")
brf = highlight.HtmlFormatter()

def find(query):
    with ix.searcher() as searcher:
        query = QueryParser("transcript", ix.schema).parse(query)
        results = searcher.search(query)
        results.fragmenter=highlight.WholeFragmenter()
        results.formatter = brf
        return [dict(url=result['url'],summary=result.highlights('transcript'),date=datetime.strftime(result['date'],'%b %d %Y'),transcript=result['transcript']) for result in results]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    query = request.args.get('query')
    results=find(query)
    return jsonify(results)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0',debug=True)