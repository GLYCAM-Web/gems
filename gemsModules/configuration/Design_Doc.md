# Design Documentation for the Configuration gemsModule

The main work of this module is the production and parsing of the file `instance_config.json`.

This Entity has no child Entities and no parent Entity. It does not inherit from Common or from any other
GEMS modules. 

The instance configuration is often called 'instance config' or simply 'IC'.

---

## Purpose and Goals

Important background: 

GEMS is designed to provide communication between computers. If configured properly, a GEMS instance on one 
computer, _ComputerA_ should be able to send requests to a GEMS instance on another computer, _ComputerB_.

This allows, for example, a computer providing a website to communicate with another computer that is the
head node for a computing cluster. It can also allow a person to submit remote jobs from a local machine.

The GEMS instances communicate via gRPC. See `GEMSHOME/docs/GEMS_to_GEMS_Communication.md` for details. The 
use of gRPC comes with advantages beyond mere communication.

The Configuration module provides a way to generate a and query a database of available GEMS instances,
including the local GEMS. This database, called an _Instance Configuration_, contains information regarding
the capabilities of the available GEMS instances and how they can be contacted.

---

## Available Services

This module does not use the JSON API that most modules use. It exists to serve the other modules in their
work. It reads and writes the IC files and provides information from them to the modules.

Notably, this module should generally not be used by the normal JSON-API-oriented modules designed for 
interaction with users. 

Modules that interact directly with this module:
- Project : for setting directory paths and such
- Batch Compute : for interfacing computers with batch computing resources
- Network Connections : for sending the requests from one GEMS to another
- Delegator : for recording the roles of various GEMS instances

