
class Log(object):
    """Logs data into csv files"""
    def __init__(self, filename, head):
        self.filename = filename
        self.logfile = open(filename, 'w')
        self.write_items(head)
    def write_items(self, items):
        line = ', '.join([str(item) for item in items])
        self.logfile.write(line)
        self.logfile.write('\n')
    def close(self):
        self.logfile.close()


