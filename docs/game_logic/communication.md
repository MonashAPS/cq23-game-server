# Communication

The communication between you and the game server is pretty straight forward.
The game server gives you information about the game and, you will decide what your tank should do based on the
information you have received.

All the communication happens through standard input and standard output. That means, when it's time for you to receive
new information about the game, you take an input (`input()` in python or `std::cin` in c++ etc.) and parse the received
JSON message and, when it's time for you to tell the game server something to do, you print it as a JSON message
(`print()` in python or `std::cout` in c++ etc.).

## Receiving game info

Everytime you read information, the game will send you a message containing all the events that happened since the last
turn and all the objects that have "changed" since the last turn. An object is changed if one of its attributes has changed.

All the messages you receive from the game will be JSON messages and in the following format:

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
                "angle": 217  TODO lets make sure the server is also printing them in degrees now?
            }
        },
        {
            ... data about another event ...
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
        "another-object-id": {
          ... data about this other object ...
        }
    }
}
```

As you can see the message you receive from the game has two main parts: the object information and the events.
Events will be a list of `event` objects. For more information on `event` objects you can refer to [events](events.md).
Object information will be an object where the keys are the object ids (e.g. `tank-1`, `bullet-24`) and the value will
be an object containing all the information. To see what's inside the information object you can refer to the
corresponding type (e.g. [tank](../game_objects/tank.md), [bullet](../game_objects/bullet.md), etc.).

Note that the object information you receive will only be the UPDATES. Consider the following example.

### Example

You're given the following message in the first tick of the game:

```json
{
  "events": [...],
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
}
```

`tank-1` decides to not move or do anything else after the first tick, in other words there are no UPDATES for tank-1.
So when you receive the object information in the second tick of the game, there will be no information about tank-1.

```json
{
  "events": [...],
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
}
```

The purpose of this way of communicating is that you don't have to process redundant messages like the position of the
stationary objects every tick. So we only send you what has changed in the game since the last tick.

## Sending actions

Once you have received a message from the game, you will have approximately 0.1 seconds to make a decision and respond
with the action that you'd like to take. If you fail to respond in the given time (or respond with an invalid mesage), 
the game will assume you didn't take any actions.

For more information on actions and their format, refer to [actions](actions.md)
