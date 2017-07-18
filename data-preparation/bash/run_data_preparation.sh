#!/usr/bin/env bash

# Copyright 2017 by Idiap Research Institute, http://www.idiap.ch
#
# Author(s):
#   Bastian Schnell, 03.07.17

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

usage() {
cat <<- EOF
    usage: $PROGNAME [OPTIONS] <path/inputFile> <path/outputDir> <path/regexFile>

    Bash wrapper function which calls ./../python/run_data_preparation.py.
    All arguments and flags are set in that function call.

    OPTIONS:
        -l --language <id>=0      language of input file (0=unk, 1=fr, 2=ge, 3=en, 4=it)
        -f --filter               filter sentences
        -F --filter2ndStage       enable filter sentence checking for second stage
        -n --rmpunct              remove punctuation
        -p --vbpunct              verbalize punctuation
        -s --rawseg               do not segment sentences with NLTK
        -m --lm                   prepare for lm modeling
        -d --debug                enable debug output
        -h                        show this help


    Examples:
        Normalize an english text file.
        $PROGNAME -s -m -l 3 $PWD/text.txt $PWD/text_norm.txt $PWD/regex.txt
        Automatically detect language and produce output for all implemented languages.
        $PROGNAME -f -m $PWD/text.txt $PWD/text_norm.txt $PWD/regex.txt
EOF
}


[[ "$TRACE" ]] && set -o xtrace # Enables xtrace option for this file if already enabled.
# set -o xtrace # Prints every command before running it, same as "set -x".
# set -o errexit # Exit when a command fails, same as "set -e".
#                # Use "|| true" for those who are allowed to fail.
#                # Disable (set +e) this mode if you want to know a nonzero return value.
# set -o pipefail # Catch mysqldump fails.
# set -o nounset # Exit when using undeclared variables, same as "set -u".
# set -o noclobber # Prevents the bash shell from overwriting files, but you can force it with ">|".

readonly PROGNAME=$(basename $0)
readonly PROGDIR=$(readlink -m $(dirname $0))
readonly ARGS="$@"

# source does not work with -u option, so disable it temporarily.
# set +u
# source bash_logging.sh
# set -u
log()
{
    echo -e >&2 "$@"
}

# This function can be used to selectively enable/disable debugging.
# Use with the set command to debug sections of the script.
DEBUG()
{
    # Check to see if the enable debugging variable is set
    if [ -n "${DEBUG_ENABLE+x}" ]
    then
        # Run whatever command/option/argument combo that was
        # passed to our DEBUG function.
        $@
    fi
}

# Clean up is called by the trap at any stop/exit of the script.
cleanup()
{
    # Cleanup code.
    rm -rf "$TMP"
}
# Die should be called when an error occurs with a HELPFUL error message.
die () {
    log "ERROR" "$@"
    exit 1
}


# Set magic variables for current file & directory (upper-case).
readonly TMP=$(mktemp -d)

# The main function of this file.
main()
{
    # Force execution of cleanup at the end.
    trap cleanup EXIT INT TERM HUP

    # Read flags and optional parameters.
    local language='' # (0=unk, 1=fr, 2=ge, 3=en, 4=it, default=[0])
    local filterSentences=''
    local filterSentences2ndStage=''
    local removePunctuation=''
    local verbalizePunctuation=''
    local rawSeg=''
    local lmModeling=''
    local debug=''
    while getopts ":hl:fFnpsmd-:" flag; do # If a character is followed by a colon (e.g. f:), that option is expected to have an argument.
        case "${flag}" in
            -) case "${OPTARG}" in
                   language) language="${!OPTIND}"; OPTIND=$(( $OPTIND + 1 )) ;;
                   filter) filterSentences='true' ;;
                   filter2ndStage) filterSentences2ndStage='true' ;;
                   rmpunct) removePunctuation='true' ;;
                   vbpunct) verbalizePunctuation='true' ;;
                   rawseg) rawSeg='true' ;;
                   lm) lmModeling='true' ;;
                   debug) debug='true' ;;
                   *) die "Invalid option: --${OPTARG}" ;;
               esac;;
            h) usage; exit ;;
            l) language="${OPTARG}" ;;
            f) filterSentences='true' ;;
            F) filterSentences2ndStage='true' ;;
            n) removePunctuation='true' ;;
            p) verbalizePunctuation='true' ;;
            s) rawSeg='true' ;;
            m) lmModeling='true' ;;
            d) debug='true' ;;
            \?) die "Invalid option: -$OPTARG" ;;
            :)  die "Option -$OPTARG requires an argument." ;;
        esac
    done
    shift $(($OPTIND - 1)) # Skip the already processed arguments.

    # Read arguments.
    local expectedArgs=3 # Always use "local" for local variables, global variables are evil anyway.
    if [[ $# != "${expectedArgs}" ]]; then
        usage # Function call.
        die "Wrong number of parameters, expected ${expectedArgs} but got $#."
    fi
    # Read parameters, use default values (:-) to work with -u option.
    local inputFile=${1:-}
    local outputFile=${2:-}
    local regexFile=${3:-}

    ########################
    # Main functionality of this file.
    #

    py_cmd="${PROGDIR}/../python/run_data_preparation.py -i ${inputFile} -o ${TMP} -r ${regexFile}"
    if [ -n "${language}" ]; then
        py_cmd+=" -l ${language}"
    fi
    if [ -n "${filterSentences}" ]; then
        py_cmd+=" -f"
    fi
    if [ -n "${filterSentences2ndStage}" ]; then
        py_cmd+=" --filter2ndStage"
    fi
    if [ -n "${removePunctuation}" ]; then
        py_cmd+=" -n"
    fi
    if [ -n "${verbalizePunctuation}" ]; then
        py_cmd+=" -p"
    fi
    if [ -n "${rawSeg}" ]; then
        py_cmd+=" -s"
    fi
    if [ -n "${lmModeling}" ]; then
        py_cmd+=" -m"
    fi
    if [ -n "${debug}" ]; then
        py_cmd+=" -d"
    fi

    # echo "${inputFile}"
    # echo "${outputFile}"

    # Call the python function which does the work.
    eval "python ${py_cmd}"

    # Handle output files.
    #ls "${TMP}"/sentences_*
    if [ -n "${language}" ]; then
        # If language was set, only one file was created so use it as output.
        cp --force "${TMP}"/sentences_* "${outputFile}"
        log "INFO" "Normalized file in ${outputFile}.\n"
    else
        # Otherwise copy all created files to the output directory.
        local outDir="$(dirname ${outputFile})"
        cp --force "${TMP}"/sentences_* "${outDir}"
        log "INFO" "No language was specified. Normalized files for all supported languages in ${outDir}.\n"
    fi
}

# Call the main function, provide all parameters.
main "$@"
