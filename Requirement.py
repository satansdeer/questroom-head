class Requirement:

    state = None
    validation_fuction = None

    def __init__(self,func = None):
        self.validation_function = func

    def satisfied(self):
        return self.validation_function(self.state)
