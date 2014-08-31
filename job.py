class Job(object):
    id_seq = 0
    def next_id(self):
        Job.id_seq += 1
        return Job.id_seq

    def __init__(self, data, pri=1024, ttr=120, delay=0):
        self.id = self.next_id()
        self.pri = pri
        self.ttr = ttr
        self.delay = delay
        self.data = data
