class Action:

    def __init__(self,func = None):
        self.function_to_perform = func

    def perform(self, master, state):
        if not self.function_to_perform: return
        self.function_to_perform(master, state)
