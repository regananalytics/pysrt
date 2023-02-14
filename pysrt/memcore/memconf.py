import logging
from pathlib import Path
import yaml

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)



class MemConfig:

    def __init__(self, yaml_file:Path|str):
        if not Path(yaml_file).exists():
            raise FileNotFoundError(f"Could not find {yaml_file}")
        self.yaml_file = yaml_file
        self.config = yaml.safe_load(open(yaml_file, 'r'))

        self._game_info = {}
        self._game_versions = {}
        self._states = {}
        self._structs = {}
        self._enums = {}


    def build(self):
        # Build structs and enum classes
        for key, value in self.config.items():
            if key.upper() == 'STRUCTS':
                for struct_name, struct_info in value.items():
                    self._structs[struct_name] = self._build_struct(struct_name, struct_info)


    def _build_struct(self, struct_name:str, struct_info:dict):
        class _Struct: ...
        _Struct.__name__ = struct_name
        if 'Fields' in struct_info:
            for field_name, field_info in struct_info['Fields'].items():
                setattr(
                    _Struct, 
                    '_' + field_name, 
                    {
                        'type': field_info['Type'],
                        'default': field_info['Default'],
                        'value': field_info['Default']
                    }
                )


if __name__ == '__main__':
    config = MemConfig('memconf/re2.yaml')
    config.parse()