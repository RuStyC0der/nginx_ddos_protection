from time import sleep
import os

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


    def tail(f, lines=15, _buffer=4098):
        """Tail a file and get X lines from the end"""
        lines_found = []

        block_counter = -1
        while len(lines_found) < lines:
            try:
                f.seek(block_counter * _buffer, os.SEEK_END)
            except IOError:  # either file is too small, or too many lines requested
                f.seek(0)
                lines_found = f.readlines()
                break

            lines_found = f.readlines()
            block_counter -= 1

        return lines_found[-lines:]
