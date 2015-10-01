from GameState import GameState
from mock import MagicMock
from mock import Mock

class TestGameState:
    def setup(self):
        self.game_state = GameState()
        self.game_state.stages = []

    def teardown(self):
        self.game_state = None

    def test_add_stage(self):
        assert len(self.game_state.stages) == 0
        self.game_state.add_stage("test stage")
        assert len(self.game_state.stages) == 1

    def test_advance(self):
        assert self.game_state.current_stage_id == 0
        self.game_state.advance()
        assert self.game_state.current_stage_id == 1

    def test_game_loop(self):
        stage = Mock()
        stage.all_requirements_satisfied = Mock(return_value=True)
        self.game_state.add_stage(stage)
        self.game_state.game_loop()
        assert stage.perform_actions.called
