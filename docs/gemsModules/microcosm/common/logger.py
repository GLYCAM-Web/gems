### This is an attempt to not have to put these lines at the top
### of every file.  It works, but it ain't pretty.

from gemsModules.docs.microcosm.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)
