from gemsModules.status.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

log.debug("The logging tester posts this message in the DEBUG log.")
log.error("The logging tester posts this message in the ERROR log.")
log.info("The logging tester posts this message in the INFO log.")

