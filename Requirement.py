class Requirement:

    def __init__(self,func = None, state = None):
        self.state = state
        self.validation_function = func

    def satisfied(self):
        return self.validation_function(self.state)
