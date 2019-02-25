import os

#send message to the phonr through Notify app
def send_message(url):
     os.system("bash -c \" notify -t \"has_been_modified:"+url+"\"\"")

#regusters notfy token of the user
def sign(value):
     os.system("bash -c \" notify -r "+value+"\"")
