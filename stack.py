class Stack():
    def __init__(self):
        self.stek = []

    def size(self):
        return len(self.stek)

    def peek(self):
        return self.stek[-1]

    def pop(self):
        if self.stek:
            return self.stek.pop()

    def push(self, element):
        self.stek.append(element)

    def is_empty(self):
        return not self.stek

