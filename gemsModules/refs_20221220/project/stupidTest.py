from pydantic import BaseModel, Field, ValidationError
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class Project(BaseModel):
	title : str = ""
	project_type : str = ""


class CbProject(Project):
	sequence : str = ""


if __name__ == "__main__":
	log.info("Testing stupid.")

	try:
		cb = CbProject(title="Stupid second title.", project_type="cb", sequence="DGalpa1-OH")
		log.debug("cbProject: " + str(cb))
	except Exception as error:
		log.error("There was a problem validating the Project: " + str(error))