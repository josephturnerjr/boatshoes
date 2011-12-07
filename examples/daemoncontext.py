from boatshoes.DaemonContext import DaemonContext

def do_important_work():
    import time
    time.sleep(5)    

if __name__ == "__main__":
    try:
        # When the context manager is created, daemonization occurs.
        # The parent process, the one that is attached to the terminal
        #   does not exit immediately, but waits on input to a pipe.
        #   The child enters the context statements and can alter the
        #   shell return value of the parent by setting it (integer 0-255)
        with DaemonContext(True) as dc:
            # Only the child makes it in
            print "yep" # won't be printed
            # Any change to the return value will be reflected in the parent
            #   exit code. If nothing is set, return code will be 0.
            dc.return_value = 187 
        # After the context, the parent has exited and the child can go on
        #   its merry way.
        do_important_work()
    except SystemExit, e:
        print e.code # will print -1
        # Re-raise to set the shell exit code. Try this:
        #   ~/boatshoes (master)> python example.py; echo $?
        #   187
        #   187
        # It will exit almost immediately, though the child is sleeping.
        raise
