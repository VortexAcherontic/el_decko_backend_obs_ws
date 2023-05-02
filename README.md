# El Decko Backend OBS Studio Websocket

OBS Studio websocket based backend for El Decko.

## First run

Upon running El Decko the first time with this backend installed it will create an empty default config to connect to
your local OBS Studio instance at: `$XDG_CONFIG/eldecko/backend/obsws.json`.  
Please update the generated default credentials with the actual port and password of what is shown inside your OBS
Studio Websocket Settings.

## Use this backend

In order to use this backend you need to supply the `streamdeck.json` generated
by [El Decko Core](https://github.com/Z-Ray-Entertainment/el_decko_core) with the following `key_config`:

```
{
    "STREAM_DECK_SERIAL_NUMBER": {
        "brightness": 30,
        "key_config": {
            "0": {
            "backend": "edb_obs_ws",
            "event": "SetCurrentProgramScene",
            "event_parameters": {"name":"S: Desktop"},
            "image_idle": null,
            "image_pressed": null
            }
        }
    }
}
```

This will configure the very first key (`0`) to use this plugin (`edb_obs_ws`) and bind the event `SwitchScene` to it.  
The event will receive the parameter map defined by `event_parameters`, `name` defines the name of you scene within OBS
Studio.  
More supported websocket events will follow.

### Implemented websocket protocols

#### SetCurrentProgramScene

Tells OBS Studio to change the currently visible Scene to any other available scene.

Event name: `SetCurrentProgramScene`  
Parameters: `name` -> Name of your local OBS Studio Scene

#### GetSceneList

Returns a list with all available Scenes within OBS Studio.

Event name: `GetSceneList`  
Parameters: `None`

#### SetSceneItemEnabled

Set the enabled state of an item inside a given scene  

Event name: `SetSceneItemEnabled`
Parameters:  
`scene_name` -> The name of the scene  
`item_id` -> The internal ID of the required item.  
You can find this inside your OBS Scene Settings JSON.  
`enabled` -> True or False to show/hide the item.

##### Example JSON:
````
"key_config": {
    "<key_number>": {
        "backend": "edb_obs_ws",
        "event": "SetSceneItemEnabled",
        "event_parameters": {"scene_name":"S: Confeti", "item_id": 42, "enabled": false},
        "image_idle": "<some_image_path>",
        "image_pressed": null,
        "label": "Hide Video"
      },
}
````

#### ToggleSceneItemEnabled

Similar to SetSceneItemEnabled does this event show/hide an item in a given scene.  
But additionally it queries the current item state and sets it to the opposite state. 

Event name: `SetSceneItemEnabled`
Parameters:  
`scene_name` -> The name of the scene  
`item_id` -> The internal ID of the required item.  
You can find this inside your OBS Scene Settings JSON.  

##### Example JSON:
````
"key_config": {
    "<key_number>": {
        "backend": "edb_obs_ws",
        "event": "ToggleSceneItemEnabled",
        "event_parameters": {"scene_name":"S: Confeti", "item_id": 2},
        "image_idle": "<some_image_path>",
        "image_pressed": null,
        "label": "Confetti!"
      },
}
````