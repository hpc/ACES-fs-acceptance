#!/bin/sh

# run_file_exists.sh
# 
#
# Created by brettk on 12/12/12.
# Copyright 2012 __MyCompanyName__. All rights reserved.


#MSUB -S /bin/bash
#MSUB -l nodes=<num-nodes>
#MSUB -l walltime=00:10:00
#MSUB -V
#MSUB -o run_file_exists.out
#MSUB -j oe

aprun -n <num-nodes> -N 1 file_exists.sh $HOME/file_existence_test.tst
