import urllib.request
from bs4 import BeautifulSoup
import time
import datetime




def read(url):
    
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,features="lxml")

    # remove all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()    

    # get text
    text = soup.get_text()
    return text

#returns false if the url is not valid else True
def check_url(url):
    try:    
        html = urllib.request.urlopen(url).read()
    except Exception as e:
        print(e)
        return False
    return True
