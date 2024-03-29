## Who I am
WhoIAm='Query'

status = "In development"
moduleStatusDetail = "Can make queries via GlyFinder serviceModule."

servicesStatus = [
    {
        "service" : "glyFinder",
        "status" : "In development.",
        "statusDetail" : "The glyfinder service is maturing. Can make queries. Adding finishing touches."
    }
]

subEntities = [
    {
        "subEntity" : "Graph"
    }
]


## Module names for services that this entity/module can perform.
## These should not include the Common Services.
ServiceModule = {
        'GlyFinder' : 'glyFinder'
        }

# def main():
#     import importlib, os, sys
#     if importlib.util.find_spec("gemsModules") is None:
#         this_dir, this_filename = os.path.split(__file__)
#         sys.path.append(this_dir + "/../")
#         if importlib.util.find_spec("common") is None:
#             print("Something went horribly wrong.  No clue what to do.")
#             return
#         else:
#             from common import utils
#     else:
#         from gemsModules.common import utils
#     data=utils.JSON_From_Command_Line(sys.argv)
#
#
#
#     # If I can get the code below to work it should be a breeze to make the other queries.
#
#
#     # Code from gems level detect sugar test
#     # import gems/gmml stuff
#     sys.path.append(GemsPath)
#     import gmml
#
#
#     #code from gf/views.py
#     temp = gmml_lib.Assembly()
#     curl = temp.QueryOntology(searchType, temp_oligo_sequence, resolution_min, resolution_max, b_factor_min, b_factor_max, oligo_b_factor_min, oligo_b_factor_max, isError, isWarning, isComment, page, resultsPerPage, sortBy, VIRT_DATABASE, "json")
#     proc = subprocess.Popen(curl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     (out, err) = proc.communicate()
#     out = str(out.decode('utf-8'))
#     startIndex = out.index('{')
#     out = out[startIndex:]
#     jsonObj = json.loads(out)
#
#     #return the json object to views.py
#     return jsonObj


if __name__ == "__main__":
  main()
