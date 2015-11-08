class Stage:

    def __init__(self):
        self.requirements = []
        self.actions = []

    def all_requirements_satisfied(self, master, stage):
        return all(requirement.satisfied(master, stage) for requirement in self.requirements)

    def add_requirement(self, requirement):
        self.requirements.append(requirement)

    def add_action(self, action):
        self.actions.append(action)

    def perform_actions(self, master, stages):
        # print ("Connetction: in perform_action")

        map(lambda action: action.perform(master, stages), self.actions)

