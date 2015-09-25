#!/bin/bash

#
# Copyright 2015 by Idiap Research Institute, http://www.idiap.ch
#
# Author(s):
#   Alexandre Nanchen, May 2015

# This file is part of asrt.

# asrt is free software: you can redistribute it and/or modify
# it under the terms of the BSD 3-Clause License as published by
# the Open Source Initiative.

# asrt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# BSD 3-Clause License for more details.

# You should have received a copy of the BSD 3-Clause License
# along with asrt. If not, see <http://opensource.org/licenses/>.

usage="\n
 This script extract multilingual sentences from
 the 'Research.pdf' document.

 It filters, prepares and classifies sentences.

 Filtering is performed with the following criteria:

 1. Min, max number of characters per sentence
 2. Min words count per sentence
 3. Max number of groups of digits
 4. Custom regular expressions

 Classification is performed using NLTK and a naive
 bayes classifier.
"

die () {
    echo -e >&2 "$@"
    exit 1
}

cwd=`pwd`
scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

################
#Environment
#
source $scriptDir/../../config/AsrtConfig.sh

TEMPDIR=$cwd/temp
[ -d $TEMPDIR ] || mkdir $TEMPDIR

PDF=$(readlink -m "$scriptDir/../resources/Research.pdf")
TARGETFOLDER=$TEMPDIR/target-research
OUTPUTFOLDER=$TEMPDIR/output-research
REGEXFILE=$scriptDir/../resources/regex.csv

################
#Main program
#
[ -d $OUTPUTFOLDER ] || mkdir $OUTPUTFOLDER

echo "Generating target folder"
[ -d $TARGETFOLDER ] || mkdir -p $TARGETFOLDER
echo "  --> Generating data.olist"

#Format is unique id;absolute path of the document
echo "research-01;$PDF" > $TARGETFOLDER/data.olist
echo "  --> Generating data.omap"

#Format is unique id;language
#Language is unique and can be unknown for automatic detection
#or anything else to specify that the pdf document is in
#a given language
echo "research-01;unknown" > $TARGETFOLDER/data.omap

echo "Extracting sentences from $(basename $PDF)"
eval "$RUNTASKSCRIPT -t $TARGETFOLDER -o $OUTPUTFOLDER -r $REGEXFILE -f -m" || die "An error has occurred!"

echo "Results files are into $OUTPUTFOLDER/ImportDocumentTask-1/output"
pushd $OUTPUTFOLDER/ImportDocumentTask-1/output &>/dev/null
ls -l sentences*
popd &>/dev/null
