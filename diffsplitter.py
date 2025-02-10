import argparse
import os
import re

def split_diff(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r") as f:
        diff_content = f.readlines()

    current_file = None
    file_data = {}

    # Regex for matching the diff header line and capturing the appropriate groups
    diff_header_pattern = r"^diff\s+(\-rupN|\-Nur)?\s*(\S+)\s+(\S+)"
    
    for line in diff_content:
        match = re.match(diff_header_pattern, line)
        if match:
            diff_type = match.group(1)  # Will capture either '-rupN' or '-Nur'
            current_file = match.group(2)  # The second part of the diff (file path)
            
            # Initialize the file data with the diff type as key
            if current_file not in file_data:
                file_data[current_file] = {'type': diff_type, 'lines': []}

        if current_file:
            file_data[current_file]['lines'].append(line)

    for file_path, data in file_data.items():
        diff_type = data['type']
        diff_lines = data['lines']

        # Handle different diff formats based on the diff type
        if diff_type == "-Nur":
            output_file = os.path.join(output_dir, f"{file_path}.diff")
        elif diff_type == "-rupN":
            # Handle splitting for '-rupN' differently
            output_file = os.path.join(output_dir, f"{file_path}.rupn.diff")

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, "w") as f:
            f.writelines(diff_lines)

        print(f"Created: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="DiffSplitter splits and organizes diff files.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input diff file.")
    parser.add_argument("-o", "--output", help="Path to the output directory (optional).")

    args = parser.parse_args()

    input_file = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.output) if args.output else os.path.join(os.getcwd(), "output")

    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")

    split_diff(input_file, output_dir)

if __name__ == "__main__":
    main()
