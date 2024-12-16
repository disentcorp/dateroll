import importlib.util
import pathlib
import warnings

ctx_conv = "_ctx_convention"

default_settings = {
    "convention": "MDY", 
    "twodigityear_cutoff": 2050, 
    "default_daycounter" : "ACT/365",
    "ie":"(]"
}

def get_settings_path():
    return pathlib.Path().home() / '.dateroll' / 'settings.py'

default_settings_validation = {
    "debug": (lambda x: isinstance(x, bool), TypeError("debug must be bool")),
    "convention": (
        lambda x: isinstance(x, str) and x in ["YMD", "MDY", "DMY"],
        ValueError('must be one of "MDY", "DMY" or "YMD".'),
    ),
    "ie": (
        lambda x: isinstance(x, str) and x in ["()", "(]", "[)", "[]"],
        ValueError(
            "must be one of (), (], [), or [] such that is the interval: (a,b])"
        ),
    ),
    "twodigityear_cutoff": (
        lambda x: isinstance(x, int) and ((x == 1900) or (x >= 2000 and x < 2100)),
        ValueError(
            "Cutoff must be either 1900 (all 2-digit are 1900), 2000 (all 2-digit are 2000), or some n >2001 and < 2099 as a cutoff level"
        ),
    ),
    "default_daycounter": (
                lambda x: x in ["ACT/365", "ACT/365F", "ACT/360", "30/360", "30E/360"],
        ValueError(
            "Must be one of ACT/365, ACT/365F, ACT/360, 30/360, 30E/360"
        ),
    )

}

class Settings:
    """
    singleton whose attributes are stored in a plain .py file as name=value
    """

    def __init__(self):
        """
        retrieve user settings and validate
        """
        
        if self.path.exists():
            d = self.retrieve()
            d_validated = self.validate(d)
            self.__dict__.update(d_validated)

        else:
            self.__dict__.update(default_settings)
            self.save()
    
    @property
    def path(self):
        return get_settings_path()

    def retrieve(self):
        """
        try to load settings file, if corrupted replace with defaults
        """
        try:
            spec = importlib.util.spec_from_file_location("module.name", self.path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            d = mod.__dict__
        except Exception as e:
            d = {}
            msg = f"Unable to read settings file in {self.path}, will restoring defaults."
            warnings.warn(msg)

        d = {k: v for k, v in d.items() if not k.startswith("_")}
        return d

    def save(self):
        """
        save settings file -- settings must be in default_settings
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w") as f:
            txt = f"# Dateroll settings file\n# {self.path}\n\n"
            for k, v in self.__dict__.items():
                if not k.startswith("__") and k in default_settings:
                    txt += f"{k}={repr(v)}\n"
            f.write(txt)

    def validate(self, user_settings):
        """
        2 tests:
            user settings key in default settings
            user settings value passes default settings value check
        1 adjustment:
            append default settings not in user settings for a complete set of settings
        """

        reset = False
        for k, v in user_settings.items():

            if k not in default_settings:
                msg = f"Unknown setting {k}, ignoring"
                warnings.warn(msg)
            else:
                test, exc = default_settings_validation[k]
                if not test(v):
                    raise exc

        for k, v in default_settings.items():
            if k not in user_settings:
                user_settings[k] = v

        return user_settings

    def __getattribute__(self, k):
        if k == "convention":
            if hasattr(self, "_convention_override"):
                return self._convention_override

        return super().__getattribute__(k)

    def __setattr__(self, k, v):
        """
        if a new setting value, validate and save
        """
        if k in default_settings:
            # check, set, save
            func_value_is_valid, exc = default_settings_validation[k]

            if not func_value_is_valid(v):
                raise exc

            super().__setattr__(k, v)
            self.save()
        else:
            super().__setattr__(k, v)

    def __repr__(self):
        """
        show settings
        """
        kwargs = ",".join([f"{k}={repr(v)}" for k, v in self.__dict__.items()])
        string = f"{self.__class__.__name__}({kwargs})"
        return string


settings = Settings()

if __name__ == "__main__":  # pragma: no cover
    # settings = Settings()
    ...
