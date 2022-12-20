#!/usr/bin/env python3

usageText="""
Create a project for your gemsModule.
"""
basicHelpText="""
Pass a transaction to receive.py. Project module will update the transaction
with project details, and create any necessary directories for output.
"""
moreHelpText="""
gemsProject is concerned with project details of concern to gems, not Django.
Therefore, it is useful to clarify which project you are speaking about.
When no clarification is made, project is assumed to be the Django project.
gemsProjects may be created in cases where the website is not used.
gemsProjects are objects in memory, though they write their data to a log.
"""
