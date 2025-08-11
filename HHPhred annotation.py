import os
import re

folder_path = 'FAA_phrog'

test_hypothetical = 'MTRYNAPKLGKYLTIFGFCAFFSVIIGAIVWGILDMKKQQVEEEKLVKFLDTYCEVVEYGLNKKPTKYSCDQVIFNVK'
# List all files in the folder
files = os.listdir(folder_path)
hypothetical_dictionary = {}
with open('hypotheticals_26a_C.txt', 'r') as file:
    sequences = file.read()
    sequence_list = re.findall(r' ([^\s]+)\n', sequences)
    print(sequence_list)

for sequence in sequence_list:
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)

    # Check if the file is a regular file (not a folder)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                # Read the contents of the file
                contents = file.read()
                if sequence in str(contents):
                    hypothetical_dictionary[sequence] = file_name
                    with open("hypothetical_pred.txt", 'a') as output_file:
                        output_file.write(sequence + ': ' + file_name +'\n')
                else:
                    continue

