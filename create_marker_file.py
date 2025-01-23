#!/usr/bin/python3
import argparse as arg
from .util import parse_tsv, write_tsv


def arg_reader():
    """ Reads arguments from command line

    :return class containing the arguments
    """
    arg_parser = arg.ArgumentParser(
        description="Create a markerfile for visualization with "
                    "chromMap R package"
    )
    arg_parser.add_argument(
        "infile",
        help="A .bim file output by plink"
    )
    arg_parser.add_argument(
        "outfile",
        help="The name of the outfile"
    )
    arg_parser.add_argument(
        "-v",
        help="Verbose mode, prints progress if set",
        action="store_true"
    )
    return arg_parser.parse_args()


def format_markers(line: list[str | int]) -> dict[str, str | int]:
    """ Formats lines from a .bim file into input for R package chromMap

    :param line: a parsed line from a .bim file
    :return: Dictionary containing ...
    """
    chr_id = line[0]
    var_id = line[1]
    var_start = int(line[3])
    var_end = var_start
    return {"VAR_ID": var_id, "CHR_ID": chr_id, "START": var_start,
            "END": var_end}


def main():
    """ main function """
    args = arg_reader()
    bim_lines = parse_tsv(args.infile)
    out_lines = []
    if args.v:
        for i, line in enumerate(bim_lines):
            print(f"processing line {i}", end="\r")
            out_lines.append(format_markers(line))
        print("all lines processed\nwriting outfile")
    else:
        for line in bim_lines:
            out_lines.append(format_markers(line))
    write_tsv(args.outfile, out_lines)


if __name__ == "__main__":
    main()
