[33mcommit 77c29915d70aa6692c037ca06cd898cfd79a34fb[m[33m ([m[1;36mHEAD -> [m[1;32mShaylin[m[33m)[m
Author: Shaylin-UCT <chtsha042@myuct.ac.za>
Date:   Tue May 16 12:41:48 2023 +0200

    Improved Extraction

[1mdiff --git a/MetaData/XMLExtract.py b/MetaData/XMLExtract.py[m
[1mindex 19c5fce..666ce9e 100644[m
[1m--- a/MetaData/XMLExtract.py[m
[1m+++ b/MetaData/XMLExtract.py[m
[36m@@ -1,4 +1,5 @@[m
 import xml.etree.ElementTree as ET[m
[32m+[m[32mimport re[m
 [m
 def parse_xml(xml_file):[m
     # Parse XML with ElementTree[m
[36m@@ -102,9 +103,14 @@[m [mdef Extract(xml_file, outputFile):[m
         [m
         #date.text = item["date"][m
         if item["date"] is None:[m
[32m+[m[32m            date.text = "0000"[m
[32m+[m[32m        elif item["date"] == "<yyyy>" or item["date"] == "n/a":[m
             date.text = "1111"[m
         else:[m
[31m-            date.text = item["date"][m
[32m+[m[32m            date.text = re.search(r"[1-3][0-9]{3}", item["date"]).group(0)[m
[32m+[m[32m            print(item["title"],date.text)[m
[32m+[m[32m            #print(re.search(r"[1-3][0-9]{3}", item["date"]).group(0))[m
[32m+[m
 [m
         description.text = item["description"][m
         #date.text = item["date"][m
[36m@@ -135,7 +141,7 @@[m [mdef Extract(xml_file, outputFile):[m
 total = 0[m
 import glob[m
 txtfiles = [][m
[31m-for file in glob.glob("Metadata\\aaaaaad*.xml"):[m
[32m+[m[32mfor file in glob.glob("Metadata\\aaaaaadb.xml"):[m
 #for file in ["Metadata\\aaaaaaaa.xml"]:[m
     txtfiles.append(file)[m
     ls = file.split("\\")[m
[1mdiff --git a/searchFrontEnd/search.py b/searchFrontEnd/search.py[m
[1mindex a17e618..85b1da9 100644[m
[1m--- a/searchFrontEnd/search.py[m
[1m+++ b/searchFrontEnd/search.py[m
[36m@@ -59,11 +59,11 @@[m [mdef search():[m
     print("search route")[m
     query = request.args.get('q')[m
     originalQuery = query[m
[31m-    if request.args.get('subject') != "":[m
[31m-        sub = request.args.get('subject')[m
[31m-        query = query + " subject:" + sub[m
[31m-    else:[m
[31m-        sub = None[m
[32m+[m[32m    #if request.args.get('subject') != "":[m[41m[m
[32m+[m[32m    #    sub = request.args.get('subject')[m[41m[m
[32m+[m[32m    #    query = query + " subject:" + sub[m[41m[m
[32m+[m[32m    #else:[m[41m[m
[32m+[m[32m    #    sub = None[m[41m[m
     if request.args.get('author') != "Any":[m
         aut = request.args.get('author')[m
         query = query + " creator:" + aut[m
[36m@@ -95,7 +95,7 @@[m [mdef search():[m
     years = getFactes(query, "date")[m
 [m
     # results_for_template = [{'title': result['title'], 'identifier': result['identifier'], 'description': result['description']} for result in results][m
[31m-    return render_template('results.html', query=originalQuery, results=results, authors = authors, years = years, sub = sub, aut = aut, yearfrom = yearfrom, yearto=yearto)[m
[32m+[m[32m    return render_template('results.html', query=originalQuery, results=results, authors = authors, years = years, aut = aut, yearfrom = yearfrom, yearto=yearto)[m[41m[m
 [m
 if __name__ == '__main__':[m
     app.run(debug=True)[m
