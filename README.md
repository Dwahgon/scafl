# ScafL - Steam Card Afk Farm for Linux

ScafL (Steam Card Afk Farm for Linux) is a Linux application made with Python to idle Steam games for [Steam Trading Card](https://steamcommunity.com/tradingcards/) drops.
This project was inspired by [Idle Master Extended](https://github.com/JonasNilson/idle_master_extended) and [Idle Master Python](https://github.com/jshackles/idle_master_py).

ScafL features an interface built using Gtk.

This project was made specifically for the "Linux Gamers". Other operating systems may be suported in the future.

## Installing the application

To install ScafL, you first need Python 3.6+ installed and pip. Check your Linux distribution on how to install both of these dependencies.

### Running from source

To run ScafL from source, it is recommended that you run it on a virtual environment. To create a virtual environment, run the following command inside the project directory:

```sh
$ python -m venv .env
```

Then, activate the virtual environment:

```sh
$ source .env/bin/activate
```

After activating the virtual environment, install the project's dependencies:

```sh
(env) $ pip install -e .
(env) $ pip install pycairo pygobject
```

To run the project, you must have the virtual environment activated. After ensuring that you're in a virtual environment, run:

```sh
(env) $ python src/scafl
```


## Suport the project!

You can suport the project by [donating to the main maintainer](https://www.paypal.com/donate/?hosted_button_id=TSARHWQFKSEBA), or by contributing code!