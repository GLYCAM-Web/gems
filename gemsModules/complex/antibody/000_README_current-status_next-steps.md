# Current Status and Next Steps - Antibody Docking

2026-03-20

## Pre-Existing Challenges

### That Are Being Addressed Now

#### Significant Hard-Coding
Some hardcoding was necessary when the module was first generated because the infrastructure for better practices was 
not yet in place. In fact, the hard-coding was somewhat purposeful because it served as a notice to future coders that 
the module had been written very early, and in haste, and would need significant changes.

#### Limited Provenance Trails for Remote Hosts
This service, as with others, requires execution on remote hosts (e.g., remote HPC clusters). The website must adapt 
and respond to changes in the identities, environments, and requirements of the remote hosts.  Infrastructure capable 
of recording and managing interactions with remote hosts had not been fully designed or implemented.  This affects all
of our services that interact with computing environments outside the development platform.

#### Deviations From Architecture
The existing code mostly tracked the intended architecture. But, there were exceptions. There were also unused files 
and methods whose utility was uncertain. 

#### No Support for Testing Workflow
The primary result of these challenges was the lack of a mechanism for testing services provided by or on remote hosts. 
Specifically, there was no way to isolate code being tested from code used by the live website.

### That Are Not Being Addressed Now

#### Integration Into Our Development Platform
The scientific code supporting this service is very old and relies on old technologies (compilers, libraries, etc.). 
For isolation of the old technologies from the execution host, the code is being run inside a Docker container. This
introduces challenges for integration into our (Docker-based) development platform. Solutions like Docker-in-Docker, 
Spack, code rewrites, etc., require significant effort that is outside the current scope. 

## Current Status 

All of the challenges listed as 'Being Addressed' have been addressed, though there is work to be done (noted below).
Any specific change to the code generally addresses more than one challenge. 

### Overall
At the moment, the code is inoperable. Many interacting changes must be completed simultaneously and are in progress.

### Significant Hard-Coding
Areas containing Hard-Coding have been annotated.  Most will be easy to correct once the infrastructure for managing 
interactions with remote hosts is complete. The needs of the rest will become clearer once the easy ones are addressed.

### Limited Provenance Trails for Remote Hosts
Significant design improvements have been made. These exist mostly within `gemsModules/configuration/main_api.py`. 
Specifically, it is now possible to isolate the requirements of the local and remote hosts. It is also possible to 
identify, choose among, and respond to, multiple remote hosts capable of providing the same service. Most importantly, 
the design facilitates preservation of provenance.

### Deviations From Architecture
Because the architecture was designed for our specific needs, the simplest thing to do is make changes that move the 
code closer to the architecture. This is happening as expected.

### No Support for Testing Workflow
The design, in the systems as well as in this specific software, has been updated to facilitate testing. Two main 
features are responsible for the improvements. One, inasmuch as possible, the support software (ours and others), is 
being decoupled from the website deployments. Where that is not realistic, the supporting software is coupled to the 
deployment (e.g., 'upset-utsi') rather than to the URL hosting the deployment (e.g., glycam.org vs test.glycam.org).

## Next Steps

Within the architecture(1), the place to start is almost always with the Tasks(2). Ensure that all the specific needs 
of the Tasks are reflected in the module's API and in the Instance Config. Modify API and IC as needed so that no
hard-coding is needed, even where remote filesystem structure is very different.

Once the API, IC and Tasks are aligned, update the Services and other aspects of the architecture as needed.

And, of course, ignore this advice when it is prudent to do so.

## Notes

(1) There are diagrams of the GEMS Architecture, and it deserves better documentation. Generally, I leave code design 
decisions to the coders, but because GEMS lies more in the systems domain than the software domain, I specify its form. 
The following repository contains my diagrams. They might be of little use to the untrained.
https://github.com/GLYCAM-Web/coArchi-GLYCAM-Web

(2) Capitalized words like this are specific parts of the architecture. In the code, they are often represented as 
folders. For example, the Tasks for this Service are in `gemsModules/complex/antibody/tasks`. The architecture is
complex, but the following gives an idea of how it works. Services are separated from Tasks. A Service such as 
Evaluate might require many tasks in common with the Build or Status Services. Tasks are generated from the workflow
of the scientist. Services help bridge scientific concerns with the needs of a website.
