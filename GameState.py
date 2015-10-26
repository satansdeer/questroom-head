# -*- coding: utf-8 -*-
class GameState:

    def __init__(self):
        self.device_master = None
        self.stages = []
        self.repetitive_stages = []
        self.current_stage_id = 0

    def current_stage(self):
        if self.current_stage_id >= len(self.stages): return
        return self.stages[self.current_stage_id]

    def perform_repetitive_stages(self, master, state):
        if self.current_stage_id >= len(self.stages): return
        for stage in self.repetitive_stages:
            if not stage.all_requirements_satisfied(master, state):
                continue
            stage.perform_actions(master, state)

    def start_game_loop(self):
        if not self.device_master: return
        if not self.slave: return
        if len(self.stages) == 0: return

        while self.current_stage_id < len(self.stages):
            self.game_loop()

    def game_loop(self):
        state = 1
        # if not self.state: return
        if not self.current_stage(): return
        self.perform_repetitive_stages(self.device_master, state)
        if not self.current_stage().all_requirements_satisfied(self.device_master, state): return
        self.current_stage().perform_actions(self.device_master, state)
        print("Current stage", self.current_stage_id)
        self.advance()

    def add_stage(self, stage):
        self.stages.append(stage)

    def add_repetitive_stage(self, stage):
        self.repetitive_stages.append(stage)

    def advance(self):
        self.current_stage_id += 1
