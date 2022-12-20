Right now the query entity is for GlyFinder.  It is replacing the direct call from the site to GMML.  At the minimum for GlyFinder to search, it needs the QueryOntology (gmml/src/MolecularModeling/Ontology/gf_query.cc:69) function working.

Django used to get and process GET data (glycamweb/gf/views.py:85-151) and send it to gmml.  Two queries are sent on a search:
(glycamweb/gf/views.py:153) Sends a query that returns only the results for the first page (25 by default)
(glycamweb/gf/views.py:272) Sends a query for all of the results and then uses that to return how many results matched the search (glycamweb/gf/views.py:273-283)

Additional queries are sent when the More button is clicked (glycamweb/gf/views.py:58-64), and when downloading results (glycamweb/gf/views.py:298-379)

All of the queries return a curl request string, which needs to be run by the query entity, and will return a JSON to Django which is set up to handle it already.

gf/views.py also needs to have a call to the query entity.  This will send a json object with all of the needed variables to choose and run a query.

The number of arguments for the Ontology query and the More query have changed; I'm hoping to have the correct function call in views.py at least before I push

Some line numbers may be off because of added comments; sorry!
