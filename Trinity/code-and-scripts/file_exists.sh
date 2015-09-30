#!/bin/bash
#
# This tells how many arguments to the script. If just the script is
# given on the command line, $# is 0 (zero).
#
#echo "$#"
#
# This script takes one argument, the file to check for existence.
# Make sure there is an argument passed.
#
the_file="$1"
#
# Make sure the usage is correct
#
#if [ "$the_file" == "" ]
if [ $# -ne 1 ]
then
  echo "ERROR - Usage: ./file_exists.sh <file-to-check-for-existence>"
  echo "ERROR: <file-to-check-for-existence> is required"
  exit 1
fi
#
# If we have the argument, check to make sure the file exists.
#
# If this is run sending output to a log file, just grep the log
# file for "does NOT exist" to see if there were any failures.
#
if [ ! -e ${the_file} ]
then
  echo "ERROR: ${the_file} does NOT exist on `hostname`"
  exit 1
fi

echo "SUCCESS: ${the_file} exists on `hostname`"
exit 0
