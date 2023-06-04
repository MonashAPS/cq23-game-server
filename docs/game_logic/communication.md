# Communication

The communication between you and the game server is pretty straight forward.
The game server gives you information about the game and, you will decide what your tank should do based on the
information you have received.

All the communication happens through standard input and standard output. That means, when it's time for you to receive
new information about the game, you take an input (`input()` in python or `std::cin` in c++ etc.) and parse the received
JSON message and, when it's time for you to tell the game server something to do, you print it as a JSON message
(`print()` in python or `std::cout` in c++ etc.).

## Client id

The very first message you receive will be your client id. This is important so you can identify which tank belongs to you in the game. If you've read the [tanks page](../game_objects/tank.md), you would know that the id of your tank will
be your client id plus `-tank`.

```json
{
  "client-id": "tanksters"
}
```

## World init

The first part of receiving the game information will be initialising the world. You will receive multiple messages on
separate lines. These messages are meant to give you an idea of what the map looks like and what objects there are in the map. You should keep that information somewhere in your code.

This is the type of message you would receive in the world init section:

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

**Note that there is no `message` field and there is also no `time` field.** (this will make more sense when you read
the next section)

After the initialisation is done, you will receive a non JSON message that reads `"END_INIT"`. This message is to signal
you that the initialisation is done and the game has begun, this means you will be expected to choose actions from the
next tick.

```json
... game information ...
"END_INIT"
... future messages ...
```

## Receiving game info

This is where the main game loop starts. This is also where your code and the game will start to go back and forth and
you will make decisions about what you want to do.

Everytime you read information, the game will send you a message containing all the events that happened since the last
turn and all the objects that have "changed" since the last turn. An object is changed if one of its attributes has changed.

The format of these messages is slightly different to the messages you receive in world init. The only difference is
that you will receive the game information inside the `message` field and you will also receive an additional field
`time` which indicates how much time you have to respond to the game server.

```json
{
  "message": {
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
          "angle": 217
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
  },
  "time": 0.1
}
```

As you can see the message you receive from the game has two main parts: `message` and `time`. `message` will contain
game information and `time` will contain how much time you have to respond. More on both below.

### Message

The `message` you receive from the game also has two main parts: the object information and the events.
Events will be a list of `event` objects. For more information on `event` objects you can refer to [events](events.md).
Object information will be an object where the keys are the object ids (e.g. `tank-1`, `bullet-24`) and the value will
be an object containing all the information. To see what's inside the information object you can refer to the
corresponding type (e.g. [tank](../game_objects/tank.md), [bullet](../game_objects/bullet.md), etc.).

Note that the object information you receive will only be the UPDATES. Consider the following example.

#### Example

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

### Time

As you might have noticed, the message format above had two outter parts: `message` and `time`. We've already discussed
the `message` part above but what is the `time` part? The time indicates how much time you have to come up with an
action and respond to the server. For example `"time": 0.1` means that you have 0.1 seconds to respond after you've
received the message from the game server.

## Sending actions

Once you have received a message from the game, you will have approximately 0.1 seconds to make a decision and respond
with the action that you'd like to take. If you fail to respond in the given time (or respond with an invalid mesage),
the game will assume you didn't take any actions.

For more information on actions and their format, refer to [actions](actions.md)

## Recap

To summarise, the communication in the game happens in the following order:

```json
incoming> receive your client id

// world init
incoming> world init msg1
incoming> world init msg2
incoming> world init msg3
...
incoming> "END_INIT"

// main game loop
incoming> game info
outgoing< your chosen action
```
