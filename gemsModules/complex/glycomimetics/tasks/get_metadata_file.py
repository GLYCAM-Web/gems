from gemsModules.systemoperations.environment_ops import get_gems_path

GEMSHOME = get_gems_path()


def execute() -> List:
    """Return a file from External/GM_Utils/metadata"""
    metadata_dir = GEMSHOME + "/External/GM_Utils/metadata"
    return [str(file) for file in metadata_dir.iterdir() if file.is_file()]
