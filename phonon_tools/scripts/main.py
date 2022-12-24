import click

from phonon_tools.config import load_config


@click.command()
@click.argument("config_file")
def main(config_file) -> None:
    "Useful tools to perform phonon calculation by DFT"
    config = load_config(config_file)

    if config.mode == "preprocess":
        pass
    elif config.mode == "postprocess":
        pass


if __name__ == "__main__":
    main()
