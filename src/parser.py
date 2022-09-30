class SplitParser():
    """
    this parser gets string like <ip>|<timestamp><new line>
    and returns list like [ip, timestamp]
    """
    separator = "|"

    def __init__(self, datasource):
        """
        datasource must be iterable
        """

        self._datasource = datasource

    def __iter__(self):
        return self

    def __next__(self):
        line = self._datasource.next()
        if not line:
            return None
            
        parsed_line = line.strip().split(self.separator)
        return parsed_line


if __name__ == "__main__":
    from reader import ChunkReader

    logfile = "nginx_test_conf/log/access.log"


    reader = ChunkReader(logfile)
    parser = SplitParser(reader)

    print(parser.__next__())