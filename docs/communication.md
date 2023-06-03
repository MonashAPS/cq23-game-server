# Communication

The communication between you and the game server is pretty straight forward.
The game server gives you information about the game and you will decide what your tank should do based on the information you have received.

All the communication happens through standard input and standard output, that means that any time you want to receive information about the game you take an input (`input()` in python or `std::cin` in c++ etc.) and any time you want to tell the game server something to do, you print it (`print()` in python or `std::cout` in c++ etc.).

## Receiving game info

All the messages you receive from the game server will be json messages and in the following format:

```json
{
    "events": [
        {
            "event_type": "BULLET_SPAWN",
            "data": {
                "id": "bullet-3",
                "tank_id": "tank-1",
                "position": [
                    661.92,
                    833.83
                ],
                "velocity": [
                    -425.74,
                    -145.75
                ],
                "angle": 3.47
            }
        },
        {
            "event_type": "BULLET_DESTROYED",
            "data": {
                "id": "bullet-3",
                "position": [
                    577.98,
                    805.1
                ]
            }
        }
    ],
    "object_info": {
        "tank-1": {
            "type": 1,
            "position": [
                655.03,
                815.03
            ],
            "velocity": [
                -100.0,
                -100.0
            ],
            "hp": 10
        },
        "tank-2": {
            "type": 1,
            "position": [
                595.03,
                130.0
            ],
            "velocity": [
                -100.0,
                100.0
            ],
            "hp": 10
        },
        "bullet-2": {
            "type": 2,
            "position": [
                572.43,
                171.76
            ],
            "velocity": [
                -133.83,
                449.64
            ],
            "hp": 1
        }
    }
}
```

As you can see the message you receive from the game server has two main parts, the object information and the events. For more information on events you can refer to [events](events.md) and for more information about object information you can refer to the corresponding object page. (i.e. [tank](tank.md))

Note that the object information you receive will only be the UPDATES. Consider the following example.

### Example

You're given the following message in the first tick of the game:

```json
"object_info": {
    "tank-1": {
        "position": [
            655.03,
            815.03
        ],
        ...
    },
    ...
}
```

`tank-1` decides to not move or do anything else after the first tick, in other words there are no UPDATES for tank-1. So when you receive the object information in the second tick of the game, there will be no information about tank-1.

```json
"object_info": {
    "bullet-23": {
        "position": [
            353.12,
            112.53
        ],
        ...
    },
    ...
}
```

The purpose of this way of communicating is that you don't have to process redundant messages like the position of the stationary objects every tick so we only send you what has changed in the game since the last tick.

## Sending actions

Once you have received a message from the game server, you will have approximately 0.1 seconds to make a decision and respond to the game server with the action that you'd like to take.

For more information on actions and their format, refer to [actions](actions.md)
