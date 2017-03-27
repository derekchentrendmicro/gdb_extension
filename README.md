* force memory allocation to fail
  - description
    break at malloc and save sha1 of each call stack. after collecting all stacks, call the program
    again and this time set the allocation size to 0. the purpose to calculating sha1 is to save time 
    by avoiding running the test with same call stack
  - steps
    1. gdb -x gdb_save_stacks --args <command>
    2. gdb -x gdb_do_memory_error --args <command>