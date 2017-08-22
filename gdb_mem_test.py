import re
import gdb
import hashlib
import pickle
from subprocess import check_call, CalledProcessError

def fileSHA1(filename):
   h = hashlib.sha1()
   with open(filename,'rb') as f:
     line = 0
     while line != b'':
       line = f.readline()
       line = re.sub(r'0x[0-9a-f]+',r'####',line)  #mask address
       line = re.sub(r'\s\(.+\)\s',r'()',line)     #remove arguments because some may be random
       h.update(line)
   return h.hexdigest()

class ForceMemoryError(gdb.Command):

  pklfile = 'bt.pickle'
  def __init__ (self):
    super (ForceMemoryError, self).__init__ ("domemerr", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE, True)
    #read stack history saved by SaveBacktrace
    with open(self.pklfile, 'rb') as handle:
      self.backtraces = pickle.load(handle)

  def invoke (self, arg, from_tty):
    if 0 == len(arg):
      sha1sum = fileSHA1('gdb.txt')
      if sha1sum in self.backtraces and self.backtraces[sha1sum] == 0:
        #gdb.write('running sha1sum = {0}\n'.format(sha1sum))
        self.backtraces[sha1sum] = 1
        gdb.execute('set $hit = 1')
        gdb.execute('set variable size = 0')
        gdb.execute('disable 1')
      #else:
      #  gdb.write('skip sha1sum = {0}\n'.format(sha1sum))
    else:
      args = gdb.string_to_argv(arg)
      if args[0] == 'state':
        if args[1] == 'save':
          gdb.write('save current state\n')
        elif args[1] == 'reset':
          gdb.write('reset state\n')
          for s in self.backtraces:
            self.backtraces[s] = 0
        else:
          return
        with open(self.pklfile, 'wb') as handle:
          pickle.dump(self.backtraces, handle, protocol=pickle.HIGHEST_PROTOCOL)

class SaveBacktrace(gdb.Command):

  def __init__ (self):
    super (SaveBacktrace, self).__init__ ("savebt", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE, True)
    self.backtraces = {}
    with open('ignore.pickle', 'rb') as handle:
      self.ignorelist = pickle.load(handle)

  def invoke (self, arg, from_tty):
    sha1sum = fileSHA1('gdb.txt')
    if sha1sum not in self.backtraces and sha1sum not in self.ignorelist:
      self.backtraces[sha1sum] = 0
    #  gdb.write('sha1sum = {0} is new\n'.format(sha1sum))
    #else:
    #  gdb.write('sha1sum = {0} already exists\n'.format(sha1sum))
    if len(arg):
      with open(arg, 'wb') as handle:
        pickle.dump(self.backtraces, handle, protocol=pickle.HIGHEST_PROTOCOL)

class MyRun(gdb.Command):
  '''
  just can't make run command in while loop of gdb script work.
  wrapping it in the extension works for me.
  '''

  def __init__ (self):
    super (MyRun, self).__init__ ("myrun", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE, True)

  def invoke (self, arg, from_tty):
    gdb.execute('run', from_tty)
    out = gdb.execute('p $_siginfo', from_tty, True)
    if re.search(r'si_signo = 6',out): # SIGABRT = 6
      gdb.write('Got SIGABRT\n' + out)
      #raise gdb.GdbError("SIGABRT") # sometimes you may want to stop the execution once the error occurs.

'''
for reference. may be useful someday

class GetShellExecResult(gdb.Command):

  def __init__ (self):
    super (GetShellExecResult, self).__init__ ("shellexec",
                         gdb.COMMAND_SUPPORT,
                         gdb.COMPLETE_NONE, True)
    
  def invoke (self, arg, from_tty):
    try:
        check_call(["perl", arg])
    except CalledProcessError:
        gdb.write('return non-zero\n')
        return
    gdb.execute('bt', from_tty)
'''

SaveBacktrace()
ForceMemoryError()
MyRun()

