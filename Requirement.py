class Requirement:

    def __init__(self,func = None, state = None):
        self.state = 0
        self.validation_function = func

    def satisfied(self, master, task, game_state):
        value = self.validation_function(master, task, game_state)
	value = bool(value)
        if isinstance(value, bool):
            return value
         # print("Reuirement: value:", value)
        task.state = value
        return False
