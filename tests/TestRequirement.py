from Requirement import Requirement

class TestRequirement:

    def test_satisfied(self):
        requirement = Requirement()
        requirement.state = [0,1,2]
        requirement.validation_function = lambda state: state[2] == 2
        assert requirement.satisfied() == True
