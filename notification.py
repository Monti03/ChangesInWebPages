import os
def send_message(url):
     os.system("bash -c \" notify -t \"has_been_modified:"+url+"\"\"")

def sign(value):
     os.system("bash -c \" notify -r "+value+"\"")
