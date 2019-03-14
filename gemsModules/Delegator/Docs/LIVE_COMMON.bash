#!/bin/bash
####
####  File:  LIVE_SITES/LIVE_COMMON.bash
####
####  Purpose:  Hold settings that are common to the live sites
####            (DEV, ACTUAL).
####
####  NOTES:
####
####     1.  This file is not meant to work alone.
####         It should be called from a script that
####         has also called other files that contain
####         definitions used herein.
####
####     2.  The live settings file should be called from
####         that script before calling this one.
####
####  Currently, the files that call this script are:
####
####         Setup_LIVE.bash
####         Slurm/initial_LIVE_start_command.bash
####

##############################################
###  SWARM General settings
##############################################
##
## Hosts in the Swarm
SWARM_HOSTS=(
  'coleridge'
  'howard'
  'parker'
)
##
## Directory locations
##  THIS_HOME='/website/DOCKER/GLYCAM'
##  ENV_BASE=$(pwd)  ## "V_1" dirctory
##  PREFIX='actual'
##  WEBDIR='GLYCAM'

## User info
WEB_USER_ID=53183:1003
WEB_UID=53183
WEB_GID=1003



##############################################
###  Volumes settings
##############################################
##
## Names of Common Named Volumes
##
NamedVolumeCommand='docker volume create --driver local '
NSFVolumeCommonOptions=' --opt type=nfs --opt o=addr=192.168.1.9,rw '
VolumeBaseNames=(
    website
    batchcompute
    conf
    gemsgmml
    grpc
    misc
    optslurm
    virtuosodata
    mariadbdata
    logs
    userdata
    workinghome
    graftinggems
    graftingsitedeps
    glycoproteinbuilder
)
declare -A VolumeTypes=(
    [website]='named'
    [batchcompute]='named'
    [conf]='named'
    [gemsgmml]='named'
    [grpc]='named'
    [misc]='named'
    [optslurm]='named'
    [virtuosodata]='named'
    [mariadbdata]='both'
    [logs]='nfs'
    [userdata]='nfs'
    [workinghome]='nfs'
    [graftinggems]='named'
    [graftingsitedeps]='named'
    [glycoproteinbuilder]='named'
)
declare -A VolumeServiceLocation=(
    [website]='/website'
    [batchcompute]='/programs/Batch_Compute'
    [conf]='/programs/conf'
    [gemsgmml]='/programs/gems'
    [grpc]='/programs/GRPC'
    [misc]='/programs/gw_misc'
    [optslurm]='/opt/slurm'
    [virtuosodata]='/data'
    [mariadbdata]='/var/lib/mysql'
    [logs]='/programs/logs'
    [userdata]='/website/userdata'
    [workinghome]='/home/working'
    [graftinggems]='/programs/temp/gems_grafting_2016Jan27'
    [graftingsitedeps]='/programs/site_deps/Grafting'
    [glycoproteinbuilder]='/programs/GlycoProteinBuilder'
)
declare -A VolumeHostCommonLocation=(
    [website]='Docker-controlled'
    [batchcompute]='Docker-controlled'
    [conf]='Docker-controlled'
    [gemsgmml]='Docker-controlled'
    [grpc]='Docker-controlled'
    [misc]='Docker-controlled'
    [optslurm]='Docker-controlled'
    [virtuosodata]='Docker-controlled'
    [mariadbdata]="${THIS_HOME}/Database"
    [logs]="${THIS_HOME}/logs"
    [userdata]="${THIS_HOME}/userdata"
    [workinghome]="${THIS_HOME}/working"
    [graftinggems]='Docker-controlled'
    [graftingsitedeps]='Docker-controlled'
    [glycoproteinbuilder]='Docker-controlled'
)
declare -A VolumeHostLocation=(
    [website]="${ENV_BASE}/Main_Web_Stack/website"
    [batchcompute]="${ENV_BASE}/Web_Programs/Batch_Compute"
    [conf]="${ENV_BASE}/Main_Web_Stack/programs_conf"
    [gemsgmml]="${ENV_BASE}/Web_Programs/gems"
    [grpc]="${ENV_BASE}/Web_Programs/GRPC"
    [misc]="${ENV_BASE}/Main_Web_Stack/programs_gw_misc"
    [optslurm]="${LIVE_DIR}/slurm_conf_logs_${PREFIX}"
    [virtuosodata]="${ENV_BASE}/Virtuoso/Info/db"
    [mariadbdata]="/volume1/website/DOCKER/${WEBDIR}/Database/dbdata"
    [logs]="/volume1/website/DOCKER/${WEBDIR}/logs"
    [userdata]="/volume1/website/DOCKER/${WEBDIR}/userdata"
    [workinghome]="/volume1/website/DOCKER/${WEBDIR}/working"
    [graftinggems]="${ENV_BASE}/Web_Programs/grafting_gems"
    [graftingsitedeps]="${ENV_BASE}/Web_Programs/grafting_site_deps"
    [glycoproteinbuilder]="${ENV_BASE}/Web_Programs/GlycoProteinBuilder"
)
declare -A VolumeNamesInUse=(
    [website]='NOT_SET'
    [batchcompute]='NOT_SET'
    [conf]='NOT_SET'
    [gemsgmml]='NOT_SET'
    [grpc]='NOT_SET'
    [misc]='NOT_SET'
    [optslurm]='NOT_SET'
    [virtuosodata]='NOT_SET'
    [mariadbdata]='NOT_SET'
    [logs]='NOT_SET'
    [userdata]='NOT_SET'
    [workinghome]='NOT_SET'
    [graftinggems]='NOT_SET'
    [graftingsitedeps]='NOT_SET'
    [glycoproteinbuilder]='NOT_SET'
)

##############################################
###  Service Volumes
##############################################
## If you are looking for the array used by the SLURM services.
## Look in the Slurm_Common.bash file. They are declared that
## file because they are used by another variable in the file.
LIVE_MARIADB_VOLUME_NAME_BASES=(
	mariadbdata
)

LIVE_VIRTUOSO_VOLUME_NAME_BASES=(
    virtuosodata
)

LIVE_MAIN_VOLUME_NAME_BASES=(
    website
    logs
    userdata
    workinghome
    batchcompute
    conf
    gemsgmml
    grpc
    misc
    graftinggems
    graftingsitedeps
    glycoproteinbuilder
)
