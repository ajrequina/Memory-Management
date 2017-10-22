
class Job(object):
    def __init__(self, id=0, name="0", time=0, size=0):
        self.id = id
        self.name = name
        self.time = time
        self.size = size
        self.memory = None
        self.waiting_time = 0
        self.counter = time

    def reset(self):
        self.memory = None
        self.waiting_time = 0
        self.counter = 0

    def get_rem_time(self):
        if self.counter:
            return str(self.counter) + " ms"
        return "FREE"

    def waiting_time_value(self):
        return self.waiting_time - 1

    def wait(self):
        if not self.memory:
            self.waiting_time += 1

    def get_waiting_time(self):
        return str(self.waiting_time - 1) + " ms"

    def decrease_time(self):
        if self.counter > 0:
            self.counter -= 1

    def to_string(self):
        return self.name + " (" + str(self.size) + "K) - " + str(self.time) + " ms"
