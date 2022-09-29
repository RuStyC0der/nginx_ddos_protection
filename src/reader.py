from time import sleep

class SplitReader():
    """
    line by line reader
    it reads file then splits with separator and returns tuple

    """

    # read from end of file
    last_lines_to_read_count = 100000
    separator = "/"

    def __init__(self, target_file, read_from_begin=False):
        pass

file_path = "access.log"

with open(file_path, "rt") as f:
    print(f.tell())
    f.seek(0, 2)
    print(f.tell())