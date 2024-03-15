import warnings
import pathlib
import importlib.util
import code

path = pathlib.Path("~/.dateroll/settings.py").expanduser()

default_settings = {
    'debug':True,
    'convention':'MDY'
}

default_settings_validation ={
    'debug':(
        lambda x: isinstance(x,bool),
        TypeError('debug must be bool')
    ),
    'convention': (
        lambda x: isinstance(x,str) and x in ['YMD','MDY','DMY'],
        ValueError('must be one of "MDY", "DMY" or "YMD".')
    )
}

class Settings:
    '''
    singleton whose attributes are stored in a plain .py file as name=value
    '''
    def __init__(self):
        '''
        if settings load and validate, if not load defaults and save
        '''
        if path.exists():
            self.load()
            self.validate()
        else:
            self.load_default()
            self.save()

    def load_default(self):
        '''
        update singleton with settings
        '''
        self.__dict__.update(default_settings)
    
    def load(self):
        '''
        try to load settings file, if corrupted replace with defaults
        '''
        try:
            spec = importlib.util.spec_from_file_location("module.name", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            settings = mod.__dict__
            self.__dict__.update(settings)
        except:
            msg = f'Settings corrupted in {path}, restoring defaults.'
            warnings.warn(msg)
            self.load_default()
            self.save()

    def save(self):
        '''
        save settings file
        '''
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w') as f:
            txt = f'# Dateroll settings file\n# {path}\n\n'
            for k,v in self.__dict__.items():
                if not k.startswith('__'):
                    txt += f'{k}={repr(v)}\n'
            f.write(txt)

    def validate(self):
        '''
        3 validate checks per setting / key is valid, type of value is valid, and value of value is valid
        '''
        # key check
        reset = False
        for k,v in self.__dict__.items():
            if k.startswith('__'):
                continue
            key_is_valid = k in default_settings
            type_is_valid = isinstance(v,type(default_settings.get(k,None)))
            func_value_is_valid, exc = default_settings_validation.setdefault(k,(lambda x:False,ValueError(f'Setting {k} not found')))

            if  not (key_is_valid and type_is_valid and func_value_is_valid(v)):
                msg = f'Settings corrupted in {path}, restoring defaults.'
                warnings.warn(msg)
                self.load_default()
                break

    def __setattr__(self,k,v):
        '''
        add a new setting
        '''
        # check, set, save
        func_value_is_valid,exc = default_settings_validation[k]
        
        if not func_value_is_valid(v):
            raise exc
        
        super().__setattr__(k,v)
        self.save()

    def __repr__(self):
        ''' 
        show settings
        '''
        kwargs = ','.join([f'{k}={repr(v)}' for k,v in self.__dict__.items()])
        string = f'{self.__class__.__name__}({kwargs})'
        return string

                
settings = Settings()

if __name__=='__main__':  # pragma: no cover
    settings = Settings()