class Stage:

    requirements = []
    actions = []

    def all_requirements_satisfied(self):
        return all(requirement.satisfied() for requirement in self.requirements)

    def add_requirement(self, requirement):
        self.requirements.append(requirement)

    def add_action(self, action):
        self.actions.append(action)

    def perform_actions(self):
        map(lambda action: action.perform(), self.actions)

