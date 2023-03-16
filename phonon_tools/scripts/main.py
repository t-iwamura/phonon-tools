import shutil
from pathlib import Path

import click

from phonon_tools.config import load_config
from phonon_tools.postprocess import make_force_constants
from phonon_tools.preprocess import arrange_disp_set_dir


@click.command()
@click.argument("config_file")
def main(config_file) -> None:
    "Useful tools to perform phonon calculation by DFT"
    config = load_config(config_file)

    if config.mode == "relax":
        relax_dir_path = Path(config.calc_dir) / "relax"
        shutil.copytree(config.inputs_dir, relax_dir_path)
    elif config.mode == "preprocess":
        arrange_disp_set_dir(
            calc_dir=config.calc_dir,
            inputs_dir=config.inputs_dir,
            use_upho=config.use_upho,
            use_mlp=config.use_mlp,
        )
    elif config.mode == "postprocess":
        make_force_constants(
            calc_dir=config.calc_dir,
            inputs_dir=config.inputs_dir,
            use_upho=config.use_upho,
        )


if __name__ == "__main__":
    main()
