import re
import os
import pwd


"""
def chmod(f, mode):
    newmode
    if isinstance(mode, int):
        print mode
        newmode = mode
    else:
        current = stat.S_IMODE(os.stat(f).st_mode)
        newmode = get_int_mode(mode, current)
    os.chmod(f, newmode)

def get_int_mode(mode, current_mode = 0):
    # Match octal
    m = re.match(r"[01234567]{1,4}$", mode)
    if m:
        nums = re.match(r"[0]*(\d*)", mode)
        if nums.groups()[0]:
            return int(nums.groups()[0], 8)
        else:
            return 0
    else:
        mode_array = map(lambda x: x.strip(), mode.split(","))
        for mode_str in mode_array:
            m = re.match(r"^([ugoa]?)([\+\-\=])([rwxXst]{0,6}|[ugo]{1})$", mode)
            print mode, m
            if not m:
                raise OSError("Improper mode specification string %s" % (mode,))
            else:
                if m[1] == '+':
                elif m[1] == '-':
                elif m[1] == '=':
                return 0
"""

def ch_file(self, filename, username=None, groupname=None, mode=None):
    uid = gid = -1
    if username:
        uid = pwd.getpwnam(username)[2]
    if groupname:
        gid = pwd.getgrnam(groupname)[2]
    os.chown(filename, uid, gid)
    if mode:
        os.chmod(filename, mode)
        
def drop_priv(self, username):
    pwd_entry = pwd.getpwnam(username)
    os.setgid(pwd_entry[3])
    os.setuid(pwd_entry[2])

