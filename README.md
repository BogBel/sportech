# Test task for sportech company

Goal of the project was creating realtime parsing system for few betting resources

## Getting Started

Dowload the project via `git clone git@github.com:BogBel/sportech.git`


### Prerequisites

Project requires Selenium chrome driver executable.
You can do it via from project dir:
```
wget https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
rm -f chromedriver_linux64.zip
```

### Installing

After cloning the project and downloading driver, you should install dependencies.
Project requires ***Python3.6*** installed.

You can create enviroment or install dependencies into system via

```
pip3 install -r requirements.txt
```

## Running the tests

Execute 

```
python -m unittest discover
```

While you are in project dir

## Running App

After all installations you can run project via
```
python app.py
```
But don't forget that this type of launch requires file ***chromedriver*** file in the project root
If you wan't to specify executable_path you should run with

```
python app.py --executable-path /any/other/path/you/want/
```
You can specify delay in seconds via command-line args

```
python app.py --delay 30
```

You can paste proxy in format: ***ip:port*** for Skybet parser via

```
python app.py --proxy 178.62.81.68:8080
```


## Authors

* **Bohdan Biloshytskiy** - *Initial work* - [BogBel](https://github.com/BogBel)
