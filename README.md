# ChangesInWebPages
---

## Get a notification when a web page changes
you can control changes in web pages and get a notification on your android phone via [Notify](https://arcane-tor-21270.herokuapp.com/). You can find the source code of the app in this [repo](https://github.com/Monti03/Notify).

<p align="center">
  <img src= "./media/Notification_example.jpg" width="144px" height="256px">

## Installation and requirements
```bash
  sudo apt-get install python3-pyqt5

  pip3 install BeautifulSoup4 || pip3 install beautifulsoup4 || pip3 install bs4

  pip install lxml
```

## Usage
  To start just run: `python3 gui.py`
  
## Gui

<p align="center">
  <img src= "./media/gui.png" width="300px" height="185px">
  
  - Url           -> insert here the url you're checking
  
  - NotifyToken   -> if you have not inserted it yet you have ho insert the token that is shown in the notify app
  
  - Notification  -> check if you whant to have the notification on the phone
  
  - Slider        -> inspection period (minutes)