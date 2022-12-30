import asyncio
import json
import os.path
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

VERSION = "2022.12.28.1"

config_path: str = str(xdg_config_home()) + "/eldecko/backend/"
config_file: str = config_path + "obsws.json"
host = "localhost"
port = "4455"
password = "1234IsABadPassword"
websocket: WebSocketClient = None
id_params = IdentificationParameters(ignoreNonFatalRequestChecks=False)


# Initializes this backend and all required event loops and websockets.
def edb_init():
    __load_obs_ws_config()


def edb_stop():
    __stop_websocket()


# Fires a given event to OBS Studio via it's Websocket server
def edb_fire_event(even_type: str, event_properties: dict = None):
    loop = None

    # This needs to be done because asyncio does not generate an even loop for any threads except the main thread
    # But since this function may also be used in a threaded environment we need to ensure there is an event loop.
    # So we try to get the current event loop and if that fails we generate a new one.
    # Note: creating a new Websocket also requires an active event loop.
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError as ex:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    global websocket
    if websocket is None:
        url = "ws://" + host + ":" + port
        websocket = WebSocketClient(url, password, id_params)
    loop.run_until_complete(__make_request(even_type, event_properties))


# Returns a dictionary with all available event types and their respective event parameters.
# Every event returns human_readable_name which may be used to present this endpoint in a UI to the user.
def edb_available_events():
    return {
        "GetVersion": {"human_readable_name": "Get OBS Studio Version"},
        "SetCurrentProgramScene": {
            "human_readable_name": "Switch OBS Studio Scene",
            "name": "string"
        },
        "GetSceneList": {
            "human_readable_name": "Returns list of all available scenes"
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


async def __stop_websocket():
    await websocket.disconnect()


async def __make_request(even_type: str, event_properties: dict = None):
    if not websocket.is_identified():
        await websocket.connect()
        await websocket.wait_until_identified()
    result = None

    match even_type:
        case "GetVersion":
            result = await endpoints.__get_version(websocket)
        case "SetCurrentProgramScene":
            result = await endpoints.__set_current_program_scene(websocket, event_properties["name"])
        case "GetSceneList":
            result = await endpoints.__get_scene_list(websocket)
        case other:
            pass
