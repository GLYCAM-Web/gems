import os, sys, importlib.util
import gemsModules
from gemsModules.common.services import *
from gemsModules.common.transaction import *
from gemsModules.project.projectUtil import *
import gemsModules.mmservice.settings as mmSettings
import traceback

##  If this module is receiving a request, then there should be almost no
##  setup required other than whatever is specific to the modeling engine.
##
##  For example, if the modeling engine is amber, then it's ok to have to
##  specify a force field file for building prmtop/inpcrd.  And, it's ok
##  to need to generate an input-control file.  But, there should be no
##  building of coordinates, etc., which aren't really an amber thing.
##  (unless you write modules for using tleap to build, etc.....)
##

"""
The receive() method receives a transaction, and checks for the requested service.
"""
def receive(thisTransaction):
    print("mmservice receive() was called.")
    request = thisTransaction.request_dict

    if 'services' not in thisTransaction.request_dict['entity'].keys():
        doDefaultService(thisTransaction)
    else:
        services = getTypesFromList(thisTransaction.request_dict['entity']['services'])

        for requestedService in services:
            print("requestedService: " + str(requestedService))
            ##Can we detect if this project has already been started?
            ##  If so, check the status of a job that exists, and start jobs that don't.

            if requestedService not in mmSettings.serviceModules.keys():
                print("The requested service is not recognized.")
                print("services: " + str(mmSettings.serviceModules.keys()))
                common.settings.appendCommonParserNotice(thisTransaction,'ServiceNotKnownToEntity', requestedService)
            elif requestedService == "Amber":
                print("Amber service requested.")

                startProject(thisTransaction)
            else:
                print("The requested service is still in development.")
                print("serviceModules.keys(): " + str(mmSettings.serviceModules.keys()))
                pass


def doDefaultService(thisTransaction):
    print("doDefaultService() was called.")
    # .setup.check(thisTransaction)
    # .amber.md.generate.plainMD(thisTransaction)
    # batchcompute.check(thisTransaction)
    # batchcompute.generatescript(thisTransaction)
    # batchcompute.submit(thisTransaction)

def main():
     ## TODO:  Make this look more like the main in delegator's receive.py
    GemsPath = os.environ.get('GEMSHOME')
    if GemsPath == None:
        this_dir, this_filename = os.path.split(__file__)
        print("""

        GEMSHOME environment variable is not set.

        Set it using somthing like:

          BASH:  export GEMSHOME=/path/to/gems
          SH:    setenv GEMSHOME /path/to/gems
        """)

    #print("length of argv: " + str(len(sys.argv)))
    if len(sys.argv) > 1:
        #print("looking for the input filename.")
        if os.path.isfile(sys.argv[1]):
            inputFile = sys.argv[1]
        else:
            #print("got an arg that is not a filename: " + sys.argv[1])
            inputFile = GemsPath + "/gemsModules/delegator/test_in/amberMdRequest.json"
    else:
        #print("no argv was offered.")
        inputFile = GemsPath + "/gemsModules/delegator/test_in/amberMdRequest.json"

    #print("using the default inputFile: " + inputFile)
    #print(os.listdir("../../delegator/test_in/"))

    with open(inputFile, 'r') as file:
        jsonObjectString = file.read().replace('\n', '')
        #print("jsonObjectString: " + str(jsonObjectString))

    #Create transaction, then pass that to receive
    thisTransaction = Transaction(jsonObjectString)

    try:
        parseInput(thisTransaction)
    except Exception as error:
        print("Error parsing input.")
        print("Error type: " + str(type(error)))
        print(traceback.format_exc())

    receive(thisTransaction)

    responseObjectString = thisTransaction.outgoing_string
    return responseObjectString

if __name__ == "__main__":
    main()

