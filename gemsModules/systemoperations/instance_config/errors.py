from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class InstanceConfigError(Exception):
    pass


class InstanceConfigNotFoundError(FileNotFoundError):
    """Raised when the $GEMSHOME/instance_config.json file is not found.

    This file is required for GEMS to route requests appropriately. Please copy the example file
    from $GEMSHOME/instance_config.json.example.

    """

    def __init__(self, msg=None, *args, **kwargs):
        if msg is None:
            msg = (
                "Warning! Did you configure your GEMS instance?\n"
                "\tThe GEMS instance_config.json was not found in $GEMSHOME.\n\n"
                "\tPlease copy the example file:\n"
                "\t\t`cp $GEMSHOME/instance_config.json.example $GEMSHOME/instance_config.json`\n\n"
                "\tOtherwise, some GEMS requests may not function as expected.\n"
                f"\t$GEMSHOME is {os.getenv('GEMSHOME', '$GEMSHOME')}."
            )

        log.error(msg)

        super().__init__(msg, *args, **kwargs)


__all__ = ["InstanceConfigError", "InstanceConfigNotFoundError"]
