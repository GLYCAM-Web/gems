# Design Documentation for the Resource

This module provides allows Entities and Services to make use of artifacts without needing special
code for obtaining, sharing, and inspecting the artifacts.

This Module has no parent Module.

*Important Note*

This module should move to the Systemoperations module. It needs to be available to the Configuration
module without that module needing to import anything from Common.

---

## Purpose and Goals

A Resource Object should contain the necessary information for an artifact to be transparently located, 
obtained, transferred, inspected, deleted, etc.

For example, a PDB file might be obtained from any one of the following sources, and possibly others:

- A directory in the local filesystem
- Via a URL call to rcsb.org
- Embedded in a JSON object

Code that needs the PDB file should not need to be concerned with the initial location of the file. The
Resource infrastructure abstracts the location.

Similarly, the Resource infrastructure should abstract inspection of the artifact. In fact, a Resource
object should do this automatically, but at the appropriate time. For example, if the resource is a link
available for download, the Resource object should, at minimum, confirm that the URL is properly formatted.
Once the artifact is usable, it should be inspected to ensure it is of the proper type. At the very least,
the Resource object should ensure that text files are text, audio file are audio, etc. 

Further inspection of very specific file formats (such as PDB) can be part of the Resource object. However,
scientific files are often modified slightly for various reasons. It is permissible if the scientific code
prefers to perform its own deep evaluation. 

This abstraction capability envisions a time when clusters might exist on remote cloud services or when
artifacts should be housed in an object store rather than in a filesystem path. Use of the resource means
that the scientific code has no need, now or in the future, to be concerned about the systems-level
manipulation of its artifacts.

## Interface with the JSON API

Numerous conveniences have been added to the various APIs. For example, in the Sequence entity, the sequence
to be modeled or inspected can be specified as a 'payload' in the JSON. We do not want to remove these 
conveniences. In these cases, it is up to the Entity to package the conveniences into a Resource early in
the API processing. 

Many sample JSON inputs - many of which are still valid - can be found here:

`gemsModules/deprecated/delegator/test_in`

