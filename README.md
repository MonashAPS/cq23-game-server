# CodeQuest Game Server 2023

## Purpose
This repo is the game server for the 2023 Code Quest competition.

## installation
Installation can be done with pip:
```shell
pip install pre-commit
```

And init:
```
pre-commit install
```

## Usage
The server can be run by executing the `main.py` python script:
```
python3 src/main.py
```

Once the game has started, it will require input from the standard input. These inputs will generally be requests from the clients.

The server accepts the following requests:

### `Path`
Path can be used to tell the game server to move a specific player to a given position specified by an (x,y) coordinate.

### `Shoot`
Shoot can be used to tell the game server to fire a bullet in a given direction specified by an angle in radians.

## Example Usage
Initialise the game by specifying the players:
```json
{"clients": [{"id": "player1","name": "James","image": "image1"},{"id": "player2","name": "John","image": "image2"}]}
```

Give each player a target destination to follow:
```json
{"player1": {"path": [250,200]}, "player2": {"path": [350,200]}}
```

Give each player an angle in radians to shoot towards:
```json
{"player1": {"shoot": 3.14}, "player2": {"shoot": 0.777}}
```

Stop the player movement:
```json
{"player1": {"path": []}, "player2": {"path": []}}
```

Do nothing:
```json
{"player1": {}, "player2": {}}
```
