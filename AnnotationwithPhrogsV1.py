import re
import textwrap
import pandas as pd

TRANSLATION_TABLE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
}

x = input("Write the 'Genemarks' file name with txt extension: ")
y = input("Write the Fasta file name with fasta extension, containing whole genome: ")
z = input("Write the locus tag: ")
a = input("Write the phrog matches' file name: ")
b = input("Write the phrog table file name: ")


def identified_phrogs(matches_file):
    """create a list from the found genes on Linux(This icludes GENE NUMBER, PHROG NUMBER and PHROG PROB"""
    with open(matches_file, "r") as identified_phrogs_file:
        pattern = r'Query.*?(?=\n\nNo 1)'
        identified_phrog_list = re.findall(pattern, identified_phrogs_file.read(), re.DOTALL)
    return identified_phrog_list


IDENTIFIED_PHROG_LIST = identified_phrogs(a)


def phrog_table(phrog_file):
    """creates a dataframe from the phrog table, PROTEIN NAME can be searched with a known PHROG NUMBER"""
    phrog_dataframe = pd.read_csv(phrog_file, sep='\t')
    return phrog_dataframe


PHROG_TABLE = phrog_table(b)


def search_protein_in_phrogs(gene_number):
    print(gene_number)
    protein = "hypothetical protein"
    for identified_phrog in IDENTIFIED_PHROG_LIST:
        #print(identified_phrog)
        if f"gene_{gene_number}\n" in identified_phrog:
            #print(identified_phrog)
            number_of_lines = len(identified_phrog.split("\n"))
            for i in range((number_of_lines-9), 1, -1):
                phrog_line = identified_phrog.split("\n")[-i].split()
                print(phrog_line)
                phrog_number = phrog_line[1][6:]
                try:
                    prob = float(phrog_line[4])
                    #score = float(phrog_line[7])

                except ValueError:
                    prob = float(phrog_line[5])
                    #score = float(phrog_line[8])
                if prob < 90.0:
                    #or score < 100.0):
                    #print(prob)
                    #print(score)
                    print("\n\n")
                    return protein
                protein_initial = PHROG_TABLE.loc[PHROG_TABLE["phrog"] == int(phrog_number), "annot"].values[0]
                if not pd.isna(protein_initial) and (protein_initial != "unknown function") and protein != "None":
                    protein = protein_initial
                if pd.isna(protein_initial) or (protein_initial == "unknown function"):
                    protein = "hypothetical protein"
                    continue
                print("\n\n")
                return protein


def embl_generator(genemarks_file, fasta_file, locus_tag):
    """Generates an embl file with information about its genes and the proteins the genes synthesize."""
    with open(genemarks_file, "r") as source_file:
        content = source_file.read()
        split_content = content.split("\n\n")
        if split_content[-1] == '\n':
            split_content = split_content[:-1]
        with open(f"{locus_tag}.embl", "w") as embl_file:
            pattern = r"\d+\|\d+"
            for gene in split_content:
                #print(gene)
                info_tuple = ()
                if "+" in gene:
                    match = re.findall(pattern, gene)
                    new_match = match[0].replace("|", "..")
                    # print(new_match)
                    info_tuple += (f"{new_match}",)
                    # print(info_tuple[0])
                elif "-" in gene:
                    match = re.findall(pattern, gene)
                    new_match = match[0].replace("|", "..")
                    info_tuple += (f"complement({new_match})",)
                    # print(info_tuple)
                lines = gene.split('\n')
                nucleotide_sequence = ''.join(lines[1:])
                amino_acid_sequence = ''.join(
                    TRANSLATION_TABLE[nucleotide_sequence[i:i + 3]] for i in
                    range(0, len(nucleotide_sequence), 3)).replace("*", "")
                info_tuple += (amino_acid_sequence,)
                if info_tuple == (" ",) or info_tuple == ("",):
                    continue
                gene_number = split_content.index(gene) + 1
                #print(gene_number)
                protein = search_protein_in_phrogs(gene_number)
                #print(protein)
                embl_content = f"""FT   gene            {info_tuple[0]}
FT                   /locus_tag="{locus_tag + "-" + str(split_content.index(gene) + 1).zfill(3)}"
FT   CDS             {info_tuple[0]}
FT                   /locus_tag="{locus_tag + "-" + str(split_content.index(gene) + 1).zfill(3)}"
FT                   /codon_start=1
FT                   /transl_table=11
FT                   /product="{protein}"
{textwrap.fill(info_tuple[1], width=79, initial_indent='FT                   /translation="', subsequent_indent=
                'FT                   ')}"
"""
                embl_file.write(embl_content)
            with open(fasta_file, 'r') as fast_file:
                embl_file.write(fast_file.read())


embl_generator(x, y, z)
