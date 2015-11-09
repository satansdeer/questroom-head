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
        stage = Stage()
        map(lambda req:    stage.add_requirement(Requirement(eval(req))), sequential_stage["requirements"])
        map(lambda action: stage.add_action(Action(eval(action))), sequential_stage["actions"])
        stage.title = sequential_stage["title"] if "title" in sequential_stage else "No title"
        game_state.add_stage(stage)
    return game_state

