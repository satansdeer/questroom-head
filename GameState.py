class GameState:

    def __init__(self):
        self.device_master = None
        self.stages = []
        self.current_stage_id = 0

    def current_stage(self):
        if self.current_stage_id >= len(self.stages): return
        return self.stages[self.current_stage_id]

    def start_game_loop(self, callback):
        if not self.master: return
        if not self.slave: return
        if len(self.stages) == 0: return
        while self.current_stage_id < len(self.stages):
            self.game_loop(callback)

    def game_loop(self, callback):
        #self.device_master.sendGetStuckButtons(self.slave)
        #self.state = self.device_master.getButtons(self.slave)
        if not self.state: return
        if not self.current_stage(): return
        if not self.current_stage().all_requirements_satisfied(): return
        print(self.current_stage().title)
        self.current_stage().perform_actions()
        title = self.current_stage().title
        message = {'message': title, 'hearts': 2}
        callback(message) if callback else None
        self.advance()

    def add_stage(self, stage):
        self.stages.append(stage)

    def advance(self):
        self.current_stage_id += 1
