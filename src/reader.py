from time import sleep, time
import os


class SplitReader():
    """
    chunk reader
    it reads file then splits with separator and returns tuple
    """

    # read from end of file
    separator = "/"
    lines_per_chunk = 500

    buffered_lines = []

    def __init__(self, target_file, last_bytes_to_read_count=100000):
        if os.path.isfile(target_file) and os.access(target_file, os.R_OK):
            self.file = target_file
            self.buffered_lines = self._tail(last_bytes_to_read_count)
        else:
            raise IOError("file not exist or not readable")
        


    def _tail(self, lines=150, _buffer=8192):
        """Tail a file and get X lines from the end"""
        with open(self.file, 'rt') as f:
            lines_found = []
            f.seek(0, 2)
            self.end_position = f.tell()
            position = self.end_position - _buffer
            while (len(lines_found) < lines) and position >= 0:
                f.seek(position)
                got_lines = f.read(_buffer).split('\n')[1:-1]
                lines_found = got_lines + lines_found
                
                position -= _buffer
            
            return lines_found[-lines:]

    def load_chunk(self):
        with open(self.file, 'rt') as f:
            f.seek(self.end_position)
            got_lines = f.readlines(self.lines_per_chunk)
            self.buffered_lines.extend(got_lines)
            self.end_position = f.tell()
    def __iter__(self):
        return self

    def __next__(self):
        if (len(self.buffered_lines) <= self.lines_per_chunk / 2):
            self.load_chunk()
        try:
            return self.buffered_lines.pop(0)
        except IndexError:
            return None

if __name__ == '__main__':
    rd = SplitReader("nginx_test_conf/log/access.log", 5)
    for i in rd:
        print(i)
        sleep(1)
    # rdi = rd.__iter__()
    # for i in range(100):
    #     print(rdi.__next__())