class Requirement:

    def __init__(self,func = None, state = None):
        self.state = state
        self.validation_function = func

    def satisfied(self, master, state):
        return self.validation_function(master, state)
