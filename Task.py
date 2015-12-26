class Task:

    def __init__(self):
        self.success_requirements = []
        self.failure_requirements = []
        self.success_actions = []
        self.failure_actions = []
        self.showOnMonitor = False
        self.state = 0
        self.type = None


    def success_requirements_satisfied(self, master, state, game_state):
        
        # print("Task in self class Task succ req: {}".format(self)) 
        if not self.success_requirements: return False
        return all(requirement.satisfied(master, self, game_state) for requirement in self.success_requirements)


    def failure_requirements_satisfied(self, master, state, game_state):
        if not self.failure_requirements: return False
        return all(requirement.satisfied(master, self, game_state) for requirement in self.failure_requirements)


    def add_success_requirement(self, requirement):
        self.success_requirements.append(requirement)


    def add_failure_requirement(self, requirement):
        self.failure_requirements.append(requirement)


    def add_success_action(self, action):
        self.success_actions.append(action)


    def add_failure_action(self, action):
        self.failure_actions.append(action)


    def perform_success_actions(self, master, state, game_state):
        map(lambda action: action.perform(master, state, game_state), self.success_actions)


    def perform_failure_actions(self, master, state, game_state):
        map(lambda action: action.perform(master, state, game_state), self.failure_actions)

