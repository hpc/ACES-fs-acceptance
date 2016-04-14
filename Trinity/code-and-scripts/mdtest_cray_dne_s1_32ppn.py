import sys,os,time,getpass
sys.path += [ './lib', '../lib' ]
import expr_mgmt

user        = getpass.getuser()
home        = os.getenv( "HOME" )
my_mpi_host = os.getenv( "MY_MPI_HOST" )

#mdtest_top = "/usr/projects/ioteam/trinitite/mdtest-1.9.3/"
#mdtest_top = "/users/atorrez/Testing/mdtest-s3-mdt"
mdtest_top = "/home/atorrez/Testing/mdtest-dne/mdtest"

# the mdtest_wrapper actually calls mpirun so use a non-default mpirun command
# Not using this method anymore but left here for reference
#mpirun = "%s/scripts/mdtest_wrapper.py aprun" % ( mdtest_top )

# if you want to use this to run a new test, use the current time,
# if you want to use this to complete an already started test, use that time
ts = int( time.time() )
#ts = 1269097554
#
# We cannot have a constant file count divided by the number of processes
# in the experiment by defining "n" here, but we do need the variable,
# mpi_options, to exist. We will then use a custom "make_commands" below.
#
mpi_options = {
#  "np"   : [ 2 ], 
#  "np"   : [ 2 ], 
#
# "n" is used on the Crays.
#
#  "n"    : [ 2, 4 ],
}

mpi_program = ( "%s/mdtest" % ( mdtest_top )) 

#target = ( "/panfs/pas12a/vol1/%s/mdtest" % ( user ))
#target_dirs = [ "/lus/trinity/lanl/mdtest", "/lus/trinity/lanl/mdtest" ]
target_dirs = [ "/scratch1/users/atorrez/mdtest","/scratch2/users/atorrez/mdtest" ]

program_options = {
#
# Branching factor of hierarchical directory structure. See README. It's
# complicated.
#
#  "b" : [ 2 ],
#
# Each task times itself. Have noticed bugs where the experiment will
# fail when using this parameter. Generally, don't use it.
#
#  "B" : [ '' ],
#
# Collective creates: task 0 does all the creates and deletes.
#
#  "c" : [ '' ],
#
# Only create files/dirs.
#
  "C" : [ '' ],
#
# The directory for the files.
#
#  "d" : [ "%s/mdtest.%d/" % ( target, ts ) ], 
  "d" : [ "%s/nn_shared_dir/mdt_0@%s/nn_shared_dir/mdt_1@%s/nn_shared_dir/mdt_2@%s/nn_shared_dir/mdt_3@%s/nn_shared_dir/mdt_4" % ( target_dirs[0],target_dirs[0],target_dirs[0],target_dirs[0],target_dirs[0] ) ], 
#
# Perform tests on directories only (no files).
#
#  "D" : [ '' ],
#
# Number of bytes to read from each file.
#
#  "e" : [ 64 ],
#
# Only read files.
#
#  "E" : [ '' ],
#
# First number of tasks on which test will run. I don't understand this and
# there is no additional explanation in the README.
#
#  "f" : [ <integer>?? ],
#
# Perform the tests on the files only (no directories).
#
  "F" : [ '' ],
#
# Number of iterations in the experiment. Default is 1.
#
  "i" : [ 3 ],
#
# "n" and "I" are mutually exclusive. In general, we prefer "n" because it
# creates, stats, and deletes the files in the directory the caller
# specifies.
#
# "I" specifies the number of items per tree node. Use this in conjunction
# with "b" and "z".
#
#  "I" : [ 1, 10 ],
#
# Last  number of tasks on which test will run. I don't understand this and
# there is no additional explanation in the README.
#
#  "l" : [ <integer>?? ],
#
# Create files and directories at the "leaf" level only.
#
#  "L" : [ '' ],
#
# "n" and "I" are mutually exclusive. In general, we prefer "n" because it
# creates, stats, and deletes the files in the directory the caller
# specifies.
#
# Every task will create/stat/delete number of files/dirs specified per tree.
#
# We cannot have a constant file count divided by the number of processes
# in the experiment by defining "n" here. We will use a custom
# "make_commands" below.
#
  "n" : [ 1024 ],
#
# Use multiple mdts. Assign round robin dirs to all mdtes available
#  "M" : [ '' ],
#
# Stride number between neighbor tasks for file/dir stat. Make this the number
# of processes that will run on a node.
#
#  "N" : [ 32 ],
#
# Pre-iteration delay in seconds.
#
#  "p" : [ 10 ],
#
# Only remove files/dirs.
#
  "r" : [ '' ],
#
# Randomly stat files/dirs (optional seed can be provided).
#
#  "R" : [ '' ],
#
# Stride between the number of tasks for each test. No other explanation
# is given. I'm not sure what this does.
#
#  "s" : [ 16 ],
#
# Shared file access (file only, no directories). For N-1 where all
# processes operate on the same file.
#
#  "S" : [ '' ],
#
# Time unique working directory overhead. No other explanation is given.
# I'm not sure what this does.
#
#  "t" : [ '' ],
#
# Only stat files/dirs.
#
  "T" : [ '' ],
#
# This parameter has each process use its own directory. If you don't
# use it, all processes use the same, shared, directory.
#
  "u" : [ '' ],
#
# Verbosity (each instance of option increments by one). So, you can have:
# -v, -vv, -vvv, etc.
#
#  "v" : [ '' ],
#
# Verbosity value. Instead of lots of small "v"s, put an integer after
# this to specify the verbosity value.
#
#  "V" : [ 1 ],
#
# Number of bytes to write to each file.
#
#  "w" : [ 64 ],
#
# Sync file after write completion.
# 
#  "y" : [ '' ],
#
# Depth of hierarchical directory structure. See README. It's complicated.
#
#  "z" : [ 1, 2 ],
}

# the wrapper looks for these args at the end of the args and splices them
# off before calling IOR, these args are used by the wrapper to get more
# data into the sql insert
#program_arguments = [
#  [ "--desc ./mdtest.%d" % int(time.time()) ]
#]

#############################################################################
# typical use of this framework won't require modification beyond this point
#############################################################################

def get_commands( expr_mgmt_options ):
  global mpi_options,program_options,program_arguments,mpirun
#
# Uncomment this section when using mpi_options and "n" from above.
#
#  commands = expr_mgmt.get_commands( 
#      mpi_options=mpi_options,
#      mpi_program=mpi_program,
##      program_arguments=program_arguments,
##      mpirun=mpirun,
#      program_options=program_options,
#      expr_mgmt_options=expr_mgmt_options )
#  return commands
#
# Comment this section when using mpi_options and "n" from above.
#
  def make_commands():
    return expr_mgmt.get_commands(
        mpi_options=mpi_options,
        mpi_program=mpi_program,
  ##      program_arguments=program_arguments,
  ##      mpirun=mpirun,
        program_options=program_options,
        expr_mgmt_options=expr_mgmt_options )

  commands = []

  #for exponent in [ 25, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000, 100000 ]:
  #for exponent in [ 1000, 2000, 5000, 10000, 50000, 100000,200000 ]:
  for exponent in [ 2000 ]:
    np = exponent
    mpi_options['n'] = [ np ]
    program_options['n'] = [ 1000000/np ]
    commands += make_commands()

  #for exponent in range ( 5, 17 ):
  ##for exponent in range ( 5, 6 ):
    #np = 2**exponent
    #mpi_options['n'] = [ np ]
    #program_options['n'] = [ 1048576/np ]
    #commands += make_commands()

  return commands

