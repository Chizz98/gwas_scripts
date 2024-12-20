from typing import Generator


def parse_tsv(filename: str) -> Generator[list[str, ...], None, None]:
    """ Parses a tsv file and generates the output line by line

    :param filename: the filename of the .tsv file
    :return: generator returning one line at a time as a list of
        str
    """
    infile_conn = open(filename, "r")
    # Skip header line
    infile_conn.readline().strip().split("\t")
    for line in infile_conn:
        line = line.strip().split("\t")
        yield line
    infile_conn.close()


def write_tsv(outfile: str, lines: list[dict], write_head=True) -> None:
    """ Writes a tsv from a dictionary

    :param outfile: The name of the outfile
    :param lines: the lines to write as dictionaries with headers as key and
        value as value
    :param write_head: If true writes dict keys as first line, started with a #
    :return: None, writes outfile
    """
    outfile_conn = open(outfile, "w")
    if write_head:
        headers = lines[0].keys()
        outfile_conn.write("#" + "\t".join(headers) + "\n")
    for line in lines:
        if line["ID"] != ".":
            values = [str(val) for val in line.values()]
            outfile_conn.write("\t".join(values) + "\n")
    outfile_conn.close()
