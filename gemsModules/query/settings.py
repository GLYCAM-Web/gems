## Who I am
WhoIAm='Query'

## Module names for services that this entity/module can perform.
## These should not include the Common Services.
ServiceModule = {
        'GlyFinder' : 'glyfinder'
        }

def main():
    import importlib, os, sys
    if importlib.util.find_spec("gemsModules") is None:
        this_dir, this_filename = os.path.split(__file__)
        sys.path.append(this_dir + "/../")
        if importlib.util.find_spec("common") is None:
            print("Something went horribly wrong.  No clue what to do.")
            sys.exit(1)
        else:
            from common import utils
    else:
        from gemsModules.common import utils
    utils.investigate_gems_setup(sys.argv)



    # If I can get the code below to work it should be a breeze to make the other queries.

    
    # Code from gems level detect sugar test
    # import gems/gmml stuff
    sys.path.append(GemsPath)
    import gmml


    #code from gf/views.py
    temp = gmml_lib.Assembly()
    curl = temp.QueryOntology(searchType, temp_oligo_sequence, resolution_min, resolution_max, b_factor_min, b_factor_max, oligo_b_factor_min, oligo_b_factor_max, isError, isWarning, isComment, page, resultsPerPage, sortBy, VIRT_DATABASE, "json")
    proc = subprocess.Popen(curl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out, err) = proc.communicate()
    out = str(out.decode('utf-8'))
    startIndex = out.index('{')
    out = out[startIndex:]
    jsonObj = json.loads(out)

    #return the json object to views.py
    return jsonObj


if __name__ == "__main__":
  main()
