import os
import shutil
import subprocess
from copy import copy
from pathlib import Path


def make_writefc_conf(use_upho: bool = False) -> str:
    """Make content of writefc.conf

    Args:
        use_upho (bool, optional): Whether to use UPHO or not. Defaults to False.

    Returns:
        str: The content of writefc.conf
    """
    writefc_conf_lines = []
    if use_upho:
        up_moments = ["5.0" for _ in range(16)]
        down_moments = ["-5.0" for _ in range(16)]

        up_moments_string = " ".join(up_moments)
        down_moments_string = " ".join(down_moments)
        writefc_conf_lines.append(f"MAGMOM = {up_moments_string} {down_moments_string}")

    writefc_conf_lines.append("DIM = 1 1 1")
    writefc_conf_lines.append("FORCE_CONSTANTS = WRITE")
    writefc_conf_contents = "\n".join(writefc_conf_lines)

    return writefc_conf_contents


def make_force_constants(
    calc_dir: str, inputs_dir: str, use_upho: bool = False
) -> None:
    """Make FORCE_CONSTANTS file in calc_dir/postprocess

    Args:
        calc_dir (str): The path to calculation directory.
        inputs_dir (str): The path to inputs directory.
        use_upho (bool, optional): Whether to use UPHO or not. Defaults to False.
    """
    postprocess_dir_path = Path(calc_dir) / "postprocess"
    disp_set_dir_path = Path(calc_dir) / "disp_set"

    disp_dir_path_list = [
        disp_dir_path for disp_dir_path in disp_set_dir_path.glob("disp-???")
    ]
    for disp_dir_path in disp_dir_path_list:
        dest_dir_path = postprocess_dir_path / disp_dir_path.stem
        if not dest_dir_path.exists():
            dest_dir_path.mkdir(parents=True)

        src_path = disp_dir_path / "vasprun.xml"
        dest_path = dest_dir_path / "vasprun.xml"
        shutil.copy(src_path, dest_path)

    src_path = disp_set_dir_path / "phonopy_disp.yaml"
    dest_path = postprocess_dir_path / "phonopy_disp.yaml"
    shutil.copy(src_path, dest_path)

    os.chdir(postprocess_dir_path)
    cmd_args = ["phonopy", "-f"]
    vasprun_xml_list = [
        str(postprocess_dir_path / disp_dir_path.stem / "vasprun.xml")
        for disp_dir_path in disp_dir_path_list
    ]
    vasprun_xml_list.sort()
    cmd_args.extend(vasprun_xml_list)
    subprocess.run(cmd_args)

    content = make_writefc_conf(use_upho=use_upho)
    writefc_conf_path = postprocess_dir_path / "writefc.conf"
    with writefc_conf_path.open("w") as f:
        f.write(content)
    subprocess.run(["phonopy", "writefc.conf"])

    if use_upho:
        inputs_file_path_list = [file_path for file_path in Path(inputs_dir).glob("*")]
        for inputs_file_path in inputs_file_path_list:
            dest_path = postprocess_dir_path / inputs_file_path.name
            shutil.copy(inputs_file_path, dest_path)
        subprocess.run(["upho_weights", "band.conf", "--average_force_constants"])

        old_file_path = postprocess_dir_path / "FORCE_CONSTANTS"
        new_file_path = postprocess_dir_path / "FORCE_CONSTANTS_orig"
        old_file_path.rename(new_file_path)

        old_file_path = postprocess_dir_path / "FORCE_CONSTANTS_SPG"
        new_file_path = postprocess_dir_path / "FORCE_CONSTANTS"
        old_file_path.rename(new_file_path)

        old_poscar_path = postprocess_dir_path / "POSCAR"
        new_poscar_path = postprocess_dir_path / "POSCAR_one_specie"
        shutil.copy(old_poscar_path, new_poscar_path)

        with new_poscar_path.open("r") as f:
            lines = f.readlines()

        element = lines[5].split()[0]
        n_atoms = sum(map(int, lines[6].split()))
        new_lines = copy(lines)
        new_lines[5] = f"{element}\n"
        new_lines[6] = f"{n_atoms}\n"
        content = "".join(new_lines)

        with new_poscar_path.open("w") as f:
            f.write(content)
