# Communication

The communication between you and the game server is pretty straight forward.
The game server gives you information about the game and, you will decide what your tank should do based on the
information you have received.

All the communication happens through standard input and standard output. That means, when it's time for you to receive
new information about the game, you take an input (`input()` in python or `std::cin` in c++ etc.) and parse the received
JSON message and, when it's time for you to tell the game server something to do, you print it as a JSON message
(`print()` in python or `std::cout` in c++ etc.).

## Message Format

All messages you receive from the game will be an object with two keys: `message` and `time`.

The `message` will be the actual message the game has sent you. The `time` denotes how much time you have (in seconds) to
process this message. Sometimes you will need to respond to the message, sometimes you don't. If you need to respond to
the message, you should do so before the given time otherwise your message will not be read.

This timeout time will be 0.1 for most of the ticks.

Here is an example of how the message format looks like:

```json
{
  "message": "Some message for the client",
  "time": 0.1
}
```

## Special Signals

There are two exceptions to this format. At two points, the game will just send a JSON string to you, to signal about
the game stage. One is after the "World Init" stage has finished, one is after the main game loop has finished. You will
learn more about what these two stages are down below.

The first signal is `"END_INIT"`:
```json
"END_INIT"
```

and the second signal is `"END"`.
```json
"END"
```

When you receive the end signal, you should close your program.

## World Init

Before the main communication cycle starts between the game and your players, a few messages will be sent from the game
to you in, one-way. These messages are some initial information about the game and the map that you will need to
implement your strategies.

These include, your tank id (so you would know which tank of the two you are controlling), the location of the walls,
the location of the boundaries around the map, etc. Refer to [Types](types.md) to see a full list of objects that could
be in these messages.

### Your Tank ID

The very first message you receive will be your tank id. This is important so you can identify which tank belongs to
you in the game. If you've read the [tanks page](../game_objects/tank.md), you would know that tanks (like all other
objects in the game) have an id which the game refers to throughout all communications.

This is the first message you will receive:
```json
{
  "message": {
    "your-tank-id": "tank-12"
  },
  "time": 0.1
}

```

### Other objects

The rest of the messages here (before the main communication cycle starts) are information about other objects.
This is the type of message you would receive here:

```json
{
  "message": {
    "deleted_objects": [
      ...
    ],
    "updated_objects": {
      "bullet-23": {
        "position": [
          353.12,
          112.53
        ],
        ...
      },
      ...
    }
  },
  "time": 0.1
}
```

As explained above, after each message you receive, you will be given an amount of time for your code to process
that information. This applies to pre and post initial messages. In the example above, you've been given 0.1 seconds to
process this information but, you do not need to respond with anything at this stage.

After the initialisation is done, you will receive the end init signal (explained above). This message is to signal
you that the initialisation is done and the game has begun, this means you will be expected to respond to the messages from the
next tick.

```json
... game information ...
"END_INIT"
... future messages ...
```

## Main Game Loop

This is where the main game loop starts. This is also where your code and the game will start to go back and forth and
you will make decisions about what you want to do.

Everytime you read information, the game will send you a message containing all the objects that have been removed from
the game since the last turn and all the objects that have been "updated" since the last turn. An object is considered
updated if one of its attributes has changed.

The format of these messages is exactly the same as the messages you received in world init:

```json
{
  "message": {
    "deleted_objects": [
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
    "updated_objects": {
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

Once in the main game loop, make sure you respond with your actions in the given timeout time.

## Message Data

As said above, the messages have two keys. A `message` which contains the actual data and a `time`.
In this section, we learn about what sort of data will be inside the `message` object.

The `message` object has two main parts: the updated_objects and the [deleted_objects](deleted_objects.md).

[deleted_objects](deleted_objects.md) will be a list of json objects letting you know which game objects have been removed
from the game.

updated_objects will be an object where the keys are the object ids (e.g. `tank-1`, `bullet-24`) and the value will
be an object containing all the information. To see what's inside the information object you can refer to the
corresponding type (e.g. [tank](../game_objects/tank.md), [bullet](../game_objects/bullet.md), etc.).

Note that the object information you receive will only be the UPDATES. Consider the following example.

### Example

You're given the following message in the first tick of the game:

```json
{
  "message": {
    "deleted_objects": [
      ...
    ],
    "updated_objects": {
      "tank-1": {
        "position": [
          655.03,
          815.03
        ],
        ...
      },
      ...
    }
  },
  "time": ...
}
```

`tank-1` decides to not move or do anything else after the first tick, in other words there are no UPDATES for tank-1.
So when you receive the object information in the second tick of the game, there will be no information about tank-1.

```json
{
  "message": {
    "deleted_objects": [
      ...
    ],
    "updated_objects": {
      "bullet-23": {
        "position": [
          353.12,
          112.53
        ],
        ...
      },
      ...
    }
  },
  "time": ...
}
```

The purpose of this way of communicating is that you don't have to process redundant messages like the position of the
stationary objects every tick. So we only send you what has changed in the game since the last tick.

## Sending actions

Once you have received a message from the game, you will have some time (given to you in the message, usually 0.1 seconds)
to make a decision and respond with the action that you'd like to take. If you fail to respond in the given time
(or respond with an invalid message), the game will assume you didn't take any actions.

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
