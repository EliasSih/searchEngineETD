curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"identifier",
     "type":"text_general",
     "stored":true }
}' http://localhost:8983/solr/#/ETDSearch/schema

