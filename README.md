# ChangesInWebPages
---
# Notify is no longer working so you can only have notification on your pc

## Get a notification when a web page changes
you can control changes in web pages and get a notification on your android phone via Notify: https://play.google.com/store/apps/details?id=com.kevinbedi.notify

## Installation and requirements
```bash
  sudo apt-get install python3-pyqt4

  pip3 install BeautifulSoup4 || pip3 install beautifulsoup4 || pip3 install bs4

  pip install lxml

  npm install -g notify-cli
```

## Usage
  To start:
  ```python3 gui.py```
  
## Gui
  
  Url           -> insert here the url you're checking
  
  NotifyToken   -> if you have not inserted it yet you have ho insert the token that is shown in the nptify app
  
  notification  -> check if you whant to have the notification on the phone
  
  Slider        -> inspection period (minutes)
