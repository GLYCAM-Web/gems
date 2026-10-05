#!/usr/bin/env python3
"""System Operations Resource API.

Provides clean, structured Resource and Resources models for artifact and configuration
management across GEMS services and execution environments.

In GEMS terminology:
- payload: The generic container entry in JSON or memory holding the artifact data
  or reference (e.g., sequence string "DManpa1-OH", file path string "/path/to/file.pdb",
  URL, dict, or number).
- locationType: Specifies how payload is interpreted ('Payload' for inline content/sequences,
  'filesystem-path-unix', 'URL', 'File').
- resourceRole: Describes the function or purpose of a Resource (e.g., "Antibody", "Ligand").
- resourceFormat: Describes the data format (e.g., "PDB", "CondensedIUPAC").
"""

import email
from email.message import EmailMessage
import mimetypes
from pathlib import Path
import tempfile
from typing import Any, Dict, List, Literal, Optional, Union
import urllib.request

try:
    from pydantic.v1 import BaseModel, Field, PrivateAttr
except ImportError:
    from pydantic import BaseModel, Field, PrivateAttr

from gemsModules.common.main_api_notices import Notices
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class MimeEncodableResourceMixin:
    """Mixin for Resource MIME encoding/decoding."""

    @property
    def is_mime_encoded(self) -> bool:
        """Check if the payload is MIME encoded by GEMS."""
        if self.options is not None and "is_mime_encoded" in self.options:
            return self.options["is_mime_encoded"] in ["True", "true", True]
        return False

    def try_decode_mime(self, data: Any) -> Any:
        """If the payload is MIME encoded by GEMS, decode it."""
        if self.is_mime_encoded or (isinstance(data, bytes) and data.startswith(b"Content-Type:")):
            msg = email.parser.BytesParser().parsebytes(data if isinstance(data, bytes) else data.encode("utf-8"))
            return msg.get_payload(decode=True)
        return data


class Resource(BaseModel, MimeEncodableResourceMixin):
    """Information describing a GEMS artifact or resource.

    Payload is the generic entry containing data, a file path, sequence string, URL, or dict.
    LocationType specifies how the payload is interpreted.
    """

    typename: str = Field(
        "Unset",
        alias="type",
        title="Resource type",
        description="The name of the type of Resource.",
    )
    locationType: Optional[Literal["Payload", "URL", "File", "filesystem-path-unix"]] = Field(
        None,
        title="Location Type",
        description="Supported location type indicating how payload is stored or referenced.",
    )
    resourceFormat: Optional[str] = Field(
        None,
        title="Resource Format",
        description="Data format of the resource payload (e.g., PDB, AMBER-7-prmtop).",
    )
    resourceRole: Optional[str] = Field(
        None,
        title="Resource Role",
        description="Role indicating the function or purpose of a Resource (e.g., Antibody, Ligand).",
    )
    payload: Any = Field(
        None,
        description="The artifact value, reference path, URL, or data payload.",
    )
    options: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Key-value pair options specific to entity, host mounts, credentials, or metadata.",
    )
    notices: Optional[Notices] = Field(
        default_factory=Notices,
        description="Notices associated with this resource.",
    )

    class Config:
        allow_population_by_field_name = True

    @property
    def filename(self) -> Optional[str]:
        """Return filename from options or filesystem payload if present."""
        if self.locationType in ["filesystem-path-unix", "File"] and isinstance(self.payload, (str, Path)):
            return Path(self.payload).name
        if self.options and "filename" in self.options:
            return str(self.options["filename"])
        if self.resourceRole:
            return self.resourceRole
        return None

    def get_payload(self, decode: bool = True) -> Any:
        """Extract and return the raw payload content.

        Decodes binary file contents to text by default unless decode=False is passed.
        """
        if self.locationType in ["filesystem-path-unix", "File"]:
            if self.payload is None:
                return None
            path = Path(self.payload)
            if not path.is_file():
                log.warning(f"File path {path} does not exist when reading payload.")
                return str(self.payload)
            is_binary = self.options and self.options.get("binary")
            mode = "rb" if (is_binary and not decode) else "r"
            try:
                with open(path, mode, errors="replace") as f:
                    data = f.read()
                return self.try_decode_mime(data)
            except UnicodeDecodeError:
                with open(path, "rb") as f:
                    return self.try_decode_mime(f.read())
        elif self.locationType == "URL":
            if not self.payload:
                return None
            with urllib.request.urlopen(str(self.payload)) as f:
                data = f.read()
            decoded = self.try_decode_mime(data)
            if decode and isinstance(decoded, bytes):
                return decoded.decode("utf-8", errors="replace")
            return decoded
        else:
            # LocationType == "Payload" or inline content
            if isinstance(self.payload, bytes) and decode:
                return self.payload.decode("utf-8", errors="replace")
            return self.payload

    def get_path(self) -> Path:
        """Return a pathlib.Path pointing to the resource file on disk.

        If the resource is a filesystem path, returns that path directly.
        If the locationType is 'Payload' or 'URL', writes/caches payload to a temporary file.
        """
        if self.locationType in ["filesystem-path-unix", "File"] and self.payload is not None:
            return Path(self.payload)

        # For inline Payload or URL, write content to a temporary file
        content = self.get_payload()
        suffix = f".{self.resourceFormat.lower()}" if self.resourceFormat else ".txt"
        fname = self.filename or f"resource_{id(self)}{suffix}"
        temp_dir = Path(tempfile.gettempdir()) / "gems_resources"
        temp_dir.mkdir(parents=True, exist_ok=True)
        dest_path = temp_dir / fname

        mode = "wb" if isinstance(content, bytes) else "w"
        with open(dest_path, mode) as f:
            if isinstance(content, (dict, list)):
                import json
                json.dump(content, f, indent=2)
            else:
                f.write(content if content is not None else "")
        return dest_path

    def get_stream(self):
        """Return an open readable binary file stream for large payload reading."""
        path = self.get_path()
        return open(path, "rb")

    def resolve_path(self, host_name: Optional[str] = None) -> Path:
        """Resolve local vs remote filesystem path considering host options."""
        if self.options and "local_path" in self.options:
            return Path(self.options["local_path"])
        if self.locationType in ["filesystem-path-unix", "File"] and self.payload:
            return Path(self.payload)
        return self.get_path()

    def copy_to(self, destination: Union[str, Path, "Resource"], filename: Optional[str] = None) -> "Resource":
        """Copy or write this resource's payload to a destination path or target Resource."""
        content = self.get_payload()
        target_filename = filename or self.filename or "artifact.dat"

        if isinstance(destination, Resource):
            destination.payload = content
            if destination.options is None:
                destination.options = {}
            destination.options["filename"] = target_filename
            return destination

        dest_path = Path(destination)
        if dest_path.is_dir():
            dest_file = dest_path / target_filename
        else:
            dest_file = dest_path

        dest_file.parent.mkdir(parents=True, exist_ok=True)
        mode = "wb" if isinstance(content, bytes) else "w"
        with open(dest_file, mode) as f:
            if isinstance(content, (dict, list)):
                import json
                json.dump(content, f, indent=2)
            else:
                f.write(content if content is not None else "")

        return Resource(
            typename=self.typename,
            locationType="filesystem-path-unix",
            resourceFormat=self.resourceFormat,
            resourceRole=self.resourceRole,
            payload=str(dest_file.resolve()),
            options={"filename": dest_file.name, "binary": isinstance(content, bytes)},
        )

    def copy_from(self, source: Union["Resource", str, Path]) -> "Resource":
        """Ingest payload from a source Resource or path file into this Resource."""
        if isinstance(source, Resource):
            self.typename = source.typename
            self.locationType = source.locationType
            self.resourceFormat = source.resourceFormat
            self.resourceRole = source.resourceRole
            self.payload = source.payload
            if source.options:
                self.options = dict(source.options)
            if source.notices:
                self.notices = source.notices
        else:
            source_path = Path(source)
            self.locationType = "filesystem-path-unix"
            self.payload = str(source_path.resolve())
            if self.options is None:
                self.options = {}
            self.options["filename"] = source_path.name
        return self

    @classmethod
    def from_payload(
        cls,
        payload: Any,
        role: Optional[str] = None,
        format: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> "Resource":
        """Create a Resource with locationType='Payload' packaging the provided payload directly."""
        return cls(
            locationType="Payload",
            resourceRole=role,
            resourceFormat=format,
            payload=payload,
            options=options or {},
        )

    @classmethod
    def from_file(
        cls,
        path: Union[str, Path],
        role: Optional[str] = None,
        format: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> "Resource":
        """Create a Resource with locationType='filesystem-path-unix' referencing a file path."""
        file_path = Path(path)
        opts = options or {}
        if "filename" not in opts:
            opts["filename"] = file_path.name
        return cls(
            locationType="filesystem-path-unix",
            resourceRole=role,
            resourceFormat=format,
            payload=str(file_path.resolve()),
            options=opts,
        )

    @classmethod
    def from_url(
        cls,
        url: str,
        role: Optional[str] = None,
        format: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> "Resource":
        """Create a Resource with locationType='URL' referencing a URL."""
        return cls(
            locationType="URL",
            resourceRole=role,
            resourceFormat=format,
            payload=url,
            options=options or {},
        )


class Resources(BaseModel):
    """Container list for multiple Resource objects."""

    __root__: List[Resource] = Field(default_factory=list)

    def add_resource(self, resource: Resource, metadata_only: bool = False):
        if metadata_only:
            resource = resource.copy(deep=True)
            resource.payload = None
        self.__root__.append(resource)

    def type_is_present(self, typename: str) -> bool:
        return any(r.typename == typename for r in self.__root__)

    def get_resource_by_type(self, typename: str) -> List[Resource]:
        return [r for r in self.__root__ if r.typename == typename]

    def get_resource_by_role(self, role: str) -> Optional[Resource]:
        for r in self.__root__:
            if r.resourceRole == role:
                return r
        return None

    def get_resources_by_role(self, role: str) -> List[Resource]:
        return [r for r in self.__root__ if r.resourceRole == role]

    def append(self, resource: Resource):
        if not isinstance(resource, Resource):
            raise TypeError("Only Resource instances can be appended.")
        self.__root__.append(resource)

    def extend(self, resources: Union[List[Resource], "Resources"]):
        if isinstance(resources, Resources):
            resources = resources.__root__
        if not all(isinstance(r, Resource) for r in resources):
            raise TypeError("Only a list of Resource instances can be extended.")
        self.__root__.extend(resources)

    def remove_resource_by_role(self, role: str):
        self.__root__ = [r for r in self.__root__ if r.resourceRole != role]

    def remove(self, resource: Resource):
        self.__root__.remove(resource)

    def pop(self, index: int = -1) -> Resource:
        return self.__root__.pop(index)

    def __getitem__(self, key):
        return self.__root__[key]

    def __setitem__(self, key, value):
        self.__root__[key] = value

    def __len__(self) -> int:
        return len(self.__root__)

    def __iter__(self):
        return iter(self.__root__)

    def __repr__(self):
        return f"{self.__root__}"
