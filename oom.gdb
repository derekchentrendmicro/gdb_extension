set breakpoint pending on
set pagination off
# let each gdb.txt have only one backtrace
set logging overwrite on
source gdb_mem_test.py
break ns_malloc
commands
 # record the number so as to skip it in the next run
 set $brkcnt=$brkcnt+1
 set logging on
 bt
 set logging off
 # let malloc fail
 oom
 continue
end
set $brkcnt=0
set $hit=1
while $hit != 0
 # during oom test, the breakpoint will be disabled so we need to enable it in each run.
 enable 1
 # skip those have been tested
 ignore 1 $brkcnt
 # during oom test, the value will be set to 1 if there's still backtrace to test. otherwise the value is not changed and the execution will stop.
 set $hit=0
 # it's the same as run command, but run just can't work here.
 myrun
end
# save execution results
oom save
q
