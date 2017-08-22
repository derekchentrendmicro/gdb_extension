set breakpoint pending on
set pagination off
set logging overwrite on
source gdb_mem_test.py
break ns_malloc
commands
 set $brkcnt=$brkcnt+1
 set logging on
 bt
 set logging off
 domemerr
 continue
end

set $brkcnt=0
set $hit=1
while $hit != 0
enable 1
ignore 1 $brkcnt
set $hit=0
myrun
end
domemerr state save
q
