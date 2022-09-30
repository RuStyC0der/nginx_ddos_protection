from time import sleep, time
import os


class SplitReader():
    """
    line by line reader
    it reads file then splits with separator and returns tuple
    """

    # read from end of file
    last_bytes_to_read_count = 100000
    separator = "/"

    def __init__(self, target_file, read_from_begin=False):
        if os.path.isfile(target_file) and os.access(target_file, os.R_OK):
            self.file = target_file
        else:
            raise IOError("file not exist or not readable")
        


    def _tail(self, lines=15000, _buffer=4096):
        """Tail a file and get X lines from the end"""
        with open(self.file, 'rt') as f:
            lines_found = []
            f.seek(0, 2)
            position = f.tell() - _buffer
            while (len(lines_found) < lines) and position >= 0:
                f.seek(position)
                got_lines = f.read(_buffer).split('\n')[1:-1]
                lines_found = got_lines + lines_found
                
                position -= _buffer

            return lines_found[-lines:]



if __name__ == '__main__':
    rd = SplitReader("nginx_test_conf/log/access.log")
    t1 = time()
    print(rd._tail())
    print (time() - t1)