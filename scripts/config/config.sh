#!/bin/bash

#
# Copyright 2015 by Idiap Research Institute, http://www.idiap.ch
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Alexandre Nanchen, May 2015
#

cwd=`pwd`
configDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

###########################
#General
#
ASRTROOT="$configDir/../../"
TEMPDIR="$ASRTROOT/temp"
DATAPREPARATIONDIR="$ASRTROOT/scripts/data-preparation/"

###########################
#Libraries
#
LIBBASE=$ASRTROOT/lib

###########################
#Data preparation
#
RUNTASKSCRIPT=$DATAPREPARATIONDIR/python/run_data_preparation_task.py
RUNDOCUMENTSCRIPT=$DATAPREPARATIONDIR/python/run_data_preparation.py
