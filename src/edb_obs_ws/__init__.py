import asyncio
import json
import os.path
import threading

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

VERSION = "0.0.1"

config_path: str = str(xdg_config_home()) + "eldecko/backend/"
config_file: str = config_path + "obsws.json"
host = "123"
port = "456"
password = "1234IsABadPassword"
websocket: WebSocketClient


def edb_run():
    print("Run EL Decko Backend for Open Broadcaster Software Websockets")
    __load_obs_ws_config()
    url = "ws://" + host + ":" + port
    id_params = IdentificationParameters()
    print(url)
    global websocket
    websocket = WebSocketClient(url, password, id_params)
    callback_loop = threading.Thread(__start_callback_loop())
    callback_loop.start()
    switch_scene()


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


def __start_callback_loop():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__connect_to_obs())
    websocket.register_event_callback(on_switch_scene, "SwitchScenes")
    loop.run_forever()


async def __connect_to_obs():
    await websocket.connect()
    await websocket.wait_until_identified()


async def on_switch_scene(event_data):
    print('Scene switched to "{}".'.format(event_data['sceneName']))


def switch_scene():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__switch_scene())


async def __switch_scene(loop):
    loop.run_until_complete(__connect_to_obs())

    requests = Request("GetVersion")
    response = await websocket.call(requests)
    if response.ok():
        print("Call made: {}".format(response.responseData))

    await websocket.disconnect()