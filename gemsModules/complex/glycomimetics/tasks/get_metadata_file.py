from pathlib import Path
from gemsModules.systemoperations.environment_ops import get_gems_path


GEMSHOME = get_gems_path()


def execute() -> list[Path]:
    """Return a file from External/GM_Utils/metadata"""
    metadata_dir = GEMSHOME + "/External/GM_Utils/metadata"
    return [Path(file) for file in metadata_dir.iterdir() if file.is_file()]
