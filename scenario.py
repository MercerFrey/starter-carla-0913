import json

scenario = {
        
    "hero":{
        "spawn_point":{
            "location": {
                "x": -400,
                "y": 37.8,
                "z": 0.28
            },

            "rotation": {
                "pitch": 0.000000,
                "yaw": -0.368408,
                "roll": 0.000000
            },
        },
        "way_points":[
            {
                "x": 300,
                "y": 37.8,
                "z": 0.281942
            },
            {
                "x": -380,
                "y": 37.8,
                "z": 0.281942
            }
        ],
        "target_speed": 25
    },
    "other1":{
        "spawn_point":{
            "location": {
                "x": -392,
                "y": 37.8,
                "z": 0.28
            },

            "rotation": {
                "pitch": 0.000000,
                "yaw": -0.368408,
                "roll": 0.000000
            },
        },
        "way_points":[
            {
                "x": 300,
                "y": 37.8,
                "z": 0.281942
            },
            {
                "x": -380,
                "y": 37.8,
                "z": 0.281942
            }
        ],
        "target_speed": 25
    },
}

with open('scenario_1.json', 'w') as f:
    json.dump(scenario, f, indent=4)