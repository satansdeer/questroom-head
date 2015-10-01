from Stage import Stage
from mock import Mock

class TestStage:

    def setup(self):
        self.stage = Stage()
        self.stage.requirements = []
        self.stage.actions = []
        pass

    def test_all_requirements_satisfied(self):
        requirement = Mock()
        requirement.satisfied = Mock(return_value=True)
        self.stage.add_requirement(requirement)
        assert self.stage.all_requirements_satisfied() == True

    def test_perform_actions(self):
        action = Mock()
        self.stage.add_action(action)
        self.stage.perform_actions()
        assert action.perform.called
