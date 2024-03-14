import warnings
import pathlib
import importlib.util

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
    def __init__(self):
        if path.exists():
            self.load()
            self.validate()
        else:
            self.load_default()
            self.save()

    def load_default(self):
        self.__dict__.update(default_settings)
    
    def load(self):    
        spec = importlib.util.spec_from_file_location("module.name", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        settings = mod.__dict__
        self.__dict__.update(settings)

    def save(self):
        with open(path,'w') as f:
            txt = f'# Dateroll settings file\n# {path}\n\n'
            for k,v in self.__dict__.items():
                if k in default_settings:
                    txt += f'{k}={repr(v)}\n'
            f.write(txt)

    def validate(self):
        # key check
        reset = False
        for k,v in self.__dict__.items():
            if k.startswith('__'):
                continue
            key_is_valid = k not in default_settings
            type_is_valid = not isinstance(v,type(default_settings.get(k,None)))
            func_value_is_valid, exc = default_settings_validation.setdefault(k,(lambda x:False,ValueError(f'Setting {k} not found')))
            if key_is_valid or type_is_valid or not func_value_is_valid(v):
                msg = f'Settings corrupted in {path}, restoring defaults.'
                warnings.warn(msg)
                reset = True
        if reset:
            self.load_default()

    def __setattr__(self,k,v):
        # check, set, save
        func_value_is_valid,exc = default_settings_validation[k]
        
        if not func_value_is_valid(v):
            raise exc
        
        super().__setattr__(k,v)
        self.save()

    def __repr__(self):
        kwargs = ','.join([f'{k}={repr(v)}' for k,v in self.__dict__.items()])
        string = f'{self.__class__.__name__}({kwargs})'
        return string

                
settings = Settings()