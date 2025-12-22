from platform import system
from os import getenv
from os.path import join, isfile
from pathlib import Path
from json import loads, dumps
from typing import Dict, Any


class Config:
    """configuration writer and reader for sine"""
    def __init__(self, override_path:str|None=None):
        self.p = None
        if override_path:
            self.p = override_path
        else:
            s = system()
            if s == "Windows":
                bp = getenv('LOCALAPPDATA')
                self.p = join(bp, "sine.json")
            elif s == "Linux":
                bp = Path.home()
                self.p = bp/".config"/"sine.json"

        self.config = None

        #init
        if not self._check_exist():
            self._setup()
        self._load()

    def _setup(self) -> None:
        """completely overwrites the existing configuration with a new blank json file. intended for use if the configuration does not exist."""
        self._write({})

    def _check_exist(self) -> bool:
        """returns true if the configuration file exists. returns false otherwise"""
        if self.p:
            if isfile(self.p):
                return True
            else:
                return False
        else:
            return False

    def _load(self) -> None:
        """internally loads the configuration file if it does exist"""
        if self._check_exist():
            with open(self.p, "r") as f:
                self.data = loads(f.read())

    def _write(self, data:Dict) -> None:
        if self.p:
            with open(self.p, "w") as f:
                f.write(dumps(data))

    def save(self) -> None:
        """saves the current configuration data to disk"""
        if self.data:
            self._write(self.data)

    def get(self, element:str|float|int) -> Any:
        """get an element from the currently loaded configuration"""
        if element in self.data:
            return self.data[element]
        else:
            return None

    def set(self, element:str|float|int, value:Any) -> None:
        """set an element in the currently loaded configuration with a new value"""
        if element in self.data:
            self.data[element]=value
        else:
            return None

    def __getitem__(self, item):
        return self.data[item]