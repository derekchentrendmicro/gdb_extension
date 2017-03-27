set breakpoint pending on
set pagination off
set logging overwrite on
source gdb_mem_test.py
break ns_malloc
commands
 set logging on
 bt
 set logging off
 savebt
 continue
end
r
savebt bt.pickle
q
