import pandas as pd
import numpy as np
import argparse as arg


def arg_reader():
    """ Reads arguments from command line

    :return class containing the arguments
    """
    arg_parser = arg.ArgumentParser(
        description="Takes a .fam file and permutes the specified phenotype, keeping NAs"
                    "in the same position"
    )
    arg_parser.add_argument(
        "infile",
        help="A .fam file"
    )
    arg_parser.add_argument(
        "phenotype",
        help="The phenotype to permute, with 1 being the first phenotype column",
        type=int
    )
    arg_parser.add_argument(
        "permute_n",
        help="The number of permutations to make",
        type=int
    )
    arg_parser.add_argument(
        "out_name",
        help="The prefix of the outfile"
    )
    return arg_parser.parse_args()


def main():
    args = arg_reader()

    pheno_of_interest = 4 + args.phenotype
    fam_file = args.infile
    n_permute = args.permute_n
    out_name = args.out_name

    fam_file = pd.read_table(fam_file, header=None, sep="\s+")
    fam_base = fam_file.iloc[:, 0:5]
    phenotype_col = fam_file.iloc[:, pheno_of_interest].copy()
    non_na = phenotype_col.dropna().tolist()

    for i in range(n_permute):
        np.random.shuffle(non_na)
        phenotype_col.loc[phenotype_col.notna()] = non_na
        fam_base = pd.concat([fam_base, phenotype_col], axis=1)

    fam_base.to_csv(out_name + ".fam", sep="\t", header=False, index=False, na_rep="NA")


if __name__ == "__main__":
    main()

