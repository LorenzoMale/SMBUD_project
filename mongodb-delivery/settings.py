import json
from typing import Any
from os import sep as os_sep
from os.path import realpath, dirname

def mydir():
    return dirname(realpath(__file__))

class Settings:
    def __init__(self, path=mydir() + os_sep + "settings.json") -> None:
        with open(path, "r") as f:
            self.content = json.load(f)["Settings"]
        
        for arg in ["main_txt_file", "languages_file", "universities_file"]:
            self.content[arg] = mydir() + os_sep + self.content["directory"] + os_sep + self.content[arg]

    def __getitem__(self, __name: str) -> Any:
        return self.content[__name]
    
    def __str__(self) -> str:
        return str(self.content)

settings = Settings()

if __name__ == "__main__":
    print(Settings())

