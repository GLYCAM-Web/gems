#!/usr/bin/env python3
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


def getVersionsFileInfo(versionsFilePath : str):
    log.info("getVersionsFileInfo was called.\n")
    import re, os
    thisDict = {
            'site_version' :  "",
            'site_branch' : "",
            'gems_version' :  "",
            'gems_branch' :  "",
            'md_utils_version' :  "",
            'md_utils_branch' :  "",
            'gmml_version' :  "",
            'gmml_branch' :  "",
            'gp_version' :  "",
            'gp_branch' :  "",
            'site_mode' :  "",
            'site_host_name' :  ""
            }
    if not os.path.exists(versionsFilePath) :
        log.error("versionsFilePath does not exist.  Cannot set versions info.")
        return thisDict
    with open(versionsFilePath) as file:
        content = file.read()
    lines = content.split("\n")
    for line in lines:
        # Get rid of any whitespace or newline
        trimmed_line = re.sub(r'\s+', '', line)
        theKeyVal =  trimmed_line.split("=")
        if len(theKeyVal) > 1 :
            theKey=theKeyVal[0]
            theVal=theKeyVal[1].strip('"')
            lowerKey = theKey.lower()
            if 'git_commit_hash' in  lowerKey :
                jsonKey=lowerKey.replace('git_commit_hash', 'version')
            elif 'git_branch' in lowerKey :
                jsonKey=lowerKey.replace('git_branch', 'branch')
            else:
                jsonKey=lowerKey
            thisDict[jsonKey]=theVal
    log.debug("the versions dictionary is : " + str(thisDict))
    return thisDict

