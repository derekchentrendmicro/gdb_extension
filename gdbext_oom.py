import os
import re
import gdb
import hashlib
import pickle
#from subprocess import check_call, CalledProcessError

def fileSHA1(filename):
   h = hashlib.sha1()
   with open(filename,'rb') as f:
     line = f.readline()
     while line:
       if re.search(r'Perl_pp_entersub',line): break			# not care about functions below Perl_pp_entersub (can't promise this has no side effect though)
       line = re.sub(r'0x[0-9a-f]+',r'####',line)			# mask address
       line = re.sub(r'\s\(.+\)\s',r'()',line)				# remove arguments because their values may vary
       h.update(line)
       line = f.readline()
   return h.hexdigest()

class OOM(gdb.Command):

  bt_pickle = 'bt.pkl'
  bt_ignored_pickle = 'bt_ignored.pkl'
  def __init__ (self):
    super (OOM, self).__init__ ("oom", gdb.COMPLETE_NONE, True)

    self.bt = {}
    self.bt_ignored = {}
    self.dry_run = True if os.environ.get('OOM_DRY_RUN') else False	# only check set or unset. not check value, e.g., 0 or false.

    try:								# read bt history (to skip those have been tested)
      with open(OOM.bt_pickle, 'rb') as f:
        self.bt = pickle.load(f)
    except:
      pass

    try:								# bt that needs not to test
      with open(OOM.bt_ignored_pickle, 'rb') as f:
        self.bt_ignored = pickle.load(f)
    except:
      pass

  def invoke (self, arg, from_tty):
    if 0 == len(arg) or self.dry_run:
      sha1sum = fileSHA1('gdb.txt')
      if sha1sum in self.bt_ignored:
        gdb.write('sha1sum = {0} is ignored.\n'.format(sha1sum))
      elif sha1sum in self.bt and self.bt[sha1sum] == True:
        gdb.write('sha1sum = {0} has been tested.\n'.format(sha1sum))
      else:
        gdb.write('add sha1sum = {0}\n'.format(sha1sum))
        self.bt[sha1sum] = not self.dry_run
        if not self.dry_run:
          gdb.execute('set $hit = 1')					# not finish all backtraces yet
          gdb.execute('set variable size = 0')				# let size of malloc be 0
          gdb.execute('disable 1')					# disable breakpoint. allow only 1 malloc error in each execution to avoid interference.
    elif arg == 'save':
        gdb.write('save execution results\n')
        with open(OOM.bt_pickle, 'wb') as f:
          pickle.dump(self.bt, f, protocol=pickle.HIGHEST_PROTOCOL)

class MyRun(gdb.Command):
  '''
  run command in while loop always stops even the stop condition is not met.
  after replacing it with this class, the problem is fixed. confusing!
  '''

  def __init__ (self):
    super (MyRun, self).__init__ ("myrun", gdb.COMPLETE_NONE, True)

  def invoke (self, arg, from_tty):
    gdb.execute('run', from_tty)
    #out = gdb.execute('p $_siginfo', from_tty, True)
    #if re.search(r'si_signo = 6',out): # SIGABRT = 6
    #  gdb.write('Got SIGABRT\n' + out)
    #  #raise gdb.GdbError("SIGABRT") # sometimes you may want to stop the execution once the error occurs.

'''
for reference. may be useful someday.

class GetShellExecResult(gdb.Command):

  def __init__ (self):
    super (GetShellExecResult, self).__init__ ("shellexec", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE, True)
    
  def invoke (self, arg, from_tty):
    try:
        check_call(["perl", arg])
    except CalledProcessError:
        gdb.write('return non-zero\n')
        return
    gdb.execute('bt', from_tty)
'''

OOM()
MyRun()

