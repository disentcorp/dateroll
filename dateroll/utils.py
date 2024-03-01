import os
import pathlib
import fcntl

class safe_open:
    '''
    use separate write lockfile to lock/unlock (fcntl removes dealock if pid w/ lock dies)
    lock is removed if pid dies
    '''
    def __init__(self,path,mode='r'):
        '''
        open lockfile and attempt to lock, will block
        '''
        self.path = pathlib.Path(path)
        self.mode = mode
        self.pathlock = self.path.with_suffix('.lockfile')
        self.lockfile = open(self.pathlock,'w')
        fcntl.lockf(self.lockfile,fcntl.LOCK_EX)
    def __enter__(self):
        '''
        open user file and send it to them
        '''
        self.file = open(self.path,self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        release lock, then close both lockfile and user file
        do not delete lockfile (even if no exc)
        '''
        fcntl.lockf(self.lockfile,fcntl.LOCK_UN)
        self.lockfile.close()
        self.file.close()