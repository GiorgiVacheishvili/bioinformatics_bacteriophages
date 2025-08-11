import re

x = input("write the embl file name with the extension: ")
locus_tag = input("write locus tag name: ")

with open(x, "r") as embl_file:
    text = embl_file.read()


    def replace_locus_tags(text):
        # Pattern to match /locus_tag and capture the digits
        pattern = r'/locus_tag="[a-zA-Z0-9_]+-(\d{3})"'

        # Find all matches
        matches = list(re.finditer(pattern, text))

        # Initialize the replacement counter
        new_number = 1  # Start from 001

        # Create a new result list to build the modified text
        result = []
        last_index = 0  # Track the last index where we added to the result

        # Replace each matched locus tag with a new tag
        count = 0  # Initialize a counter

        for match in matches:
            # Add text before the current match
            result.append(text[last_index:match.start()])

            # Create the new locus tag with the formatted number for every match
            new_locus_tag = f'/locus_tag="{locus_tag}-{new_number:03}"'  # Format as three digits
            result.append(new_locus_tag)

            # Update the last index
            last_index = match.end()

            count += 1  # Increment the counter

            # Increment the new number for every two matches
            if count % 2 == 0:
                new_number += 1

        # Add any remaining text after the last match
        result.append(text[last_index:])

        return ''.join(result)


    with open(f"{locus_tag}.embl", 'w') as new_embl:
        new_embl.write(replace_locus_tags(text))