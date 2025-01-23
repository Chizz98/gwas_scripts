import pandas as pd
import numpy as np


def main():
    pheno_of_interest = 6
    fam_file = "LKser_bed_files_v4.fam"

    fam_file = pd.read_table(fam_file, header=None)
    fam_base = fam_file.iloc[:, 0:5]
    phenotype_col = fam_file.iloc[:, pheno_of_interest].copy()
    non_na = phenotype_col.dropna().tolist()

    for i in range(10):
        np.random.shuffle(non_na)
        phenotype_col.loc[phenotype_col.notna()] = non_na
        fam_base = pd.concat([fam_base, phenotype_col], axis=1)

    fam_base.to_csv("out.fam", sep="\t", header=False, index=False, na_rep="NA")


if __name__ == "__main__":
    main()

