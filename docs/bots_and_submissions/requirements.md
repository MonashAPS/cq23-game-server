# Technical Requirements

You will need a few things installed on your computer before you can start working on your bot:

## Docker
Both the game and the players need Docker to run properly. If you don't know what Docker is or how it works,
it's not a problem. We will talk about the basics of it on the day of the competition (you are also welcome to do your
own research). But for now, make sure you have it installed on your computer. We suggest installing Docker Desktop. You
can find its download links from here: <https://docs.docker.com/get-docker/>.

## A Working Terminal
Regardless of your Operating System, your computer has a command line interface that you can use
to run commands. In Mac and Linux systems this is simply called Terminal. On Windows, you have the option of CMD or
Powershell (which is what we prefer). Make sure you know how to open your terminal and run basic commands. Again, you do
not need to be an expert with your terminal, we will give you all the commands you need. For now, just make sure it
opens. Note: if you use other terminals like iTerm, etc. that's fine too.

## Git
Your terminal needs to have git installed in it. Git is a version controlling system. In simple words, it allows
you to save changes to your code and work on it as a team. Even if you are not planning to have a team for CodeQuest,
you still need to have Git installed because... we have a team even if you don't. And we have prepared a bunch of
templates that you will need to get started and, you need Git to get them. You can use this guide to install Git:
<https://github.com/git-guides/install-git>.

## Python 3

The game is created with Python, so you need Python if you want to run the game on your computer.
You can check if you have python installed by running:

```shell
python --version
```

If the printed version does not start with 3 (e.g. `3.9.12`) then try:

```shell
python3 --version
```

If the printed version is 3, you have Python installed. If not (or if the command says "Command not found") then you
need to install Python. You can download and install Python from <https://www.python.org/downloads/>.

## Pip

After you have installed Python, close your terminal (if it's open) and open another one. Then check if pip was
installed with it as well (in most cases it will be):

```shell
pip --version
```

If the version at the end in parentheses is not `3.<something>` try this:

```shell
pip3 --version
```

If the version at the end of the output line is not `3.<something>` or if the command fails, you need to install pip as
well. You can do so from <https://pip.pypa.io/en/stable/installation/>

Again, you don't need to know what pip is before the day; we'll tell you about it. But you're welcome and encouraged to
do your own research.

## Disk Space
Ideally, you will need about 2-3 gbs of disk space on your computer. Don't worry you're not going to
install anything. It's just that loading the game and starting your players etc. takes up some space which you will get
back when you're done with the competition!

## CQ23

Now that you have Python and Pip installed, it's time to install CodeQuest tools to run the game. For that, run this in
your terminal:

```shell
pip install cq23
```

or, if your installation is called `pip3` then:

```shell
pip3 install cq23
```

This will install CodeQuest 23 interface in your terminal. You can confirm it's working by running:

```shell
cq23 check
```

This will also show you if you have the other requirements installed or not.

If you need help with any of these requirements, check out the [help page](../help.md).