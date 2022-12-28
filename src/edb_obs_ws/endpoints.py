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
