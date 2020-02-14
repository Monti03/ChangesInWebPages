import os

#send message to the phonr through Notify app
def send_message(url):
     f = open(".device_id", "r")
     dest = f.read().strip()
     os.system("bash -c \" ./notify.sh -d "+ dest +" -t Changed -c "+url+" \"")


#regusters notfy token of the user
def sign(value):
     f = open(".device_id", "w")
     f.write(value)
     f.close()
