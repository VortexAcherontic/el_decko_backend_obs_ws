from simpleobsws import Request, WebSocketClient


async def __set_current_program_scene(ws: WebSocketClient, scene_name: str):
    requests = Request("SetCurrentProgramScene", requestData={"sceneName": scene_name})
    response = await ws.call(requests)
    if response.ok():
        return response


async def __get_version(ws: WebSocketClient,):
    requests = Request("GetVersion")
    response = await ws.call(requests)
    if response.ok():
        return response


async def __get_scene_list(ws: WebSocketClient):
    requests = Request("GetSceneList")
    response = await ws.call(requests)
    if response.ok():
        return response.responseData["scenes"]


async def __set_scene_item_enabled(ws: WebSocketClient, scene_name: str, item_id: int, enabled: bool):
    request = Request("SetSceneItemEnabled", requestData={
        "sceneName": scene_name,
        "sceneItemId": item_id,
        "sceneItemEnabled": enabled
    })
    response = await ws.call(request)
    if response.ok():
        return response


async def __toggle_scene_item_enabled(ws: WebSocketClient, scene_name: str, item_id: int):
    request = Request("GetSceneItemEnabled", requestData={"sceneName": scene_name, "sceneItemId": item_id})
    response = await ws.call(request)
    if response.ok():
        item_enabled = response.responseData["sceneItemEnabled"]
        if type(item_enabled) is bool:
            await __set_scene_item_enabled(ws, scene_name, item_id, not item_enabled)
