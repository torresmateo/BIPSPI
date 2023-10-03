from pathlib import Path


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
