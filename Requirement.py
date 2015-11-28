class Requirement:

    def __init__(self,func = None, state = None):
        self.state = 0
        self.validation_function = func

    def satisfied(self, master, state, game_state):
        value = self.validation_function(master, self.state, game_state)

        if isinstance(value, bool):
            return value
         # print("Reuirement: value:", value)
        self.state = value
        return False
