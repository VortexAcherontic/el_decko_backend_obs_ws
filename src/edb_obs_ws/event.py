from enum import Enum
from typing import List


class EventParamType(Enum):
    STRING = "string"
    BOOLEAN = "boolean"
    INTEGER = "integer"


class EventType(Enum):
    GET_VERSION = "GetVersion"
    SET_CURRENT_PROGRAM_SCENE = "SetCurrentProgramScene"
    GET_SCENE_LIST = "GetSceneList"
    SET_SCENE_ITEM_ENABLED = "SetSceneItemEnabled"
    TOGGLE_SCENE_ITEM_ENABLED = "ToggleSceneItemEnabled"


class EventParam:
    def __init__(self, name: EventType, ptype: EventParamType):
        self.name = name
        self.ptype = ptype


class Event:
    def __init__(self, name: str, description: str, parameters: List[EventParam]):
        self.name = name
        self.description = description
        self.parameters = parameters


events: List[Event] = [
    Event(EventType.GET_VERSION, "Get OBS Studio Version", []),
    Event(EventType.SET_CURRENT_PROGRAM_SCENE, "Switch OBS Studio Scene", [EventParam("name", EventParamType.STRING)]),
    Event(EventType.GET_SCENE_LIST, "Returns list of all available scenes", []),
    Event(EventType.SET_SCENE_ITEM_ENABLED, "Set the enabled state of a given scene Item in a given scene", [
        [EventParam("scene_name", EventParamType.STRING)],
        [EventParam("item_id", EventParamType.INTEGER)],
        [EventParam("enabled", EventParamType.BOOLEAN)]
    ]),
    Event(EventType.TOGGLE_SCENE_ITEM_ENABLED, "Set the enabled state of a given scene Item in a given scene", [
        [EventParam("scene_name", EventParamType.STRING)],
        [EventParam("item_id", EventParamType.INTEGER)]
    ])
]
