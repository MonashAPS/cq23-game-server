# Running your code

In order to run your player, open the terminal and go to the folder containing your player's code (the folder that has
the `Dockerfile` in it). Once there, run:

```shell
cq23 run
```

This will start the game, where both players are your code (i.e. your code vs your code).

## Change Map

If you want to run the game in a different map, run:

```shell
cq23 run map=<map name>
```

Make sure there are no spaces before or after `=` and replace `<map name>` with the name of the map. You can find all
available maps in [Map](../game_logic/map.md).

## Change Opponent

The `run` command runs your code against your code by default. But you can choose to play against one of the sample bots
or another code on your computer or even an older version of your code.

### Running against a sample bot

There are some sample bots created for you to test your code against. These are:

- `sample-bot-1`: Goes to the centre of the map and shoots towards the opponent

In order to run your code against one of these, you can run the command the same way as described before, but with this argument:

```shell
cq23 run away=<name of the sample bot>
```

When you run like this, you will be team "Home" and they will be "Away". You can even run two sample bots against each other:

```shell
cq23 run home=<name of one sample bot> away=<name of other sample bot>
```

### Running against another local code

You may want to run your code against another code or an older version of your code. This can be done using the `build` command.

When you `build` a submission, you're creating an image of that bot which can be used in the game. For example, you may have your
main code in a folder called `my_main_bot` and another test bot you've worked on in `my_other_bot`.

In order to run these against each other, you first need to build your `my_other_bot`. Go inside its folder and run:

```shell
cq23 build <name>
```

Replace `<name>` with `my_other_bot` or any other name. You will use this name when you want to run the game.

Now that the other code is built, go to `my_main_bot` folder and run this:

```shell
cq23 run away=<the same name as above>
```

This will run your current code against the code in that folder.

You may use the same thing to take snapshots of your code. For example, you can run `cq23 build my_bot_1` to create that snapshot.
Then continue developing your code. Once you want to test the new code against the old one, run: `cq23 run away=my_bot_1`. This will
set the opponent your old snapshot.

## Done Testing?

Once you're happy with your source code, you can submit it for the competition. Go to [Submitting Your Code](submitting_your_code.md)
for more information.