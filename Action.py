class Action:

    function_to_perform = None

    def perform(self):
        if not self.function_to_perform: return
        self.function_to_perform()
