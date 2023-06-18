# Starting Your Code

You may use any programming language for your bots. The only requirement is being able to print in standard output and
read from standard input. However, we have created templates for Python, Java and C++ that you can use. They include the
boilerplate code for reading messages and sending actions.

## Python, Java, C++

In order to start a player off an existing template, open your terminal and go to a directory you want to create your bot
in and run this command:

```shell
cq23 new <lang> <a name for your bot>
```

This will create a folder containing a starting code for your selected language. Open this folder in your code editor.

Refer to the `README.md` file in the created folder for more information about the template.

Accepted values for `<lang>` in the command above are `python` - `java` - `cpp`.

## All other languages

You may choose not to use any of the templates or maybe there are no templates for a language you want to use. In that
case, you can start your player by running this command:

```shell
cq23 new raw <a name for your bot>
```

This will create a folder for your player. Refer to the `README.md` file in the folder for more information about how you
can develop your player from there.

Once you have the base source code, you can run the game. Go to [Running Your Code](running_your_code.md) for more information.