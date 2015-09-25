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
DATAPREPARATIONDIR="$configDir/../data-preparation/"

###########################
#Data preparation
#
RUNTASKSCRIPT=$DATAPREPARATIONDIR/python/run_data_preparation_task.py
RUNDOCUMENTSCRIPT=$DATAPREPARATIONDIR/python/run_data_preparation.py
