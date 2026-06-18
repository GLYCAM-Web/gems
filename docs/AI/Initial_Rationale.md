# Rationale For Code Generation By AI
This document explains why using AI is the only realistic way to proceed for this project at this time.

Due to budget constraints, the only person available to change this code is Lachele Foley, who is also
the author of this document. This is a mostly personal account.

The infrastructure for GLYCAM-Web is complicated. The systems(1) make it especially complicated. In fact,
those components are often harder to manage than the underlying science.

The purpose of the GEMS code is to serve as a translation layer between the relatively friendly inputs for 
the users and the very complicated software and systems that provide the scientific products. Because of 
this, GEMS itself is partly software and partly systems. That is, any person coding in GEMS needs at least
a rudimentary understanding of many aspects of the systems and software.

The required knowlege includes:
- Programming languages:
  - Python
    - Prominent packages include Pydantic and gRPC
  - BASH
  - C++
- JSON
- gRPC
- HPC clusters, especially schedulers such as Slurm
- Systems administration 
  - ports and services
  - shared filesystems

Ideally, the programmer needs very little scientific knowledge. The primary goal of GEMS's design is that
the scientist can specify the 'back end' interface to the scientific software, and the rest can be written
more-or-less automatically. This capability is mostly complete.

There is currently a single person doing all that work. The same person also tends the physical machinery
and all the other computing infrastructure (Warewulf, Slurm, Docker, Traefik, etc.) and occasionally the
scientific software. Happily, a lot of the scientific software is now handled by some other folks.

One person cannot do all that, and there is no hope for generating documentation of the system. Perhaps one 
person and AI can get a lot of it done.

The current plan is for the person to work on design specifications. These designs will be committed with 
the code. AI will implement them and generate tests. The person will verify behaviors. AI will probably 
generate user-level documentation as well.

See the Log directory if you want to learn more about the process. The logs will be unstructured notes about
the process, but they should contain insights for those who are interested.

(1) In this doc, 'systems' refers to:
    - All the hardware and 
    - All the software that is not directly involved in the business logic of the website.
