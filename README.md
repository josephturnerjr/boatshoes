# Boatshoes: helpful Unix service utilities

Boatshoes is a small library of helpful tools for creating Linux/Unix services.
Specifically, it includes the following:

* **DaemonContext**, a pipe-communicating daemonization routine, allowing your
application to exit with the correct code even after daemonization.
* **SingleInstance**, an RAII-style PID lock, following the correct Unix way: file
locking with fcntl
* Some random stuff for handling file privileges
* An easy way to drop privileges

## Documentation

### DaemonContext

DaemonContext serves as a context manager for daemonization, allowing the 
application to exit with meaningful error codes. These codes are important
in instances where the application is being run by init.d. To create such
a context, use a with statement, as so:

    with DaemonContext(True) as dc:
        ...

Within the context, the application should be initializing. If an error crops
up, you can set the return value for the context object (using the names as 
above) as:

    dc.return_value = 187 

When the context exits, the parent will then exit with the appropriate return
code. Of course, if for some perverse reason you wanted to, you could catch
the raised SystemExit exception and handle it yourself.

The DaemonContext constructor takes a single boolean parameter that specifies
whether or not the application should in fact daemonize. If the paramter is
False, the context is basically a no-op. This enables applications to accept
a command-line parameter specifying whether or not to daemonize.
