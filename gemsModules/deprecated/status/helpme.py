#!/usr/bin/env python3

usageText="""
The status module provides status reports for entities in GEMS.
Reports can be generated for all entities, or for specific entities.
"""
basicHelpText="""
Make a request from the status entity. If you don't specify a service,
a report is generated for all enities. Request the generateReport service
if you wish to specify a single entity's status report. Name the entity
in the input's payload to specify an entity.
"""
moreHelpText="""
Here is an example request:
"""
