This document describes the overall architecture that was chosen for GEMS.  The purpose of the Architecture is to specify how the code will implement the requirements and desirables as outlined in the [[Design Notes]].

The architecture described herein is used in GEMS.  Other architectures could fulfill the design specs, but at this point, changing would be very difficult.

## Overall role

This diagram illustrates the role that GEMS plays with respect to GLYCAM-Wem (glycam.org) and with respect to [[GMML(https://github.com/GLYCAM-Web/gmml).]].

![[SOFTWARE - Overview.png]]

In the [[Design Notes]], a more complete list of user-stakeholders is given.  Here, though, the only user specified is GLYCAM-Web.  GEMS is an interface that serves GLYCAM-Web.  GEMS is served by GMML and by many applications, internal and external.  It is not shown in this diagram, but GEMS can be its own user (conversely, it can serve itself).

## Architectural elements relevant to each design principle

These design principles are given in the [[Design Notes]].  These principles might not be listed in the order they appear in the document.

### GEMS should be usable by scientists who do molecular modeling 

Much of this requirement is the domain of the code.  That is, the variable and function names must be comprehensible to scientists.  However, the organization of GEMS's capabilities inhabits the domain of architecture (and design).




### Normal interface to GEMS should proceed by a simple, unchanging contract

We do not want the website to need to know Python.  We do not want the website to have to interact directly with GEMS code.  