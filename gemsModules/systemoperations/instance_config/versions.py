# GEMS note: We should not modify production configuration files automatically. It should only run in a DevEnv.
import datetime
import json
import os
from pathlib import Path
import shutil
from typing import Dict


class DateReversioner:
    """A class to version a json file based on a timestamp."""

    def __init__(
        self, active_config: Path, new_config: Path = None, new_config_data: Dict = None
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

    def set_new_config_data(self, config: Dict):
        # Because this doesn't use a path, unset it.
        self._new_version = None
        self._new_version_data = config

    def set_new_config_path(self, config_path: Path):
        # Likewise, unset data so we can regenerate it from the path.
        self._new_version_data = None
        self._new_version = config_path

    @property
    def is_outdated(self) -> bool:
        """Return True if the file_to_version is older than the new_version."""
        if not self.file_to_version.exists():
            return True

        if "date" not in self.new_version:
            raise RuntimeError("Template file does not have a date, cannot update.")

        if "date" not in self.old_version:
            # if no date is found, lets update to a versioned file
            return True
        else:
            # compare old and new version dates
            old_date = datetime.datetime.strptime(
                self.old_version["date"], "%Y-%m-%dT%H:%M:%S.%f"
            ).date()
            new_date = datetime.datetime.strptime(
                self.new_version["date"], "%Y-%m-%dT%H:%M:%S.%f"
            ).date()
            return new_date > old_date

    def update(self) -> bool:
        """Update the file_to_version with the current date."""
        needs_update = (
            self.is_outdated
            or os.getenv("GEMS_FORCE_INSTANCE_RECONFIGURATION") == "True"
        )

        if needs_update:
            # Backup the file_to_version.
            if self.file_to_version.exists():
                backup_file = self.file_to_version.with_suffix(
                    f".json.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-git-ignore-me.bak"
                )
                shutil.copyfile(self.file_to_version, backup_file)

            # copy the new version in place of the file_to_version
            with self.file_to_version.open("w") as f:
                json.dump(self.new_version, f, indent=2)
                print(f"\nUpdated {self.file_to_version} with new date.")

            # retain only the last 3
            backup_files = sorted(
                self.file_to_version.parent.glob(
                    f"{self.file_to_version.stem}.json.*-git-ignore-me.bak"
                )
            )
            for backup in backup_files[:-3]:
                backup.unlink()
        else:
            print(f"\nNo update needed for {self.file_to_version}.")

        return needs_update
