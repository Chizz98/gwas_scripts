#!/usr/bin/python3
import pandas as pd
import numpy as np
import argparse as arg
import os


def arg_reader():
    """ Reads arguments from command line

    :return class containing the arguments
    """
    arg_parser = arg.ArgumentParser(
        description="Goes trough a GEMMA output folder and writes a file with the "
                    "lowest p_wald and highest -log10p of each file to top_vars.txt"
                    "in the same dir"
    )
    arg_parser.add_argument(
        "in_dir",
        help="The directory containing the assoc files"
    )
    return arg_parser.parse_args()


def main():
    args = arg_reader()

    assoc_dir = args.in_dir
    assoc_filenames = [file for file in os.listdir(assoc_dir) if file.endswith(".assoc.txt")]
    out_file = "top_vars.txt"

    out_lines = [("min_p_wald", "max_log10")]
    for i, filename in enumerate(assoc_filenames):
        print(f"parsing {i + 1} of {len(assoc_filenames)}", end="\r", flush=True)
        path = os.path.join(assoc_dir, filename)
        gemma_output = pd.read_table(path, sep=r"\s+")
        min_p = gemma_output.loc[:, "p_wald"].min()
        max_log10 = -1 * np.log10(min_p)
        out_lines.append((str(min_p), str(max_log10)))

    with open(out_file, "w") as outfile:
        for line in out_lines:
            outfile.write("\t".join(line) + "\n")


if __name__ == "__main__":
    main()
