import requests

print("NOTE: this script only provides basic request needs, headers and arguments, retries are not supported")

name = input("Enter name of file including any extensions, leave blank for def=\"new_req.txt\"\n:") or "new_req.txt"
url = input("Enter host site url to perform a get request from\n:")

print("REQUESTING")
r = requests.get(url)
print("RESPONSE STATUS:", r.status_code)
txt = r.text
print("REQUEST COMPLETED")

file = open(name, "w")
print("CREATED FILE", name)

print("WRITING TO FILE")
file.write(txt)
file.close()
r.close()
input("... TASK COMPLETE ...")
