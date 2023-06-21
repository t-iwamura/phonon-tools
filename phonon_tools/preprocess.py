import os
import shutil
import subprocess
from copy import copy
from pathlib import Path


def make_disp_conf(use_upho: bool = False) -> str:
    """Make content of disp.conf

    Args:
        use_upho (bool, optional): Whether to use UPHO or not. Defaults to False.

    Returns:
        str: The content of disp.conf
    """
    disp_conf_lines = []
    if use_upho:
        up_moments = ["5.0" for _ in range(16)]
        down_moments = ["-5.0" for _ in range(16)]

        up_moments_string = " ".join(up_moments)
        down_moments_string = " ".join(down_moments)
        disp_conf_lines.append(f"MAGMOM = {up_moments_string} {down_moments_string}")

    disp_conf_lines.append("DIM = 1 1 1")
    disp_conf_content = "\n".join(disp_conf_lines)

    return disp_conf_content


def arrange_disp_set_dir(
    calc_dir: str, inputs_dir: str, use_upho: bool = False, use_mlp: bool = False
) -> None:
    """Arrange disp_set directory

    Args:
        calc_dir (str): Path to calculation directory.
        inputs_dir (str): Path to inputs directory.
        use_upho (bool, optional): Whether to use UPHO or not. Defaults to False.
        use_mlp (bool, optional): Whether to use machine learning potential or not.
            Defaults to False.
    """
    calc_dir_path = Path(calc_dir)
    disp_set_dir_path = calc_dir_path / "disp_set"
    if not disp_set_dir_path.exists():
        disp_set_dir_path.mkdir()

    relaxed_poscar_path = calc_dir_path / "relax" / "POSCAR"
    input_poscar_path = disp_set_dir_path / "POSCAR"
    shutil.copyfile(relaxed_poscar_path, input_poscar_path)

    content = make_disp_conf(use_upho)
    disp_conf_path = disp_set_dir_path / "disp.conf"
    with disp_conf_path.open("w") as f:
        f.write(content)

    os.chdir(disp_set_dir_path)
    subprocess.run(["phonopy", "-d", "disp.conf"])

    for poscar_path in disp_set_dir_path.glob("POSCAR-???"):
        poscar_id = poscar_path.stem.split("-")[-1]
        disp_dir_path = disp_set_dir_path / f"disp-{poscar_id}"
        disp_dir_path.mkdir()
        new_poscar_path = disp_dir_path / "POSCAR"
        shutil.move(poscar_path, new_poscar_path)

        if use_mlp:
            continue

        incar_src_path = Path(inputs_dir) / "INCAR"
        incar_path = disp_dir_path / "INCAR"
        shutil.copyfile(incar_src_path, incar_path)

        kpoints_src_path = Path(inputs_dir) / "KPOINTS"
        kpoints_path = disp_dir_path / "KPOINTS"
        shutil.copyfile(kpoints_src_path, kpoints_path)

        potcar_src_path = Path(inputs_dir) / "POTCAR"
        potcar_path = disp_dir_path / "POTCAR"
        shutil.copyfile(potcar_src_path, potcar_path)

        if not use_upho:
            continue

        with new_poscar_path.open("r") as f:
            old_poscar_lines = [line.strip() for line in f]

        new_poscar_lines = copy(old_poscar_lines)
        symbol = old_poscar_lines[5]
        new_poscar_lines[5] = f"{symbol} {symbol}"
        n_atoms_half = int(old_poscar_lines[6]) // 2
        new_poscar_lines[6] = f"{n_atoms_half} {n_atoms_half}"

        with new_poscar_path.open("w") as f:
            f.write("\n".join(new_poscar_lines))
