* force memory allocation to fail
  - description
    break at malloc and save sha1 of each call stack. after collecting all stacks, call the program
    again and this time set the allocation size to 0. the purpose to calculating sha1 is to save time 
    by avoiding running the test with same call stack
  - steps
    1. gdb -x save_call_stack.gdb --args <command>
    2. gdb -x fail_malloc.gdb --args <command> >mem.log 2>&1
    3. grep SIGABRT mem.log
       if found, look for the call stack that causes the error.