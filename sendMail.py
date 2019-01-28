import os
def sendMessage(url):
     os.system("bash -c \" notify -t \"è_stata_modificato:"+url+"\"\"")

def sign(value):
     os.system("bash -c \" notify -r "+value+"\"\"")
