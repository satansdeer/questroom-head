from __future__ import print_function
import yaml
from GameState import GameState
from Requirement import Requirement
from Stage import Stage
from Action import Action
from Lambdas import *


def parse(file_name):
    game_state = GameState()
    f = open(file_name)
    quest_script_source = yaml.safe_load(f)
    f.close()
    for sequential_stage in quest_script_source["sequential_stages"]:
        stage = fillStage(sequential_stage)
        game_state.add_stage(stage)

    for repetitive_stage in quest_script_source["repetitive_stages"]:
        stage = fillStage(repetitive_stage)
        game_state.add_repetitive_stage(stage)

    return game_state


def fillStage(type_stage):
    stage = Stage()
    map(lambda req:    stage.add_requirement(
            Requirement(eval(req))), type_stage["requirements"])
    map(lambda action: stage.add_action(
            Action(eval(action))), type_stage["actions"])
    return stage
