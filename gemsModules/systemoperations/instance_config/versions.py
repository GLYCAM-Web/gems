# GEMS note: We should not modify production configuration files automatically. It should only run in a DevEnv.
import datetime
import json
from pathlib import Path
import shutil


class DateReversioner:
    """A class to version a json file based on a timestamp."""

    def __init__(
        self, active_config: Path, new_config: Path = None, new_config_data: dict = None
    ):
        self.file_to_version = active_config
        self._old_version_data = None

        self._new_version = new_config
        self._new_version_data = new_config_data

    @property
    def old_version(self):
        """Return the old version data."""
        if self.file_to_version.exists() and self._old_version_data is None:
            with open(self.file_to_version) as f:
                self._old_version_data = json.load(f)

        return self._old_version_data

    @property
    def new_version(self):
        """Return the new version data."""
        if self._new_version_data is None and self._new_version is not None:
            with open(self._new_version) as f:
                self._new_version_data = json.load(f)

        return self._new_version_data

    def update(self):
        """Update the file_to_version with the current date."""

        needs_update = False
        if self.file_to_version.exists():
            if "date" not in self.new_version:
                raise RuntimeError("Template file does not have a date, cannot update.")

            if "date" not in self.old_version:
                # if no date is found, lets update to a versioned file
                needs_update = True
            else:
                # check the template file for a date
                # if the template is newer, lets update to a versioned file
                old_date = datetime.datetime.fromisoformat(self.old_version["date"])
                new_date = datetime.datetime.fromisoformat(self.new_version["date"])
                if new_date > old_date:
                    needs_update = True
        else:
            needs_update = True

        if needs_update:
            # Backup the file_to_version.
            if self.file_to_version.exists():
                backup_file = self.file_to_version.with_suffix(
                    f".json.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-git-ignore-me.bak"
                )
                shutil.copyfile(self.file_to_version, backup_file)

            # copy the example file in place of the file_to_version
            with self.file_to_version.open("w") as f:
                json.dump(self.new_version, f, indent=2)
                print(f"Updated {self.file_to_version} with new date.")
        else:
            print(f"No update needed for {self.file_to_version}.")

        return needs_update
