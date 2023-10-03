from pathlib import Path
from typing import Tuple
from rich.progress import track
import logging
import shutil


logger = logging.getLogger('prepare_test_data')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    "%Y-%m-%d %H:%M:%S")
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


def translate_ids(pdb_pair: str) -> Tuple[str]:
    """
    From a line with 2 PDB ids separated by a + sign, returns a tuple of
    UIDs that can be used for BIPSPI+ without it parsing the name incorrectly.

    Parameters
    ----------
    pdf_pair : str
        A pair of PDB IDs separated by a + sign

    Return
    ------
    Tuple[str]
        uuid, ligand, receptor, translated_ligand, translated_receptor
    """
    ligand, receptor = pdb_pair.split("+")
    t_ligand = ligand.replace("_", "-")
    t_receptor = receptor.replace("_", "-")
    uid = f"{t_ligand}--{t_receptor}"
    return uid, ligand, receptor, t_ligand, t_receptor


def run(indir: Path, outdir: Path, pairs: Path) -> None:
    assert indir.exists(), "input directory does not exist"
    assert pairs.is_file(), "PDB pairs is not a file"
    if not outdir.exists():
        outdir.mkdir(parents=True)

    logger.info("processing pairs file")
    # list of PDB pairs (ligand, receptor)
    pdb_pairs = []
    uids = set()
    rep = 0
    with pairs.open() as p:
        for line in p:
            pdb_pairs.append(translate_ids(line.strip()))
            uid = pdb_pairs[-1][0]
            if uid in uids:
                logger.info("repeated")
                rep += 1
            uids.add(uid)
    logger.info(f"repeated {rep=}")

    for (uid, ligand, receptor,
         t_ligand, t_receptor) in track(pdb_pairs,
                                        description="Renaming files"):
        f_ligand = indir / f"{ligand}.pdb"
        if not f_ligand.exists():
            logger.warn(f"{ligand} not found in {indir}"
                        f" ignoring pair: {ligand} {receptor}")
            continue
        f_receptor = indir / f"{receptor}.pdb"
        if not f_receptor.exists():
            logger.warn(f"{receptor} not found in {indir}"
                        f" ignoring pair: {ligand} {receptor}")
            continue
        #shutil.copy(f_ligand, outdir / f"{uid}_l_u.pdb")
        #shutil.copy(f_receptor, outdir / f"{uid}_r_u.pdb")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Reads Yulab's PDBs and prepares the files for BIPSPI+")
    parser.add_argument("-i", "--input-dir", required=True,
                        help="A directory containing PDF files")
    parser.add_argument("-o", "--output-dir", required=True,
                        help="A path to write the renamed PDB files")
    parser.add_argument("-p", "--pdb-pairs", required=True,
                        help="A text file containing a pair of PDB IDs"
                             " per line separated by a + sign, the first will"
                             " be used as the ligand, the second as the"
                             " receptor")
    args = parser.parse_args()
    run(Path(args.input_dir),
        Path(args.output_dir),
        Path(args.pdb_pairs))
