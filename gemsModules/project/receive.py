import gemsModules
from gemsModules.common.transaction import *
from gemsModules.common import utils
from datetime import datetime
from project import *
import settings
import  os, logging, sys, uuid

debugLevel=logging.DEBUG
logging.basicConfig(level=debugLevel, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def startProject(thisTransaction : Transaction):
    logging.info("\nstartProject() was called.")
    input_dir = "path/from/frontend"
    output_dir = settings.output_data_root + "tools/" + str(uuid.uuid4())
    requesting_agent = "Command line"
    myProject = Project(input_dir=input_dir, output_dir=output_dir, requesting_agent=requesting_agent)
    logging.debug("myProject: " + str(myProject))
    # project.input_dir =
    # project.output_dir = settings.output_data_root + "tools/" + str(uuid.uuid4())
    # project.requesting_agent = "Command line"
    # logging.debug("project: " + str(project))

def main():
    logging.info("project/receive.py main() was called.")
    logging.debug("number of args: " + str(len(sys.argv)))
    if len(sys.argv) == 2:
        jsonObjectString = utils.JSON_From_Command_Line(sys.argv)
        logging.debug("jsonObjectString: " + jsonObjectString)
        thisTransaction=Transaction(jsonObjectString)
        startProject(thisTransaction)
    else:
        logging.error("You must provide a path to a json request file.")

if __name__ == "__main__":
    main()
