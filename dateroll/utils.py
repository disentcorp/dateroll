import fcntl
import os
import pathlib

XPRINT_ON = False

DEBUG_COLORS ={
    'blue' : '\033[94m',
    'cyan' : '\033[96m',
    'green' : '\033[92m',
    'yellow' : '\033[33m',
    'red' : '\033[31m',
    'end' : '\033[0m',
    'gray':'\x1b[38;5;239m'
}

def color(s,color):
    return DEBUG_COLORS[color] + str(s) + DEBUG_COLORS['end']

def xprint(*args,**kwargs): # pragma:no cover
    if XPRINT_ON:
        _color = kwargs.get('color','yellow')
        if 'lbl' in kwargs:
            lbl = kwargs.get('lbl')
            b = kwargs.get('before','x')
            a = kwargs.get('after','x')
            b = str(b)
            a = str(a)
            a_star=''
            for _a,_b in zip(a,b):
                if _a==_b:
                    a_star += color(_a,'green')
                else:
                    a_star += color(_a,'blue')
            b = color(b,'green')
            s = f'{color('before',_color)}: {b}, {color('after',_color)}: {a_star}'
            print(color(f'[debug] {lbl:>12} ',_color),s)
        else:
            args = [color(a,_color)for a in args]
            print(color('[debug]',_color),*args,**kwargs)

def combine_none(a,b):
    if a is None and b is None:
        return None
    a = [] if a is None else a
    b = [] if b is None else b
    return tuple(sorted(set(a)|set(b)))

def add_none(a,b,dir=1):
    if a is None and b is None:
        return None
    else:
        a = 0 if a is None else a
        b = 0 if b is None else b
        return a + b*dir

class safe_open:
    """
    use separate write lockfile to lock/unlock (fcntl removes dealock if pid w/ lock dies)
    lock is removed if pid dies
    """

    def __init__(self, path, mode="r"):
        """
        open lockfile and attempt to lock, will block
        """
        self.path = pathlib.Path(path)
        self.mode = mode
        self.pathlock = self.path.with_suffix(".lockfile")
        self.lockfile = open(self.pathlock, "w")
        fcntl.lockf(self.lockfile, fcntl.LOCK_EX)

    def __enter__(self):
        """
        open user file and send it to them
        """
        self.file = open(self.path, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        release lock, then close both lockfile and user file
        do not delete lockfile (even if no exc)
        """
        fcntl.lockf(self.lockfile, fcntl.LOCK_UN)
        self.lockfile.close()
        self.file.close()

convention_map = {
    'YMD':r'%Y-%m-%d',
    'DMY':r'%d-%m-%Y',
    'MDY':r'%m-%d-%Y'
}