# Boatshoes: helpful Unix service utilities

Boatshoes is a small library of helpful tools for creating Linux/Unix services.
Specifically, it includes the following:
* DaemonContext, a pipe-communicating daemonization routine, allowing your
application to exit with the correct code even after daemonization.
* SingleInstance, an RAII-style PID lock, following the correct Unix way: file
locking with fcntl
* Some random stuff for handling file privileges
* An easy way to drop privileges
