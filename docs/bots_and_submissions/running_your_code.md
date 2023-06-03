# Running your code

In order to run your player, open the terminal and go to the folder containing your player's code (the folder that has
the `Dockerfile` in it). Once there, run:

```shell
cq23 run
```

This will start the game, where both players are your code (i.e. your code vs your code).

If you want to run the game in a different map, run:

```shell
cq23 run map=<map name>
```

Make sure there are no spaces before or after `=` and replace `<map name>` with the name of the map. You can find all
available maps in [Map](../game_logic/map.md).