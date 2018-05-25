GDB Extension
===============
  - gdbext_oom.py
    break at malloc and let the size to malloc be 0. during the test, record sha1 of each backtrace so as to skip
    the same backtrace.
  - scenarios
    1. dump backtraces without making malloc fail. this can be used as ignored list. run some scenarios that you're not
       interested in oom test. rename bt.pkl to bt_ignored.pkl.
       OOM_DRY_RUN=1 gdb -x oom.gdb --args <command>
    2. running oom test
       a. gdb -x oom.gdb --args <command> >mem.log 2>&1
       b. check errors in the log. the following keywords are just some examples. they may be different depending on user's needs.
          grep -e SIGABRT -e SIGSEGV mem.log
          grep "received signal" mem.log
  - note
    1. bt.pkl is accumulated. this help reduce the testing time.
    2. it's suggested to run a test case in minimum scope becasue it will repeat the same scenario many times.

  - enhancement
    1. some code paths do the same thing but their backtraces are slightly different.
    2. how to check code coverage?