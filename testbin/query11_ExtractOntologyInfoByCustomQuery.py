### Sample usage from testbin directory: python query11.py YOUR_QUERY_FILE [OUTPUT_FORMAT] &> [YOUR-OUTPUT-FILE]
### This query searches the ontology data based on the given sparql query. ExtractOntologyInfoByCustomQuery(custom_query_file, output_type)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()

if len(sys.argv) == 3:
	temp.ExtractOntologyInfoByCustomQuery(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 2:
	temp.ExtractOntologyInfoByCustomQuery(sys.argv[1])
else:
	print('A query file as an input argument is missing')
	print('Sample usage: python query11_ExtractOntologyInfoByCustomQuery.py [YOUR_QUERY_FILE]')



