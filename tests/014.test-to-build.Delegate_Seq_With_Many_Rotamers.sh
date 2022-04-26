#!/usr/bin/env bash

### 
### This test needs to be written
### 

## Purpose:  Ensure that conformerIDs that are UUIDs are treated properly.

## Resources in place:
#
#      inputs/014.input-needs-work.json  
#
#		This file needs to be pared down
#		- remove all refs to a specific IP address/server/filesystem path
#		- remove anything else that isn't needed
#
#		It contains a sequence with many rotamers.  
#		There are so many that the conformerLabels are all longer than a UUID.
#		So, the conformerID is always a UUID.
#
#		To minimize testing load, only two conformers are selected for build.

## Things to be tested:
#
#	- Only the requested structures get built plus one initial default for the options page.
#	
#	- UUIDs are self-consistent within all request and response objects
#
#	- The structures themselves are properly built.
#		- This will require generation of good reference structures.
#		- The structures that are currently built look ok, 
#			but this needs explicit confirmation.

## Why is this test not written?  
#	
#	Because the bug it is needed for was only discovered after a fix for
#	a different bug.  I gotta get that one pushed up so this one can be fixed.
#
#  An aside:  this is relevant to something that goes wrong between GEMS and
#	the website. It cannot be tested or fixed only in gems.
