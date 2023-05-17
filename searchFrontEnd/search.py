from flask import Flask, render_template, request
import pysolr
import os
import openai

app = Flask(__name__)

solr = pysolr.Solr('http://localhost:8983/solr/testCollection', always_commit=True)
solr.ping()
print("Current working directory:", os.getcwd())


def removeZeros(dic):
    #Helper function for getFacets
    hold = {x:y for x,y in dic.items() if y!=0}
    return hold

def dicttolist(dic):
    resultList = list(dic.keys())
    resultList.sort()
    return resultList

def getFactes(query, facetOn):
    print("in facets:", query)
    params = {
    'facet': 'on',
    'facet.field': facetOn,
    'rows': '0', #Make 0 to return no results and only fields
    "q.op" : "AND",
    }
    results = solr.search(query, **params)
    facetArray = results.facets["facet_fields"][facetOn]
    facetDict = {}
    i = 0 #a counter
    while i < len(facetArray)-1:
        facetDict[facetArray[i]] = facetArray[i+1]
        i = i+2
    return dicttolist(removeZeros(facetDict))

def chatGPT(prompt):
    messages = [{"role": "system", "content": "You are a helpful search engine."}]

    query = {}
    query['role'] = 'user'
    query['content'] = prompt
    messages.append(query)

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    try:
        result = response['choices'][0]['message']['content']
    except:
        result = "Please try another query, if problem persist, try again later."
    return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/basicSearch')
def basicSearch():
    print("search route")
    query = request.args.get('q')
    params = {
    'rows': '100000', 
    "q.op" : "AND",
    }
    results = solr.search(query, **params)
    print("Saw {0} result(s).".format(len(results)))
    authors = getFactes(query, "creator_str")
    years = getFactes(query, "date")
    return render_template('results.html', query=query, results=results, authors = authors, years = years)

@app.route('/search')
def search():
    print("search route")
    query = request.args.get('q')
    originalQuery = query
    #if request.args.get('subject') != "":
    #    sub = request.args.get('subject')
    #    query = query + " subject:" + sub
    #else:
    #    sub = None
    if request.args.get('author') != "Any":
        aut = request.args.get('author')
        query = query + " creator:" + aut
    else:
        aut = None
    if request.args.get('yearfrom') < request.args.get('yearto'):
        yearfrom = request.args.get('yearfrom')
        yearto = request.args.get('yearto')
        if request.args.get('yearfrom') == "1":
            pass
        else:
        #Year error handling 
            query = query + " date:" + "[{0} TO {1}]".format(request.args.get('yearfrom'),request.args.get('yearto'))
    else:
        yearfrom = None
        yearto = None
    
    print(query)
    #The query
    params = {
    'rows': '100000', #Make 0 to return no results and only fields
    "q.op" : "AND",
    }
    results = solr.search(query, **params)  # To get all results (up to 100000)
    #results = solr.search(query, **params)
    print("Saw {0} result(s).".format(len(results)))
    
    authors = getFactes(query, "creator_str")
    years = getFactes(query, "date")

    #request ai powered response from openai
    resultGPT = chatGPT(originalQuery)
    print(resultGPT)

    # results_for_template = [{'title': result['title'], 'identifier': result['identifier'], 'description': result['description']} for result in results]
    return render_template('results.html', query=originalQuery, results=results, authors = authors, years = years, aut = aut, yearfrom = yearfrom, yearto=yearto, resultGPT=resultGPT)

if __name__ == '__main__':
    app.run(debug=True)
    