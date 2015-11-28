from Task import Task
from mock import Mock

class TestTask:

    def setup(self):
        self.task = Task()
        self.stage.requirements = []
        self.stage.actions = []
        pass

    def test_all_requirements_satisfied(self):
        requirement = Mock()
        requirement.satisfied = Mock(return_value=True)
        self.task.add_success_requirement(requirement)
        assert self.stage.success_requirements_satisfied() == True

    def test_perform_actions(self):
        action = Mock()
        self.task.add_success_action(action)
        self.task.perform_success_actions()
        assert action.perform.called
