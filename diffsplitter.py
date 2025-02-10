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

def split_si_diff(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r") as f:
        diff_content = f.readlines()

    current_file = None
    original_lines = []
    modified_lines = []
    original_file_data = {}
    modified_file_data = {}

    for line in diff_content:
        match = re.match(r"^diff\s+\-(Nur|rupN)\s+\S+\s+(\S+)", line)
        if match:
            if current_file:
                original_file_data[current_file] = original_lines
                modified_file_data[current_file] = modified_lines

            current_file = match.group(1)
            original_lines = []
            modified_lines = []

        elif line.startswith("-"):
            original_lines.append(line)  # Original lines (deletions)

        elif line.startswith("+"):
            modified_lines.append(line)  # Modified lines (additions)

        else:
            original_lines.append(line)  # Keep unchanged lines in original

    if current_file:
        original_file_data[current_file] = original_lines
        modified_file_data[current_file] = modified_lines

    # Write the original and modified files
    for file_path, orig_lines in original_file_data.items():
        orig_file_path = os.path.join(output_dir, f"{file_path}")
        os.makedirs(os.path.dirname(orig_file_path), exist_ok=True)

        with open(orig_file_path, "w") as f:
            f.writelines(orig_lines)
        print(f"Created: {orig_file_path}")

    for file_path, mod_lines in modified_file_data.items():
        mod_file_path = os.path.join(output_dir, f"{file_path}.modified")
        os.makedirs(os.path.dirname(mod_file_path), exist_ok=True)

        with open(mod_file_path, "w") as f:
            f.writelines(mod_lines)
        print(f"Created: {mod_file_path}")

def main():
    parser = argparse.ArgumentParser(description="DiffSplitter splits and organizes diff files.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input diff file.")
    parser.add_argument("-o", "--output", help="Path to the output directory (optional).")
    parser.add_argument("-si", "--split-indep", action="store_true", help="Split independent diff files.")

    args = parser.parse_args()

    input_file = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.output) if args.output else os.path.join(os.getcwd(), "output")
    if args.split_indep:
        output_dir = os.path.join(os.getcwd(), "single_output")  # Default to single_output for SI mode

    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")

    if args.split_indep:
        split_si_diff(input_file, output_dir)
    else:
        split_diff(input_file, output_dir)

if __name__ == "__main__":
    main()
