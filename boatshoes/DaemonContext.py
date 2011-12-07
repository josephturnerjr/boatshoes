import os
import resource 
import ctypes
import sys


class DaemonError(Exception):
    pass

class DaemonContext(object):
    def __init__(self, do_daemon):
        self.do_daemon = do_daemon
        self.return_value = 0
        if self.do_daemon:
            # Create the notification pipe
            try:
                self.parent_pipe, self.child_pipe = os.pipe() 
            except:
                raise DaemonError("Couldn't create pipe for startup notification")

            # Set the file creation mask
            os.umask(0)

    def __enter__(self):
        if self.do_daemon:
            # Get the max nr of file descriptors
            try:
                curr_fd, max_fd = resource.getrlimit(resource.RLIMIT_NOFILE)
            except resource.error:
                raise DaemonError("Couldn't get file descriptor rlimit")

            try:
                pid = os.fork()
            except OSError:
                raise DaemonError("Couldn't fork daemon process")

            if pid != 0:
                # If we're the parent, stick around so we can print/return errors
                os.close(self.child_pipe)
                # TODO: there should be a timeout here, probably
                child_status = ""
                byte_len = ctypes.sizeof(ctypes.c_int)
                try:
                    # Read from the pipe until the child sends a number
                    while len(child_status) < byte_len:
                        child_status += os.read(self.parent_pipe, byte_len)
                    # Cast the returned by string to an int
                    exit_status = ctypes.cast(ctypes.create_string_buffer(child_status), 
                                       ctypes.POINTER(ctypes.c_int))[0]
                except:
                    exit_status = -1
                # Because the parent never leaves __enter__, __exit__ will never get called
                sys.exit(exit_status)
            else:
                os.close(self.parent_pipe)

            try:
                os.chdir("/") 
            except:
                self.write_status(-1)
                raise DaemonError("Error changing directory to /")

            # Close file descriptors
            if max_fd == resource.RLIM_INFINITY:
                max_fd = 1024
            for fd in xrange(0, max_fd):
                try:
                    if fd != self.child_pipe:
                        os.close(fd)
                except OSError:
                    pass

            f = file("/dev/null", "r+")
            os.dup2(f.fileno(), sys.stdin.fileno())
            os.dup2(f.fileno(), sys.stdout.fileno())
            os.dup2(f.fileno(), sys.stderr.fileno())
            if(sys.stdin.fileno() != 0 or
               sys.stdout.fileno() != 1 or
               sys.stderr.fileno() != 2):
                self.write_status(-1)
                raise DaemonError("Error redirecting standard input/output/error.  Exiting.")
        return self

    def __exit__(self, type, value, tb):
        self.write_status(self.return_value)

    def write_status(self, status):
        if self.do_daemon:
            os.write(self.child_pipe, ctypes.c_int(status))
