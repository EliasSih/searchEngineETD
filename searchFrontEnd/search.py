from flask import Flask, render_template, request
import pysolr
import os

app = Flask(__name__)

solr = pysolr.Solr('http://localhost:8983/solr/ETDSearch', always_commit=True)
solr.ping()
print("Current working directory:", os.getcwd())

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    print("search route")
    query = request.args.get('q')
    print(query)

    # Field specific query
    results = solr.search("description:" + query, **{"rows": 100000})  # To get all results (up to 100000)
    print("Saw {0} result(s).".format(len(results)))
    for result in results:
        print("Title:", result['title'])
        print("Identifier:", result['identifier'])
        print("Description:", result['description'])

        pass


    # results_for_template = [{'title': result['title'], 'identifier': result['identifier'], 'description': result['description']} for result in results]

    return render_template('results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)