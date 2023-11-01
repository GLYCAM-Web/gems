# GEMS note: We should not modify production configuration files automatically. It should only run in a DevEnv.
import datetime
import json
from pathlib import Path
import shutil


class DateReversioner:
    """A class to version a json file based on a timestamp."""

    def __init__(self, active_config: Path, example_config: Path):
        self.file_to_version = active_config
        self.example = example_config

    def update(self):
        """Update the file_to_version with the current date."""

        needs_update = False
        if self.file_to_version.exists():
            # could generalize
            with open(self.file_to_version) as f:
                j_data = json.load(f)
            with open(self.example) as f:
                tj_data = json.load(f)

            if "date" not in j_data:
                # if no date is found, lets update to a versioned file
                needs_update = True
            else:
                # check the template file for a date
                # if the template is newer, lets update to a versioned file
                if "date" in tj_data:
                    if j_data["date"] < tj_data["date"]:
                        needs_update = True
                else:
                    raise RuntimeError(
                        "Template file does not have a date, cannot update."
                    )

        if needs_update:
            # Backup the file_to_version.
            backup_file = self.file_to_version.with_suffix(
                f".{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
            )
            shutil.copyfile(self.file_to_version, backup_file)

            # copy the example file in place of the file_to_version
            shutil.copyfile(self.example, self.file_to_version)
            print(f"Updated {self.file_to_version} with new date.")
