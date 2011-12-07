# Boatshoes: helpful Unix service utilities

Boatshoes is a small library of helpful tools for creating Linux/Unix services.
Specifically, it includes the following:

* **DaemonContext**, a pipe-communicating daemonization routine, allowing your
application to exit with the correct code even after daemonization.
* **SingleInstance**, an RAII-style PID lock, following the correct Unix way: file
locking with fcntl

## Documentation

### DaemonContext

DaemonContext serves as a context manager for daemonization, allowing the 
application to exit with meaningful error codes. These codes are important
in instances where the application is being run by init.d. To create such
a context, use a with statement, as so:

    with DaemonContext(True) as dc:
        ...

Within the context, the application will initialize. If an error crops
up, you can set the return value for the context object (using the names as 
above) as:

    dc.return_value = 187 

When the context exits, the parent will then exit with the appropriate return
code. Of course, if for some perverse reason you wanted to, you could catch
the raised SystemExit exception and handle it yourself.

The DaemonContext constructor takes a single boolean parameter that specifies
whether or not the application should daemonize. If the parameter is
False, the context is basically a no-op. This enables applications to accept
a command-line parameter specifying whether or not to daemonize.

For more detailed information, please see the example in 
examples/daemoncontext.py

### SingleInstance

SingleInstance is a RAII-style process PID lock that uses preferred Unix 
semantics. Specifically, it handles single instance guaranteeing by acquiring
a system file lock on the pidfile and writing its PID. This lock is held until
the application exits, at which point the kernel will clean up the lock.

To use SingleInstance, simply instantiate the object with the path to the 
lockfile. It will take care of the rest.
