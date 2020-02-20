#!/bin/bash
/programs/GlycoproteinBuilder/bin/gp_builder \
    /website/userdata/tools/gp/git-ignore-me_userdata/29515072-369e-4047-967a-6bf8fdbad525/ \
    > /website/userdata/tools/gp/git-ignore-me_userdata/29515072-369e-4047-967a-6bf8fdbad525/gp.log

GPPATH="/programs/GlycoproteinBuilder/bin/gp_builder"
WorkDir="/website/userdata/tools/gp/git-ignore-me_userdata/29515072-369e-4047-967a-6bf8fdbad525/"

COMMAND="${GPPATH} ${WorkDir} > ${WorkDir}gp.log"

eval ${COMMAND}
