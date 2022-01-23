# ScafL - Steam Card Afk Farm for Linux

ScafL (Steam Card Afk Farm for Linux) is a Linux application made with Python to idle Steam games for [Steam Trading Card](https://steamcommunity.com/tradingcards/) drops.
This project was inspired by [Idle Master Extended](https://github.com/JonasNilson/idle_master_extended) and [Idle Master Python](https://github.com/jshackles/idle_master_py).

ScafL features an interface built using Gtk.

This project was made specifically for the "Linux Gamers". Other operating systems may be suported in the future.

## Installing the application

To install ScafL, you first need Python 3.6+ installed and pip. Check your Linux distribution on how to install both of these dependencies.

### Installing on your system

To install ScafL on your system, you need to ensure that GTK and PyGObject is installed on your system. Check your Linux distribution on how to install both of these dependencies.
Then run the following command on your terminal:

```sh
$ pip install scafl
$ python -m scafl
```

### Installing inside a virtual environment

If you want to install the project in a virtual environment, to avoid any dependency conflict, first ensure venv is installed. Then, run the following:

```sh
$ python -m venv /path/to/your/virtual/environment
$ source /path/to/your/virtual/environment/bin/activate
```

Now, while still in your virtual environment, install the package by running the following command:

```sh
(env) $ pip install pycairo pygobject scafl
```

You now have ScafL installed on your virtual environment. This means that every time you want to run ScafL, you need to have the virtual environment activated, which is done by running:

```sh
$ source /path/to/your/virtual/environment/bin/activate
```

To run ScafL, run this command on your terminal:

```sh
(env) $ python -m scafl
```

To exit the virtual environment, run:

```sh
(env) $ deactivate
```

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
(env) $ python path/to/main.py
```


## Suport the project!

You can suport the project by [donating to the main maintainer](https://www.paypal.com/donate/?hosted_button_id=TSARHWQFKSEBA), or by contributing code!