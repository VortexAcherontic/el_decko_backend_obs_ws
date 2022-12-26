import asyncio
import json
import os.path
from asyncio import AbstractEventLoop

from simpleobsws import WebSocketClient, IdentificationParameters, Request
from xdg import (
    xdg_cache_home,
    xdg_config_dirs,
    xdg_config_home,
    xdg_data_dirs,
    xdg_data_home,
    xdg_runtime_dir,
    xdg_state_home,
)

from edb_obs_ws import endpoints

VERSION = "0.0.1"

config_path: str = str(xdg_config_home()) + "eldecko/backend/"
config_file: str = config_path + "obsws.json"
host = "localhost"
port = "4455"
password = "1234IsABadPassword"
websocket: WebSocketClient


# Initializes this backend and all required event loops and websockets.
def edb_init():
    global websocket

    print("Run EL Decko Backend for Open Broadcaster Software Websockets")
    __load_obs_ws_config()
    url = "ws://" + host + ":" + port
    id_params = IdentificationParameters()
    print(url)
    websocket = WebSocketClient(url, password, id_params)


def edb_stop():
    pass


# Fires a given event to OBS Studio via it's Websocket server
def edb_fire_event(even_type: str, event_properties: dict = None):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__connect_to_obs())
    match even_type:
        case "GetVersion":
            return loop.run_until_complete(endpoints.__get_version(websocket))
        case "SwitchScene":
            return loop.run_until_complete(endpoints.__switch_scene(websocket, event_properties["name"]))
        case "GetSceneList":
            return loop.run_until_complete(endpoints.__get_available_scenes(websocket))
        case other:
            pass
    loop.run_until_complete(__stop_websocket())


# Returns a dictionary with all available event types and their respective event parameters.
# Every event returns human_readable_name which may be used to present this endpoint in a UI to the user.
def edb_available_events():
    return {
        "GetVersion": {"human_readable_name": "Get OBS Studio Version"},
        "SwitchScene": {
            "human_readable_name": "Switch OBS Studio Scene",
            "name": "string"
        }
    }


def __load_obs_ws_config():
    global host
    global port
    global password

    if not os.path.exists(config_path):
        os.makedirs(config_path)
    if not os.path.isfile(config_file):
        __create_empty_config()
    try:
        with open(config_file) as input_file:
            data = json.load(input_file)
            input_file.close()
            host = data["host"]
            port = data["port"]
            password = data["password"]
    except json.decoder.JSONDecodeError as e:
        print(e)


def __create_empty_config():
    config_data = {
        "host": host,
        "port": port,
        "password": password
    }
    with open(config_file, "w+", encoding="utf-8") as outfile:
        json.dump(config_data, outfile, ensure_ascii=False, indent=2)
        print("Default configuration created at " + config_file + " please edit credentials.")


async def __connect_to_obs():
    await websocket.connect()
    await websocket.wait_until_identified()


async def __stop_websocket():
    await websocket.disconnect()
