import os

def count_lines_of_code(directory, extension=".py"):
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    total_lines += sum(1 for line in f)
    return total_lines

folder_path = '../n2p2od'
total_lines = count_lines_of_code(folder_path)
print(f"Total lines of code in '{folder_path}': {total_lines}")

