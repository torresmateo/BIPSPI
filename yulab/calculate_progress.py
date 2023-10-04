import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger('calculate_progress')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    "%Y-%m-%d %H:%M:%S")
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


def run(outdir: Path, pairs: Path) -> None:
    assert outdir.exists(), "output directory does not exist"
    assert pairs.is_file(), "PDB pairs is not a file"

    # for now, we simply care about the number of items.
    unique_pairs = set()
    with pairs.open() as p:
        for line in p:
            unique_pairs.add(line.strip())

    tot = len(unique_pairs)

    finished = 0
    predir = outdir / "preds" / "struct"
    times = []
    time_diffs = []
    for f in sorted(predir.glob("*.lig.gz"),
                    key=lambda f: f.stat().st_mtime):
        finished += 1
        times.append(f.stat().st_mtime)
        if finished > 1:
            time_diffs.append(times[-1] - times[-2])

    tt_sec = times[-1] - times[0]
    tt_min = tt_sec/60
    tt_hou = tt_min/60

    t_mea = np.mean(time_diffs)
    t_med = np.median(time_diffs)
    t_min = np.min(time_diffs)
    t_max = np.max(time_diffs)

    logger.info(f"Progress = {finished}/{tot} ({finished/tot*100.0:.2f}%)")
    logger.info(f"Time/exp  mean   = {t_mea:.2f} s ({t_mea/60:.2f} m)")
    logger.info(f"          median = {t_med:.2f} s ({t_med/60:.2f} m)")
    logger.info(f"          min    = {t_min:.2f} s ({t_min/60:.2f} m)")
    logger.info(f"          max    = {t_max:.2f} s ({t_max/60:.2f} m)")
    logger.info(f"          total  = {tt_sec:.2f} s"
                f" ({tt_min:.2f} m) ({tt_hou:.2f} h)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Reads Yulab's PDBs and prepares the files for BIPSPI+")
    parser.add_argument("-o", "--output-dir", required=True,
                        help="A path to write the renamed PDB files")
    parser.add_argument("-p", "--pdb-pairs", required=True,
                        help="A text file containing a pair of PDB IDs"
                             " per line separated by a + sign, the first will"
                             " be used as the ligand, the second as the"
                             " receptor")
    args = parser.parse_args()
    run(Path(args.output_dir),
        Path(args.pdb_pairs))
