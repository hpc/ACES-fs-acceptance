import os,sys,datetime,time,getpass
sys.path += [ './lib', '../lib' ]
import expr_mgmt

#
# A simple example of how this experiment management framework is used.  Edit
# to run parameter sweeps on the mpi job of your choice with or without msub.
# You need to edit mpi_options{} which is a dictionary of option flags mapping to
# arrays of options (e.g. "np" : [100, 200]).  You need to set the path to your
# mpi program.  You also need to edit program_options{} which is analogous to
# mpi_options{} and you need to edit program_arguments[] which is an array of
# arrays for the required arguments to your program.  mpi_options{} and
# program_options{} can be None.
#
# Here are a couple of ways to create python arrays:
# [ item, item ],
# range(1,32,2),
# "item item item".split().

#
# Sometimes you may want little helper Python variables.
#
user     = getpass.getuser()
home     = os.getenv( "HOME" )
mpi_host = os.getenv( "MY_MPI_HOST" )

#mpi_program = ( "/usr/projects/ioteam/trinitite/IOR/install/bin/ior" )
mpi_program = ( "/usr/projects/ioteam/trinity/Testing/IOR/install/bin/ior" )


# Specific to Cray Trinity Machiness
#program_arguments = ( "KNL" )
#program_arguments = ( "KNL+HASWELL" )
#program_arguments = ( "" )
#program_arguments = ( "HASWELL" )
#program_arguments = None

#
# The targets of IOR.
#
target_dirs = [ "/lustre/trscratch1/atorrez/nn","/lustre/trscratch2/atorrez/nn" ]

#
# Setup the MPI options you want to pass to the MPI launching program, for
# example, "mpirun" ("np") or "aprun" ("n").
#
mpi_options = {
#  "N"     : [ pe-count-per-node-1, ..., pe-count-per-node-a ],
#  "n"    : [ pe-count-1, ..., pe-count-b ],
#  "np"    : [ pe-count-1, ..., pe-count-c ],
  "n"    : [ 1728 ],
}

#
# IOR options
#
# In all cases, the options can be lists. The parsing program will generate
# IOR commands one at a time by picking the first element of each list.
# The next command will be generated by going to the next element of the next
# list that has multiple entries, etc.
#
# Of course, the "mpi_options" above are the first lists.
#

#
# Here's a typical example of how a code might do an N-1 strided restart dump:
#
#target_dirs = [ "/lustre/lscratch3", "/lustre/lscratch2" ]
# 
#  "a" : [ 'MPIIO' ],
#  "b" : [ '1m' ],
#  "C" : [ '' ],
#  "g" : [ '' ],
#  "o" : [ "%s/%s/ior_%s.out" % ( target_dirs[0], user, time.mktime( datetime.datetime.now().timetuple())) ],
#  "s" : [ '1k' ],
#  "t" : [ '1m' ],
#
# This will write 1G per process in 1M blocks for 1K strides. It will
# then read in the same pattern, but the parts read will be offset so
# that a process on the next node will read what the process on the
# prior node wrote so that no data is buffered in memory to read.
# It barriers between each phase of the I/O and writes its output to
# /lustre/lscratch3/$USER/ior.out.

#
# Here's a typical example of how a code might do an N-N restart dump:
#
#target_dirs = [ "/lustre/lscratch3", "/lustre/lscratch2" ]
# 
#  "a" : [ 'MPIIO' ],
#  "b" : [ '1g' ],
#  "C" : [ '' ],
#  "F" : [ '' ],
#  "g" : [ '' ],
#  "o" : [ "%s/%s/ior_%s.out" % ( target_dirs[0], user, time.mktime( datetime.datetime.now().timetuple())) ],
#  "t" : [ '1m' ],
#
# This will write 1G per process in 1M chunks for 1K times per file.
# It willthen read in the same pattern, but the parts read will be
# offset so that a process on the next node will read what the process
# on the prior node wrote so that no data is buffered in memory to read.
# It barriers between each phase of the I/O and writes its output to
# /lustre/lscratch3/$USER/ior.out.
#

program_options = {
#
# The "%s" substitutes the string argument in parentheses on the parameter line.
#
# datetime.date.today().isoformat(): Formats the current date as a string.
# datetime.datetime.now().isoformat(): Formats the current date and time as a string.
#
# The now().isoformat has colons (":") in it and doesn't work for filenames.
# Use this:
#
# time.mktime( datetime.datetime.now().timetuple()))
#
#
#
# The I/O API to use. Valid API options are POSIX, MPIIO, HDF5, and NCMPI
# The default is POSIX.
#
#  "a" : [ '<valid API option>' ],
  "a" : [ 'POSIX' ],
#
# A user reference number to include in the long summary
#
#  "A" : [ <an integer> ],
#
# The block size, number of contiguous bytes to write per task; e.g.,
# 8, 4k, 2m, 1g. The size in bytes of a contiguous chunk of data
# accessed by a single client. It is comprised of one or more transfers.
# The default is 1048576 (or 1m).
#
#  "b" : [ <integer block size> ],
  "b" : [ '925968105472' ],
#
# Whether or not to use O_DIRECT for POSIX, bypassing the I/O buffers.
#
#  "B" : [ '' ],
#
# Whether or not to use collective I/O.
#
#  "c" : [ '' ],
#
# Whether or not to make a task on a different node read the data written
# by the writer task. The default is not to do this, so you must use this
# option if you wish to ensure that this data is read by a task on another
# node, which will mean it is not read from an in-memory buffer, but from
# the storage device.
#
# That is, it reorders tasks by a constant node offset for writing/reading neighbor's
# data from different nodes. The constant node offset is 1 (one) by default, but
# can be changed with the -Q <node offset> parameter.
#
# USE THIS OR -Z OR NEITHER, BUT NOT BOTH!!!
#
  "C" : [ '' ],
#
# The number of seconds to delay between repetitions of a test when more
# than one repetition is being done. This is for statistical performance.
# The default is 0 (zero). NOTE: It does not delay before a check write or
# check read, when those flags are used.
#
#  "d" : [ <integer seconds> ],
#
# The number of seconds to write or read before stopping the test. The default
# is 0 (zero).
#
# NOTE: This is used for measuring the amount of data moved in a fixed time.
# After the barrier, each task starts its own timer, begins moving data, and
# stops moving data at a prearranged time. Instead of measuring the amount
# of timeto move a fixed amount of data, this option measure the amount of
# data moved in a fixed amount of time. The objective is to prevent tasks
# slow to complete from skewing the performance. Setting this to 0 (zero)
# unsets this option. This option is incompatible with data checking.
#
#  "D" : [ <integer seconds> ],
#
# Whether or not to perform an "fsync" call after a POSIX close for writes.
#
  "e" : [ '' ],
#
# Whether or not to use an existing test file. Do not remove the file before
# doing a write test. Default is to remove the file before doing a write test.
#
#  "E" : [ '' ],
#
# The script that has IOR commands in it to execute.
#
#  "f" : [ "<a string with the path and name of the script with IOR commands>" ],
#
# Whether or not the test is a file-per-proc (N-N) test. This accesses a single
# file for each process. The default is a single file is accessed by all
# processes. That is, the default is shared-file (N-1).
#
  "F" : [ '' ],
#
# Whether or not to use barriers between the open, write/read, and close parts
# of a test. Note: The test may also have several repetitions. The default is
# not to barrier.
#
  "g" : [ '' ],
#
# Set the value for the timestamp signature. The default is 0 (zero).
#
# NOTE: This is used to rerun tests with the exact data pattern by setting
# the data signature to contain a positive integer value as a time stamp
# that is written in the data file.
#
#  "G" : [ <integer> ],
#
# Whether or not to display the options and help on them.
#
#  "h" : [ '' ],
#
# Whether or not to show hints.
#
#  "H" : [ '' ],
#
# The integer number of times to repeat this I/O test. Multiple times gives
# statistical performance versus one-time performance. The default is 1 (one).
#
#  "i" : [ '<integer repetitions>' ],
  "i" : [ '1' ],
#
# Whether or not to use individual datasets. If this parameter is used then
# datasets are not shared by all processes. There is a note in the User Guide
# that this option is not working as of 14-Nov-2014.
#
#  "I" : [ '' ],
#
# Gives warning if any task is more than this number of seconds from the mean
# of all participating tasks. If so, the task is identified, its time (start,
# elapsed create, elapsed transfer, elapsed close, or end) is reported, as is
# the mean and standard deviation for all tasks.  The default for this is 0,
# which turns it off.  If set to a positive value, for example 3, any task not
# within 3 seconds of the mean displays its times.
#
#  "j" : [ <integer seconds> ],
#
# The HDF5 alignment in bytes; e.g., 8, 4k, 2m, 1g.
#
#  "J" : [ <integer HDF5 alignment> ],
#
# Whether or not to keep the test files when the test is done. Default is
# to remove files when test is done.
#
  "k" : [ '' ],
#
# Whether or not to keep files with errors in them after doing data-checking.
# Default is to remove the files with errors when the test is done.
#
#  "K" : [ '' ],
#
# Whether or not to use the file offset as a stored signature when writing
# a file. The default is not to do it. If you do it, it will affect
# performance measurements.
#
#  "l" : [ '' ],
#
# Whether or not to use -i (number of reps) for multiple file count.
# This means that multiple files for single-shared-file or file-per-process
# modes; e.g., each iteration creates a new file or files.
#
  "m" : [ '' ],
#
# How much memory to use on the node; e.g., 2g, 75%. This is used to simulate
# real application memory usage. It accepts a percentage of node memory; e.g.,
# 50% or 75% on machines that support sysconf( _SC_PHYS_PAGES) or a size in
# bytes; e.g., 8, 4k, 2m, 1g. The memory allocation will be split between
# the tasks that share the node.
#
#  "M" : [ <integer amount of memory to use on the node> ],
#
# Whether or not to use no fill in HDF5 file creation.
#
#  "n" : [ '' ],
#
# Number of tasks to use in the test. The default is 0 (zero), which means
# all tasks should be in the test.
#
#  "N" : [ <integer tasks> ],
#
# The full-path filename for the test. NOTE: with file-per-proc set, the
# tasks can round robin across multiple filenames; e.g.:
#
#   -o <filename1>@<filename2>@<filename3
#
#  "o" : [ <string full-path filename for test> ],
#
# Here's an example:
#  "o" : [ "%s/%s/ior.out" % ( target_dirs[0], user ) ],
#  "o" : [ "%s/%s/nn/ior.out" % ( target_dirs[0], user ) ],
  "o" : [ "%s/ior_MPIIO_%s.out@%s/ior_MPI_%s.out" % ( target_dirs[0], time.mktime( datetime.datetime.now().timetuple()), target_dirs[1], time.mktime( datetime.datetime.now().timetuple())) ],
#
# String of IOR directives in name=value format; e.g.,
# -O checkRead=1,lustreStripeCount=32.
#
#  "O" : [ <string of IOR directives> ],
#
# Whether or not to preallocate the file to its ultimate size.
#
#  "p" : [ '' ],
#
# Whether or not to use a shared file pointer. There is a note in the User Guide
# that this option is not working as of 14-Nov-2014.
#
#  "P" : [ '' ],
#
# Whether or not to abort when an error is encountered while doing file
# error checking. The default is not to abort when an error is encountered.
#
#  "q" : [ '' ],
#
# Use this with -C and -Z options for read tests. This tells IOR how many nodes to
# offset the reader from the writer. When used with -C it is a constant node offset.
# When used with -Z it is at least the specified number of nodes. If not use, this
# parameter defaults to 1 (one).
#
#  "Q" : [ <integer node offset> ],
#
# Whether or not to read the existing file or files from a current or previous run.
# By default a read test will happen.
#
# See the NOTE from the -w option.
#
  "r" : [ '' ],
#
# Whether or not to check that the value read was the value that was to
# be written.
#
# The check is to read the data and check for errors against a known pattern. Can
# be used independently of -r. By default the check is not done.
#
# NOTE: data checking is not timed and does not affect other performance timing.
# All errors are tallied and returned as program exit code, unless -q is used.
#
#  "R" : [ '' ],
#
# The number of segments in a file. The default is 1 (one).
#
# NOTE: A segment is a contiguous chunk of data accessed by multiple clients,
# each writing/reading its own contiguous data comprised of blockes accessed
# by multiple clients. With HDF5 this repeats a pattern of an entire shared
# dataset.
#
#  "s" : [ <integer segments> ],
#
# Whether or not to put strided acces into the data type. There is anote in the
# User Guide that this option is not working as of 14-Nov-2014.
#
#  "S" : [ '' ],
#
# The transfer size in bytes; e.g., 8, 4k, 2m, 1g. The size in bytes of a single
# data buffer to be transferred in a single I/O call. The default is 262144
# (256k).
#
#  "t" : [ <transfer size> ],
  "t" : [ '64m' ],
#
# The maximum time in minutes to run tests. The default is 0 (zero).
#
# NOTE: Setting this to 0 (zero) unsets this option. This option allows the
# current read/write to complete without interruption if the time expires
# while reading/writing.
#
#  "T" : [ <integer minutes> ],
#
# Whether or not to use a unique directory for each task in a file-per-proc
# test. The default is all files in one directory.
#
#  "u" : [ '' ],
#
# The full-path and filename of the hints file. By default there is no hints
# filename.
#
#  "U" : [ <string full-path filename for test> ],
#
# The verbosity of output. The more "v"s the more verbosity; e.g., -v, -vv,
# -vvv, etc.. Verbosity is up to 5 (five) v's. The default is 0 (zero).
#
#  "v" : [ '' ],
#
# Whether or not to use MPI_File_set_view.
#
#  "V" : [ '' ],
#
# Whether or not to do a write file test, first deleting any existing file.
# By default a write test will happen.
#
# NOTE: the defaults for writeFile and readFile are set such that if there
# is not at least one of the following -w, -r, -W, or -R, it is assumed
# that -w and -r are expected and are consequently used -- this is only true
# with the command line, and may be overridden in a script.
#
  "w" : [ '' ],
#
# Whether or not to do a check read after each write to make sure that the
# correct value was written.
#
# The check is to read the data and check for errors against a known pattern. Can
# be used independently of -w. By default the check is not done.
#
# NOTE: data checking is not timed and does not affect other performance timing.
# All errors are tallied and returned as program exit code, unless -q is used.
#
#  "W" : [ '' ],
#
# Whether or not to do only one try for an I/O transfer. If set, only one
# try will be made. If not set, it will retry if an I/O transfer fails.
#
#  "x" : [ '' ],
#
# The random seed to use for the -Z option. By default is 0 (zero). Use a
# number >0 for the same seed for all iterations or <0 for a different seed
# for each iteration.
#
#  "X" : [ <integer seed> ],
#
# Whether or not to perform an "fsync" after each POSIX write.
#
#  "Y" : [ '' ],
#
# Whether or not to do random offsets (not sequential) within a file. The
# default is sequential, not random.
#
# NOTE: This option is incompatible with -R, -l, -c, HDF5, NCMPI.
#
#  "z" : [ '' ],
#
# Whether or not to make a task on a different node read the data written
# by the writer task. Assigns the reader task to another node randomly.
# The default is not to do this, so you must use this option if you wish
# to ensure that this data is read by a task on another node, which will
# mean it is not read from an in-memory buffer, but from the storage device.
#
# That is, it reorders tasks by a picking a random node offset for writing/reading
# neighbor's data from different nodes. The node offset is 1 (one) by default, but
# can be changed with the -Q <node offset> parameter. When used with this option
# it means at least (or >=) the number of nodes to offset.
#
# USE THIS OR -C OR NEITHER, BUT NOT BOTH!!!
#
#  "Z" : [ '' ],
}

#############################################################################
# typical use of this framework won't require modification beyond this point
#############################################################################

#
# We've listed all the arguments to this method, but we've commented out
# the ones that we currently are not using, and that are defaulted to "None".
#
def get_commands( expr_mgmt_options ):
  global mpi_options, mpi_program, program_options
  return expr_mgmt.get_commands(
      mpi_program=mpi_program,
      expr_mgmt_options=expr_mgmt_options,
      #program_arguments=program_arguments,
      mpi_options=mpi_options,
      program_options=program_options )
#      program_options=program_options,
#      mpirun=mpirun )


#############################################################################
#
# If you want to use the loops and other program_options assignments to do
# tests you'll want to use the following get_commands, make_commands and
# setting commands to [].
#

#def get_commands( expr_mgmt_options ):

# helper utility
#  def make_commands():
#    return expr_mgmt.get_commands(
#      mpi_options=mpi_options,
#      mpi_program=mpi_program,
#      mpirun=mpirun,
#      program_arguments=program_arguments,
#      program_options=program_options,
#      expr_mgmt_options=expr_mgmt_options )

#  commands = []


#
# Cases that use the group of get_coammands, make_commands, and setting
# commands to [].
#

# N-1 strided
#
# The -s option, for segment count, being greater than one and dividing up
# the total amount of data a process writes over those segments by making
# the block size the amount of data a process writes per stride is what makes
# this option do N-1 strided versus N-1 segmented.
#
#  for size in io_sizes:
#    program_options['s'] = [ data_per_proc/size ]
#    program_options['b'] = [ size ]
#    program_options['t'] = [ size ]
#    commands += make_commands()

# N-1 segmented
#
# The -s option, for segment count, being 1 (one) with the -b, block size,
# being the size of each processes' segment and -t, transfer size, telling
# how much each process will write into its segment with each write is
# what makes this option do N-1 segmented versus N-1 strided.
#
#  program_options['s'] = [ 1 ]
#  program_options['b'] = [ data_per_proc ]
#  program_options['t'] = io_sizes 
#  commands += make_commands() 

# N-N 
# The -F, file-per-proc, option being set is what makes this option do
# N-N, where each process writes its data to its own file.
#
#  program_options['F'] = [ '' ]
#  commands += make_commands() 

#  return commands
#############################################################################
