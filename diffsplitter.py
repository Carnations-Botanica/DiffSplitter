import argparse
import os
import re

def split_diff(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r") as f:
        diff_content = f.readlines()

    current_file = None
    file_data = {}

    for line in diff_content:
        match = re.match(r"^diff\s+\-Nur\s+\S+\s+(\S+)", line)
        if match:
            current_file = match.group(1)
            file_data[current_file] = []
        if current_file:
            file_data[current_file].append(line)

    for file_path, diff_lines in file_data.items():
        output_file = os.path.join(output_dir, f"{file_path}.diff")
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
