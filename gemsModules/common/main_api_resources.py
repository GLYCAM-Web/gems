#!/usr/bin/env python3
from email.message import EmailMessage
import mimetypes
from typing import Any, List
from pydantic import BaseModel, Field
from pathlib import Path
import urllib.request

from gemsModules.common.main_api_notices import Notices

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class MimeEncodableResourceMixin:
    """Mixin for Resource mime encoding, coupled with yet separated from Resource for API clarity."""

    @property
    def is_mime_encoded(self):
        """Check if the payload is MIME encoded by GEMS."""
        # check
        if "is_mime_encoded" in self.options and self.options["is_mime_encoded"]:
            return True

        return False

    def try_decode_mime(self, data):
        """If the payload is MIME encoded by GEMS or at all, try to decode it."""
        if self.is_mime_encoded or data.startswith(b"Content-Type:"):
            msg = EmailMessage()
            msg.set_content(data)
            return msg.get_payload(decode=True)
        else:
            return data

    @classmethod
    def from_payload(cls, data, resource_format):
        return cls(
            locationType="Payload",
            resourceFormat=resource_format,
            payload=data,
        )

    @classmethod
    def from_payload_with_mime_encapsulation(
        cls, data, resource_format, mime_type=None, filename=None
    ):
        msg = EmailMessage()

        maintype, subtype = (
            mime_type.split("/") if mime_type else ("application", "octet-stream")
        )
        msg.set_content(
            data,
            maintype=maintype,
            subtype=subtype,
        )

        encoded_content = msg.as_string()

        obj = cls.from_payload(encoded_content, resource_format)

        obj.options = {"is_mime_encoded": True}
        if filename is not None:
            obj.options["filename"] = filename

        return obj

    @classmethod
    def from_path(cls, resource_path, resource_format, encapulate_mime=False):
        if encapulate_mime:
            return cls.from_payload_with_mime_encapsulation(
                str(open(resource_path, "rb").read()),
                resource_format,
                mimetypes.guess_type(resource_path)[0],
                Path(resource_path).name,
            )
        else:
            return cls(
                locationType="filesystem-path-unix",
                resourceFormat=resource_format,
                payload=str(resource_path),
            )


class Resource(BaseModel, MimeEncodableResourceMixin):
    """Information describing a resource containing data.

    Payload could be a filesystem path or a download URL or an HTML header or
    anything else that could hold a file.  Location is intended to be a type, not the payload.

    The location type could be 'String' or 'Payload', in which case,
    the payload would be the actual info and not the address of the info.

    What to do with the info will vary a lot depending on the needs of the service.
    """

    typename: str = Field(
        "Unset",
        alias="type",
        title="Resource type",
        description="The name of the type of Resource.",
    )
    locationType: str = Field(  # Literal['URL', 'File', 'Payload']
        None,
        title="Location Type",
        description="Supported locations will vary with each Entity.",
    )
    resourceFormat: str = Field(
        None,
        title="Resource Format",
        description="Supported formats will vary with each Entity.",
    )
    payload: Any = Field(
        None,
        description="The thing that is described by the location and format.",
    )
    notices: Notices = Field(
        None,
        description="Notices associated with this resource",
    )
    options: dict[str, str] = Field(
        default_factory=dict,
        description="Key-value pairs that are specific to each entity, service, etc",
    )

    @property
    def filename(self):
        """Filename from options or File payload."""
        if self.locationType == "filesystem-path-unix":
            return Path(self.payload).name
        elif "filename" in self.options:
            return self.options["filename"]
        else:
            raise ValueError(
                "No filename specified, please set it with options['filename'] or use a File payload."
            )

    def copy_to(self, parent_dir: Path, filename=None):
        """Copy this resource to the destination directory."""
        filename = filename or self.filename

        if isinstance(parent_dir, str):
            path = Path(parent_dir) / filename

        with open(path, "wb") as f:
            f.write(self._get_payload())

        log.debug(f"Copying resource {self} to {path}...")

    def _handle_file(self):
        with open(self.payload, "rb") as f:
            file = f.read()

        return self.try_decode_mime(file)

    def _handle_payload(self):
        return self.try_decode_mime(self.payload.encode("utf-8"))

    def _handle_url(self):
        with urllib.request.urlopen(self.payload) as f:
            return self.try_decode_mime(f.read())

    def _get_payload(self):
        """Return the data from the payload.

        - Can override and call super from subclass to extend location types.
        - Can also override the handlers to extend functionality.
        """
        if self.locationType == "filesystem-path-unix" or self.locationType == "File":
            payload = self._handle_file()
        elif self.locationType == "Payload" or self.locationType == "String":
            payload = self._handle_payload()
        elif self.locationType == "URL":
            payload = self._handle_url()
        else:
            raise ValueError(f"Unknown locationType {self.locationType}")

        return payload

    def convert_resource_format(self, resourceFormat: str):
        pass

    def convert_location_type(self, locationType: str):
        pass

    @classmethod
    def from_resource(cls, other):
        pass


class Resources(BaseModel):
    __root__: list[Resource] = Field(default_factory=list)

    def add_resource(self, resource: Resource):
        self.__root__.append(resource)

    def type_is_present(self, typename: str):
        if not self.__root__:
            return False

        for resource in self.__root__:
            if resource.typename == typename:
                return True

        return False

    def get_resource_by_type(self, typename: str) -> list[Resource]:
        if self.__root__ is None or self.__root__ == []:
            return []

        return [resource for resource in self.__root__ if resource.typename == typename]

    def __getitem__(self, key):
        return self.__root__[key]

    def __setitem__(self, key, value):
        self.__root__[key] = value

    def __len__(self):
        if self.__root__ is None:
            return 0
        return len(self.__root__)

    def __iter__(self):
        return iter(self.__root__)

    def __repr__(self):
        return f"{self.__root__}"


def generateSchema():
    print(Resource.schema_json(indent=2))


def generateJson():
    thisResource = Resource()
    thisResource.notices.addCommonParserNotice()
    print(thisResource.json(indent=2))
