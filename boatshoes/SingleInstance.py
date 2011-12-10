import os
import fcntl
import errno

class SingleInstanceError(Exception):
    pass

class PidPermissionError(Exception):
    pass

class RunningInstanceError(Exception):
    pass

class SingleInstance(object):
    def __init__(self, lockfile):
        self.try_pid_lock(lockfile)

    def try_pid_lock(self, lockfile):
        # Open the lockfile
        try:
            # Need the low-levelness to make sure the file gets created 
            #   with the right mode.
            fd = os.open(lockfile, os.O_RDWR|os.O_CREAT, 0644)
        except OSError, e:
            if e.errno == errno.EACCES:
                raise PidPermissionError("Permission denied when trying to "
                                         "open the pidfile.")
            raise SingleInstanceError("Couldn't open lockfile %s: %s" % 
                                      (lockfile, e.strerror))
        # Lock the lockfile
        try:
            fcntl.lockf(fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
        except IOError, e:
            os.close(fd)
            # If one of these errors, then its already locked
            if (e.errno == errno.EACCES or 
                e.errno == errno.EAGAIN):
                raise RunningInstanceError("Can't lock file. "
                                           "Is another instance running?")
            # Otherwise, its a fcntl error
            raise SingleInstanceError("Can't lock the lockfile %s: %s" % 
                                      (lockfile, e.strerror))
        # At this point, the file is locked. Write in the pid and return.
        # Clear the contents of the file
        try:
            os.ftruncate(fd, 0)
        except OSError, e:
            os.close(fd)
            raise SingleInstanceError("Can't truncate the lockfile %s: %s" % 
                                      (lockfile, e.strerror))
        # Write the PID
        #f = os.fdopen(fd)
        #f.write(os.getpid());
        os.write(fd, str(os.getpid()))
        # keep the fd open!
        self._file = fd
