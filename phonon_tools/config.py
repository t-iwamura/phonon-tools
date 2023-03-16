import json
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Config:
    calc_dir: str
    inputs_dir: str
    mode: str
    use_mlp: bool = False
    use_upho: bool = False


def load_config(path: str) -> Config:
    """Load configs/*.json

    Args:
        path (str): path to configs/*.json

    Returns:
        Config: phonon calculation config dataclass
    """
    with open(path) as f:
        config_dict = json.load(f)
    return Config.from_dict(config_dict)  # type: ignore
