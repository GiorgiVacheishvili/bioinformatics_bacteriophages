import re

with open('67t1t2_cov_959.139223 fasta.fasta', "r") as file:
    sequences = {}
    current_sequence = ""
    for line in file:
        line = line.strip()
        if line.startswith(">"):
            current_sequence = line[1:]  # Remove the ">" character
            sequences[current_sequence] = ""
        else:
            sequences[current_sequence] += line

with open("WholeSequence_1.txt", "w") as output_file:
    for dummy_key, value in sequences.items():
        output_file.write(value + '\n\n\n\n\n')
        whole_sequence = value

START_CODONS = ["ATG", "GTG", "TTG"]
STOP_CODONS = ["TAG", "TGA", "TAA"]
# Define a regular expression pattern

exact_matches = []
for start in START_CODONS:
    for stop in STOP_CODONS:
        pattern = re.escape(start) + r".*?" + re.escape(stop)
        matches = re.findall(pattern, whole_sequence)
        for match in matches:
            if len(match)>100 and len(match)< 176500:
                exact_matches.append(match)

with open("exact matches.txt", "w") as output_file_1:
    for i in range(len((exact_matches))):
        output_file_1.write("\n" + str(i) + ": " + exact_matches[i])



