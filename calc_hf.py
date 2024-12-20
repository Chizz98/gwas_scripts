#!/usr/bin/python3
import argparse as arg
from util import parse_tsv, write_tsv


def arg_reader():
    """ Reads arguments from command line

    :return class containing the arguments
    """
    arg_parser = arg.ArgumentParser(
        description="Calculates heterozygosity frequency per variant "
                    "from .frqx files"
    )
    arg_parser.add_argument(
        "infile",
        help="A .frqx file output by plink"
    )
    arg_parser.add_argument(
        "outfile",
        help="The prefix for the outfile"
    )
    arg_parser.add_argument(
        "-v",
        help="Verbose mode, prints progress if set",
        action="store_true"
    )
    return arg_parser.parse_args()


def calc_het_corr_freqs(line: list[str | int]) -> dict[str, str | int]:
    """ Calculates false heterozygote corrected missing and minor allele frequencies

    :param line: A parsed line from a .frqx file
    :return: dictionary containing variant id, het adjusted maf and het
        adjusted missing data
    """
    var_id = line[1]
    hom1 = int(line[4])
    het = int(line[5])
    hom2 = int(line[6])
    missing = int(line[9])

    missing_f = missing / (hom1 + hom2 + het + missing)
    het_adjusted_missing_f = (het + missing) / (hom1 + hom2 + het + missing)
    minor_hom = min(hom1, hom2)

    # If only missing, set maf to NA
    maf = "NA" if missing_f == 1 else (minor_hom * 2 + het) / ((hom1 + hom2 + het) * 2)
    # If only missing, set het_f to NA
    het_f = "NA" if missing_f == 1 else het / (hom1 + hom2 + het)
    # If only het and missing, set corrected maf to NA
    het_adjusted_maf = "NA" if het_adjusted_missing_f == 1 else minor_hom * 2 / ((hom1 + hom2) * 2)
    return {"ID": var_id, "CORR_MAF": het_adjusted_maf, "MAF": maf,
            "CORR_MISS_FRQ": het_adjusted_missing_f, "MISS_FRQ": missing_f,
            "HET_FRQ": het_f}


def main():
    """ main function """
    args = arg_reader()
    freq_gen = parse_tsv(args.infile)
    freqs = []
    if args.v:
        for i, line in enumerate(freq_gen):
            print(f"processing line {i}", end="\r")
            freqs.append(calc_het_corr_freqs(line))
        print("all lines processed\nwriting outfile")
    else:
        for line in freq_gen:
            freqs.append(calc_het_corr_freqs(line))
    write_tsv(args.outfile, freqs)


if __name__ == "__main__":
    main()
