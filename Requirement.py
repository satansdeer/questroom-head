class Requirement:

    state = None
    validation_fuction = None

    def satisfied(self):
        return self.validation_function(self.state)
