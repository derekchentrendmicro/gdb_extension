import gdb
import hashlib
import pickle
from subprocess import check_call, CalledProcessError

def fileSHA1(filename):
   h = hashlib.sha1()
   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)
   return h.hexdigest()

class BacktraceFilter(gdb.Command):

  def __init__ (self):
    super (BacktraceFilter, self).__init__ ("btfilter",
                         gdb.COMMAND_SUPPORT,
                         gdb.COMPLETE_NONE, True)
    '''read stack history saved this way
    a = {'21326a5dd55d0dcf664e470f402d867da694b791': 0}
    with open('filename.pickle', 'wb') as handle:
      pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)
    '''
    with open('stackHistory.pickle', 'rb') as handle:
      self.history = pickle.load(handle)

  def invoke (self, arg, from_tty):
    sha1sum = fileSHA1('gdb.txt')
    if sha1sum in self.history and self.history[sha1sum] == 0:
       self.history[sha1sum] = 1
       gdb.execute('set variable size = 0')
    gdb.execute('c', from_tty)

class GetShellExecResult(gdb.Command):

  def __init__ (self):
    super (GetShellExecResult, self).__init__ ("mybt",
                         gdb.COMMAND_SUPPORT,
                         gdb.COMPLETE_NONE, True)
    
  def invoke (self, arg, from_tty):
    try:
        check_call(["perl", arg])
    except CalledProcessError:
        gdb.write('return non-zero\n')
        return
    gdb.execute('bt', from_tty)


BacktraceFilter()
