
class Memory(object):
    def __init__(self, id=0, name="0", size=0):
        self.id = id
        self.name = name
        self.size = size
        self.process = None
        self.fragmentation = 0

    def reset(self):
        self.process = None
        self.fragmentation = 0

    def get_frag(self):
        if self.process:
            return self.size - self.process.size
        return 0

    def display_fragmentation(self):
        if self.process:
            return str(self.size - self.process.size) + "K"
        return "0K"

    def to_string(self):
        return self.name + " (" + str(self.size) + "K)"

    def current_process(self):
        if self.process:
            return self.process.name + " (" + str(self.process.size) + "K)"

        return "FREE"

    def decrease_process_time(self):
        if self.process.counter == 0:
            self.process = None
            return

        self.process.decrease_time()

    def current_process_time(self):
        if self.process:
            return str(self.process.counter) + " ms"

        return "FREE"

